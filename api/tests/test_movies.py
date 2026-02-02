import pytest
import allure
from api.api_manager import APIManager
from entities.user import User
from models.movie_models import MovieBase, MoviesPaginatedResponse, MovieDeleteResponse


@allure.epic("Тестирование позитивных movies api сценариев")
@allure.label("qa_name", "Ivan Petrovich")
@allure.tag("api")
class TestMovies:
    """Класс для позитивных movies api тестов"""

    @allure.feature("Получение данных")
    @allure.story("Получение афиш фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Получение фильмов")
    @allure.description(
        "Получение афиш фильмов с проверкой обязательных полей: count, page, pageSize, pageCount"
    )
    def test_get_movies(self, api_manager: APIManager) -> None:
        """Тестирование получение афиш"""
        with allure.step("Получение данных фильмов"):
            response = api_manager.movies_api.get_movies()
            response.raise_for_status()
            response_data = MoviesPaginatedResponse(**response.json())

        with allure.step("Валидация ответа"):
            fields = ["movies", "count", "page", "pageSize", "pageCount"]

            for field in fields:
                with allure.step(f"Проверка наличия {field} в ответе"):
                    field_value = getattr(response_data, field)

                    assert field_value is not None, f"Поле {field} имеет значение None"

    @allure.feature("Получение данных")
    @allure.story("Получение фильма по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Получение детальной информации о фильме")
    def test_get_movie(self, api_manager: APIManager, movie_id: int) -> None:
        """Тестирование получение фильма по ID"""
        with allure.step("Выполнение запроса GET по movie_id"):
            response = api_manager.movies_api.get_movie_info(movie_id)
            response.raise_for_status()
            response_data = MovieBase(**response.json())

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
                assert field_data is not None, f"Поле {field} имеет значение None"

    @allure.feature("Изменение данных")
    @allure.story("Полное изменение фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Изменение всех полей фильма")
    def test_patch_movie_all_fields(
        self,
        super_admin: User,
        movie_id: int,
        test_movie: MovieBase,
    ) -> None:
        """Тест редактирования фильма"""
        with allure.step("Выполенине запроса PATCH"):
            response = super_admin.api.movies_api.patch_movie(
                movie_id, movie_data=test_movie
            )
            response.raise_for_status()

            response_data = MovieBase(**response.json())

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

                assert response_data.id == movie_id, "ID не сопадают"
                assert expected_value == actual_value, f"Поле {field} не изменилось"

    @allure.feature("Изменение данных")
    @allure.story("Частичное изменение фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Обновление отдельного поля фильма: {field}")
    @pytest.mark.parametrize(
        "field", ["name", "price", "description", "location", "published", "genreId"]
    )
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
            response = super_admin.api.movies_api.patch_movie(movie_id, new_data)
            response.raise_for_status()

            response_data = MovieBase(**response.json())

        with allure.step(f"Валидация поля {field}"):
            expected_value = getattr(test_movie, field)
            actual_value = getattr(response_data, field)

            assert response_data.id == movie_id, "ID не совпадают"
            assert expected_value == actual_value, f"Ошибка: поле {field} не обновилось"

    @allure.feature("Создание данных")
    @allure.story("Создание нового фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание фильма")
    def test_create_movie(
        self,
        test_movie: MovieBase,
        super_admin: User,
    ) -> None:
        """Тестирование создания фильма"""
        with allure.step("Создание фильма через POST метод"):
            response = super_admin.api.movies_api.create_movie(test_movie.model_dump())
            response.raise_for_status()

            response_data = MovieBase(**response.json())

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

                    assert expected_value == actual_value, (
                        f"Поле {field} не совпадает: Ожидалось {expected_value}, получено {actual_value}"
                    )

    @allure.feature("Удаление данных")
    @allure.story("Удаление фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление филмьа по ID")
    def test_delete_movie(
        self,
        super_admin: User,
        movie_id: int,
    ) -> None:
        """Тест на удаление фильма по ID"""
        with allure.step("Отправка запроса DELETE"):
            response = super_admin.api.movies_api.delete_movie(movie_id)
            response.raise_for_status()

            response_data = MovieBase(**response.json())

        with allure.step("Провека что был удален фильм с правильным ID"):
            assert response_data.id == movie_id, "ID фильмов не совпадают"

        with allure.step("Попытка получить данные после удаления"):
            response_after_deletion = super_admin.api.movies_api.get_movie_info(
                movie_id, expected_status=404
            )
            response_after_deletion_data = MovieDeleteResponse(
                **response_after_deletion.json()
            )

        with allure.step("Проверка получения удаленного фильма"):
            assert response_after_deletion_data.message == "Фильм не найден"
            assert response_after_deletion_data.error == "Not Found"
            assert response_after_deletion_data.statusCode == 404
