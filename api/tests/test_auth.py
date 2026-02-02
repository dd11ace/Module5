import pytest
import datetime
import allure
from api.api_manager import APIManager
from models.base_models import UserData, RegisterUserResponse
from enums.roles import Roles
from pytest_mock import mocker
from unittest.mock import Mock

from pytest_check import check


class TestAuth:
    """
    def test_register_user_mock(
        self, api_manager: APIManager, test_user: UserData, mocker
    ):
        # Ответ полученный из мок сервиса
        mock_response = RegisterUserResponse(
            id="id",
            email="email@email.com",
            fullName="fullName",
            verified=True,
            banned=False,
            roles=[Roles.SUPER_ADMIN],
            createdAt=str(datetime.datetime.now()),
        )

        # Мокаем метод register_user в auth_api
        mocker.patch.object(
            api_manager.auth_api,  # Объект, который нужно замокать
            "register_user",  # Метод, который нужно замокать
            return_value=mock_response,  # Фиктивный ответ
        )
        # Вызываем метод, который должен быть замокан
        register_user_response = api_manager.auth_api.register_user(test_user)
        # Проверяем, что ответ соответствует ожидаемому
        assert register_user_response.email == mock_response.email, "Email не совпадает"
    """

    def test_check_functions(self):
        check.equal(1 + 1, 2, "Проверка сложения")
        check.not_equal(2 * 2, 5, "Проверка умножения")
        check.is_true(1 == 1, "Проверка истинности")
        check.is_in("hello", "hello world", "Проверка вхождения строки")

    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_register_user_mock(
        self, api_manager: APIManager, test_user: UserData, mocker
    ):
        with allure.step("Мокаем метод register_user в auth_api"):
            mock_response = RegisterUserResponse(  # Фиктивный ответ
                id="id",
                email="email@email.com",
                fullName="fullName",
                verified=True,
                banned=False,
                roles=[Roles.SUPER_ADMIN],
                createdAt=str(datetime.datetime.now()),
            )
            mocker.patch.object(
                api_manager.auth_api,  # Объект, который нужно замокать
                "register_user",  # Метод, который нужно замокать
                return_value=mock_response,  # Фиктивный ответ
            )

        with allure.step("Вызываем мтеод, который должен быть замокан"):
            register_user_response = api_manager.auth_api.register_user(test_user)

        with allure.step("Проверяем, что ответ соответсвует ожидаемому"):
            with allure.step("Проверка поля персональных данных"):
                with check:
                    check.equal(
                        register_user_response.fullName,
                        "INCORRECT_NAME",
                        "НЕСОВПАДЕНИЕ fullName",
                    )
                    check.equal(register_user_response.email, mock_response.email)

            with allure.step("Проверка поля banned"):
                with check("Проверка поля banned"):
                    check.equal(register_user_response.banned, mock_response.banned)
