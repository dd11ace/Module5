import pytest
import allure
from api.api_manager import APIManager
from models.base_models import RegisterUserResponse, UserData
from entities.user import User
from enums.roles import Roles


@allure.epic("Тестирование пользователей")
@allure.label("qa_name", "Ivan Petrovich")
@allure.tag("api", "positive")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.regression
@pytest.mark.smoke
class TestUser:
    @allure.feature("Регистрация пользователей")
    @allure.story("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тестирование регистрации нового пользователя через API")
    @pytest.mark.post
    @pytest.mark.critical
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_register_user(
        self, api_manager: APIManager, creation_user_data: UserData
    ) -> None:
        with allure.step("Отправка запроса"):
            register_user_response = RegisterUserResponse(
                **api_manager.auth_api.register_user(
                    user_data=creation_user_data
                ).json()
            )

        with allure.step("Валидация данных"):
            assert register_user_response.email == creation_user_data.email, (
                "Email не совпадает"
            )
            assert (
                register_user_response.get_roles_as_strings()
                == creation_user_data.get_roles_as_strings()
            )
            assert Roles.USER in register_user_response.roles

    @allure.feature("Получение пользователей")
    @allure.story("Получение пользователя по разным идентификаторам")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.get
    @pytest.mark.regression
    def test_get_user_by_locator(
        self, super_admin: User, creation_user_data: UserData
    ) -> None:
        with allure.step("Подготовка данных"):
            user_data_dict = creation_user_data.model_dump(mode="json")
        with allure.step("Отправка запросов"):
            created_user_response = RegisterUserResponse(
                **super_admin.api.user_api.create_user(user_data_dict).json()
            )
            response_by_id = super_admin.api.user_api.get_user(
                created_user_response.id
            ).json()
            response_by_email = super_admin.api.user_api.get_user(
                creation_user_data.email
            ).json()
        with allure.step("Валидация данных"):
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
