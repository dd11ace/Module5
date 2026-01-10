import pytest
from api.api_manager import APIManager
from models.base_models import RegisterUserResponse, UserData
from entities.user import User
from enums.roles import Roles


class TestUser:
    def test_register_user(
        self, api_manager: APIManager, creation_user_data: UserData
    ) -> None:
        response = api_manager.auth_api.register_user(
            user_data=creation_user_data
        ).json()
        register_user_response = RegisterUserResponse(**response)

        assert register_user_response.email == creation_user_data.email, (
            "Email не совпадает"
        )
        assert (
            register_user_response.get_roles_as_strings()
            == creation_user_data.get_roles_as_strings()
        )
        assert Roles.USER in register_user_response.roles

    def test_get_user_by_locator(
        self, super_admin: User, creation_user_data: UserData
    ) -> None:
        user_data_dict = creation_user_data.model_dump(mode="json")

        created_user_response = super_admin.api.user_api.create_user(
            user_data_dict
        ).json()
        response_by_id = super_admin.api.user_api.get_user(
            created_user_response["id"]
        ).json()
        response_by_email = super_admin.api.user_api.get_user(
            creation_user_data.email
        ).json()

        assert response_by_id == response_by_email, (
            "Содержание ответов должно быть идентичным"
        )
        assert response_by_id.get("id") and response_by_id["id"] != "", (
            "ID должен быть не пустым"
        )
        assert response_by_id.get("email") == creation_user_data.email
        assert response_by_id.get("fullName") == creation_user_data.fullName
        assert response_by_id.get("roles", []) == creation_user_data.roles_strings
        assert response_by_id.get("verified") is True
        assert response_by_id.get("banned") is False
