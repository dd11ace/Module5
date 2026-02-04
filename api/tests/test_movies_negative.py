import pytest
import allure
from entities.user import User
from models.movie_models import MovieBase, APIError


@allure.epic("Тестирование негативных movies api сценариев")
@allure.label("qa_name", "Ivan Petrovich")
@allure.tag("api", "negative")
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
class TestMoviesNegative:
    @allure.feature("Авторизация и доступ")
    @allure.story("Создание фильма без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка создания фильма обычным пользователем")
    @pytest.mark.critical
    @pytest.mark.post
    @pytest.mark.smoke
    def test_create_movie_without_authorization(
        self, common_user: User, test_movie: dict
    ) -> None:
        with allure.step("Выполнение запроса"):
            response_data = APIError(
                **common_user.api.movies_api.create_movie(test_movie, 403).json()
            )
        with allure.step("Валидация данных"):
            assert response_data.message == "Forbidden resource"
            assert response_data.error == "Forbidden"
            assert response_data.statusCode == 403

    @allure.feature("Негативные сценарии")
    @allure.story("Получение несуществующего ресурса")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Получение несуществующего фильма")
    @pytest.mark.get
    @pytest.mark.regression
    def test_get_movie_not_found(
        self, super_admin: User, nonexistent_movie_id: int
    ) -> None:
        """Тест получение несуществующего фильма"""
        with allure.step("Выполнение запроса"):
            response_data = APIError(
                **super_admin.api.movies_api.get_movie_info(
                    movie_id=nonexistent_movie_id, expected_status=404
                ).json()
            )

        with allure.step("Валидация данных"):
            assert response_data.message == "Фильм не найден"
            assert response_data.error == "Not Found"
            assert response_data.statusCode == 404

    @allure.feature("Авторизация и доступ")
    @allure.story("Доступ к API методам без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проверка всех методов API без достаточных прав")
    @pytest.mark.critical
    @pytest.mark.crud
    @pytest.mark.parametrize("method", ["create_movie", "delete_movie", "patch_movie"])
    def test_methods_unauthorized(
        self, common_user: User, test_movie: MovieBase, movie_id: int, method: str
    ) -> None:
        """Тестирование запросов без авторизации"""
        with allure.step("Выполнение запроса"):
            match method:
                case "create_movie":
                    response_data = APIError(
                        **common_user.api.movies_api.create_movie(
                            test_movie, expected_status=401
                        ).json()
                    )
                case "delete_movie":
                    response_data = APIError(
                        **common_user.api.movies_api.delete_movie(
                            movie_id, expected_status=401
                        ).json()
                    )
                case "patch_movie":
                    response_data = APIError(
                        **common_user.api.movies_api.patch_movie(
                            movie_id, test_movie, expected_status=401
                        ).json()
                    )

        with allure.step("Валидация данных"):
            assert response_data.message == "Forbidden resource"
            assert response_data.error == "Forbidden"
            assert response_data.statusCode == 403

    @allure.feature("Негативные сценарии")
    @allure.story("Конфликты данных")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание фильма с существующим названием")
    @pytest.mark.post
    @pytest.mark.regression
    def test_create_movie_with_existing_name(
        self,
        existing_movie_name: str,
        super_admin: User,
        test_movie: MovieBase,
    ) -> None:
        """Тест создания фильма с уже существующим в базе именем"""
        with allure.step("Подготовка данных"):
            test_movie.name = existing_movie_name
        with allure.step("Выполнение запроса"):
            response_data = APIError(
                **super_admin.api.movies_api.create_movie(
                    movie_data=test_movie, expected_status=409
                ).json()
            )
        with allure.step("Валидация данных"):
            assert response_data.message == "Фильм с таким названием уже существует"
            assert response_data.error == "Conflict"
            assert response_data.statusCode == 409

    @allure.feature("Негативные сценарии")
    @allure.story("Валидация обязательных полей")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создания фильма без одного обязательного поля")
    @pytest.mark.validation
    @pytest.mark.parametrized
    @pytest.mark.post
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "field",
        [
            "name",
            "description",
            "price",
            "location",
            "published",
            "genreId",
        ],
    )
    def test_create_movie_without_field(
        self,
        super_admin: User,
        field: str,
        test_movie: MovieBase,
    ) -> None:
        """Тестирование создания фильма с путым полем"""
        with allure.step("Подготовка данных"):
            setattr(test_movie, field, None)
        with allure.step("Выполнение запроса"):
            response_data = APIError(
                **super_admin.api.movies_api.create_movie(
                    test_movie, expected_status=400
                ).json()
            )

        with allure.step("Валидация данных"):
            assert response_data.message is not None, (
                "Отсутствует сообщение об ошибке в логе ответа"
            )
            assert response_data.error == "Bad Request"
            assert response_data.statusCode == 400

    @allure.feature("негативные сценарии")
    @allure.story("Валидация типов данных")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание фильма с неверным типом данных в одном поле")
    @pytest.mark.validation
    @pytest.mark.post
    @pytest.mark.regression
    @pytest.mark.parametrized
    @pytest.mark.parametrize(
        ("field_name", "invalid_value"),
        [
            ("name", 123),
            ("description", 123),
            ("price", "123"),
            ("location", 123),
            ("location", "string"),
            ("published", "True"),
            ("genreId", "1"),
        ],
    )
    def test_create_movie_with_invalid_data_types(
        self,
        test_movie: MovieBase,
        field_name: str,
        invalid_value: str | int,
        super_admin: User,
    ) -> None:
        """Тестирование создания фильма с неверными типами данных в полях"""
        with allure.step("Подготовка данных"):
            movie_data = test_movie.model_dump()
            movie_data[field_name] = invalid_value
        with allure.step("Выполнение запроса"):
            response_data = APIError(
                **super_admin.api.movies_api.create_movie(
                    movie_data, expected_status=400
                ).json()
            )
        with allure.step("Валидация данных"):
            assert response_data.message is not None, (
                "Отсутствует сообщение об ошибке в логе ответа"
            )
            assert response_data.error == "Bad Request"
            assert response_data.statusCode == 400
