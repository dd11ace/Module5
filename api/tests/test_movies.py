import pytest
from api.api_manager import APIManager
from entities.user import User


class TestMovies:
    """Класс для позитивных movies api тестов"""

    def test_get_movies(self, api_manager: APIManager) -> None:
        """Тестирование получение афиш"""
        response_data = api_manager.movies_api.get_movies().json()

        assert response_data["count"] is not None, "В ответе отсутсвует count"
        assert response_data["page"] is not None, "В ответе отсутсвует page"
        assert response_data["pageSize"] is not None, "В ответе отсутсвует pageSize"
        assert response_data["pageCount"] is not None, "В ответе отсутсвует pageCount"

    def test_get_movie(self, api_manager: APIManager, movie_id: int) -> None:
        """Тестирование получение фильма по ID"""
        response_data = api_manager.movies_api.get_movie_info(movie_id).json()

        assert response_data["id"] == movie_id, "ID фильмов не совпадают"

    def test_patch_movie_all_fields(
        self,
        super_admin: User,
        movie_id: int,
        test_movie: dict,
    ) -> None:
        """Тест редактирования фильма"""
        response_data = super_admin.api.movies_api.patch_movie(
            movie_id, movie_data=test_movie
        ).json()

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

        response_data = super_admin.api.movies_api.patch_movie(
            movie_id, new_data
        ).json()

        assert response_data["id"] == movie_id, "ID не совпадают"
        assert response_data[field] == test_movie[field], (
            f"Ошибка: поле {field} не обновилось"
        )

    def test_create_movie(
        self,
        test_movie: dict[str : str | int | bool,],
        super_admin: User,
    ) -> None:
        """Тестирование создания фильма"""

        response_data = super_admin.api.movies_api.create_movie(test_movie).json()

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

    def test_delete_movie(
        self,
        super_admin: User,
        movie_id: int,
    ) -> None:
        """Тест на удаление фильма по ID"""
        response_data = super_admin.api.movies_api.delete_movie(movie_id).json()

        assert response_data["id"] == movie_id, "ID фильмов не совпадают"
