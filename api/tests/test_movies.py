import pytest
import allure
from api.api_manager import APIManager
from entities.user import User


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
        with allure.step("Получение афиш фильмов"):
            response_data = api_manager.movies_api.get_movies().json()

        with allure.step("Валидация ответа"):
            fields = ["count", "page", "pageSize", "pageCount"]

            for field in fields:
                with allure.step(f"Проверка наличия {field} в ответе"):
                    assert field in response_data, f"Поле {field} отстуствует в ответе"
                    assert response_data[field] is not None

    @allure.feature("Получение данных")
    @allure.story("Получение фильма по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Получение детальной информации о фильме")
    def test_get_movie(self, api_manager: APIManager, movie_id: int) -> None:
        """Тестирование получение фильма по ID"""
        with allure.step("Выполнение запроса GET по movie_id"):
            response_data = api_manager.movies_api.get_movie_info(movie_id).json()

        with allure.step("Валидация ID"):
            assert response_data["id"] == movie_id, "ID фильмов не совпадают"

    @allure.feature("Изменение данных")
    @allure.story("Полное изменение фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Изменение всех полей фильма")
    def test_patch_movie_all_fields(
        self,
        super_admin: User,
        movie_id: int,
        test_movie: dict,
    ) -> None:
        """Тест редактирования фильма"""
        with allure.step("Выполенине запроса PATCH"):
            response_data = super_admin.api.movies_api.patch_movie(
                movie_id, movie_data=test_movie
            ).json()

        with allure.step("Валидация изменений"):
            assert response_data["id"] == movie_id, "ID не совпадают"
            assert response_data["name"] == test_movie["name"], (
                "Названия фильмов не совпадают"
            )
            assert response_data["price"] == test_movie["price"], "Цены не совпадают"
            assert response_data["description"] == test_movie["description"], (
                "Описание не совпадает"
            )
            assert response_data["location"] == test_movie["location"], (
                "Локация не совпадает"
            )
            assert response_data["published"] == test_movie["published"], (
                "Статус published не совпадает"
            )
            assert response_data["genreId"] == test_movie["genreId"], (
                "ID жанра не совпадает"
            )

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
        test_movie: dict,
    ) -> None:
        new_data = {field: test_movie[field]}

        with allure.step(f"Выполнение PATCH запроса для поля {field}"):
            response_data = super_admin.api.movies_api.patch_movie(
                movie_id, new_data
            ).json()

        with allure.step(f"Валидация поля {field}"):
            assert response_data["id"] == movie_id, "ID не совпадают"
            assert response_data[field] == test_movie[field], (
                f"Ошибка: поле {field} не обновилось"
            )

    @allure.feature("Создание данных")
    @allure.story("Создание нового фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание фильма")
    def test_create_movie(
        self,
        test_movie: dict[str : str | int | bool,],
        super_admin: User,
    ) -> None:
        """Тестирование создания фильма"""
        with allure.step("Создание фильма через POST метод"):
            response_data = super_admin.api.movies_api.create_movie(test_movie).json()

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
                    assert response_data[field] == test_movie[field], (
                        f"Поле {field} не совпадает"
                    )

    @allure.feature("Удаление данных")
    @allure.story("Удаление фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление филмьа по ID")
    @allure.description("""
    Проверка удаления фильма.
    После удаления проверка невозможности получение данных по ID
    """)
    def test_delete_movie(
        self,
        super_admin: User,
        movie_id: int,
    ) -> None:
        """Тест на удаление фильма по ID"""
        with allure.step("Отправка запроса DELETE"):
            response_data = super_admin.api.movies_api.delete_movie(movie_id).json()

        with allure.step("Провека что был удален фильм с правильным ID"):
            assert response_data["id"] == movie_id, "ID фильмов не совпадают"

        with allure.step("Проверка отсутствия фильма после удаления"):
            super_admin.api.movies_api.get_movie_info(movie_id, expected_status=404)
