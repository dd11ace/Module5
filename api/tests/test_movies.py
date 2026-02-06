import pytest
import allure
from pytest_check import check_functions as check
from api.api_manager import APIManager
from entities.user import User
from models.movie_models import MovieBase, MoviesPaginatedResponse, APIError


@allure.epic("Тестирование позитивных movies api сценариев")
@allure.label("qa_name", "Ivan Petrovich")
@allure.tag("api", "positive")
@pytest.mark.api
@pytest.mark.positive
class TestMovies:
    """Класс для позитивных movies api тестов"""

    @allure.feature("Получение данных")
    @allure.story("Получение афиш фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Получение фильмов")
    @allure.description(
        "Получение афиш фильмов с проверкой обязательных полей: count, page, pageSize, pageCount"
    )
    @pytest.mark.critical
    @pytest.mark.get
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_get_movies(self, api_manager: APIManager) -> None:
        """Тестирование получение афиш"""
        with allure.step("Получение данных фильмов"):
            response_data = MoviesPaginatedResponse(
                **api_manager.movies_api.get_movies().json()
            )

        with allure.step("Валидация ответа"):
            fields = ["movies", "count", "page", "pageSize", "pageCount"]

            for field in fields:
                with allure.step(f"Проверка наличия {field} в ответе"):
                    field_value = getattr(response_data, field)

                    check.is_not_none(field_value, f"Поле {field} имеет значение None")

    @allure.feature("Получение данных")
    @allure.story("Получение фильма по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Получение детальной информации о фильме")
    @pytest.mark.get
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_get_movie(self, api_manager: APIManager, movie_id: int) -> None:
        """Тестирование получение фильма по ID"""
        with allure.step("Выполнение запроса GET по movie_id"):
            response_data = MovieBase(
                **api_manager.movies_api.get_movie_info(movie_id).json()
            )

        with allure.step("Валидация ID"):
            assert response_data.id == movie_id, "ID не совпадают"

        with allure.step("Валидация полей"):
            fields = [
                "id",
                "name",
                "imageUrl",
                "price",
                "description",
                "location",
                "published",
                "genreId",
                "rating",
                "createdAt",
            ]
            for field in fields:
                field_data = getattr(response_data, field)

                check.is_not_none(field_data, f"Поле {field} имеет значение None")

    @allure.feature("Изменение данных")
    @allure.story("Полное изменение фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Изменение всех полей фильма")
    @pytest.mark.patch
    @pytest.mark.crud
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_patch_movie_all_fields(
        self,
        super_admin: User,
        movie_id: int,
        test_movie: MovieBase,
    ) -> None:
        """Тест редактирования фильма"""
        with allure.step("Выполенине запроса PATCH"):
            response_data = MovieBase(
                **super_admin.api.movies_api.patch_movie(movie_id, test_movie).json()
            )

        with allure.step("Валидация изменений"):
            fields = [
                "name",
                "price",
                "description",
                "location",
                "published",
                "genreId",
            ]

            for field in fields:
                expected_value = getattr(test_movie, field)
                actual_value = getattr(response_data, field)

                check.equal(response_data.id, movie_id, "ID не сопадают")
                check.equal(expected_value, actual_value, f"Поле {field} не изменилось")

    @allure.feature("Изменение данных")
    @allure.story("Частичное изменение фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Обновление отдельного поля фильма: {field}")
    @pytest.mark.parametrize(
        "field", ["name", "price", "description", "location", "published", "genreId"]
    )
    @pytest.mark.patch
    @pytest.mark.crud
    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.parametrized
    def test_patch_movie_single_field(
        self,
        field: str,
        super_admin: User,
        movie_id: int,
        test_movie: MovieBase,
    ) -> None:
        with allure.step(f"Подготовка данных для обновления поля {field}"):
            update_value = getattr(test_movie, field)

            new_data = {field: update_value}

        with allure.step(f"Выполнение PATCH запроса для поля {field}"):
            response_data = MovieBase(
                **super_admin.api.movies_api.patch_movie(movie_id, new_data).json()
            )
        with allure.step(f"Валидация поля {field}"):
            expected_value = getattr(test_movie, field)
            actual_value = getattr(response_data, field)

            check.equal(response_data.id, movie_id, "ID не совпадают")
            check.equal(
                expected_value, actual_value, f"Ошибка: поле {field} не обновилось"
            )

    @allure.feature("Создание данных")
    @allure.story("Создание нового фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание фильма")
    @pytest.mark.post
    @pytest.mark.crud
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.critical
    def test_create_movie(
        self,
        test_movie: MovieBase,
        super_admin: User,
    ) -> None:
        """Тестирование создания фильма"""
        with allure.step("Создание фильма через POST метод"):
            response_data = MovieBase(
                **super_admin.api.movies_api.create_movie(test_movie).json()
            )

        with allure.step("Валидация ответа"):
            fields = [
                "name",
                "price",
                "description",
                "location",
                "published",
                "genreId",
            ]

            for field in fields:
                with allure.step(f"Проверка данных в поле {field}"):
                    expected_value = getattr(test_movie, field)
                    actual_value = getattr(response_data, field)

                    check.equal(
                        expected_value,
                        actual_value,
                        f"Поле {field} не совпадает: Ожидалось {expected_value}, получено {actual_value}",
                    )

    @allure.feature("Удаление данных")
    @allure.story("Удаление фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление филмьа по ID")
    @pytest.mark.delete
    @pytest.mark.crud
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.regression
    def test_delete_movie(
        self,
        super_admin: User,
        movie_id: int,
    ) -> None:
        """Тест на удаление фильма по ID"""
        with allure.step("Отправка запроса DELETE"):
            response_data = MovieBase(
                **super_admin.api.movies_api.delete_movie(movie_id).json()
            )

        with allure.step("Провека что был удален фильм с правильным ID"):
            assert response_data.id == movie_id, "ID фильмов не совпадают"

        with allure.step("Попытка получить данные после удаления"):
            response_after_deletion = super_admin.api.movies_api.get_movie_info(
                movie_id, expected_status=404
            )
            response_after_deletion_data = APIError(**response_after_deletion.json())

        with allure.step("Проверка получения удаленного фильма"):
            check.equal(response_after_deletion_data.message, "Фильм не найден")
            check.equal(response_after_deletion_data.error, "Not Found")
            check.equal(response_after_deletion_data.statusCode, 404)
