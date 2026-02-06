import pytest
import allure
from pytest_check import check_functions as check
from db_requester.db_helpers import DBHelper
from utils.data_generator import DataGenerator


@allure.epic("Тест базы данных")
@allure.feature("Тестирование базы данных фильмов")
@allure.label("qa_name", "Ivan Petrovich")
@allure.tag("database", "positive")
@pytest.mark.database
@pytest.mark.crud
class TestDatabaseMovies:
    @allure.feature("Операции CRUD в базе данных")
    @allure.story("Создание и удаление фильма")
    @allure.title("Создание и удаление фильма в базе данных")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.database
    @pytest.mark.crud
    @pytest.mark.critical
    @pytest.mark.smoke
    def test_movie_creation_and_deletion(
        self,
        db_helper: DBHelper,
    ):
        movie_data = DataGenerator.generate_movie_data()
        with allure.step("Проверка, что фильма нет в базе перед созданием"):
            movie_before = db_helper.get_movie_by_id(movie_data["id"])

            check.is_none(movie_before)
        with allure.step("Создание фильма в базе данных"):
            created_movie = db_helper.create_test_movie(movie_data)
        with allure.step("Получение созданного фильма по ID"):
            movie_after = db_helper.get_movie_by_id(created_movie.id)
        with allure.step("Валидация данных созданного фильма"):
            check.is_not_none(movie_after)
            check.equal(movie_after.id, movie_data["id"])
            check.equal(movie_after.name, movie_data["name"])
            check.equal(movie_after.price, movie_data["price"])
            check.equal(movie_after.description, movie_data["description"])
            check.equal(movie_after.image_url, movie_data["image_url"])
            check.equal(movie_after.published, movie_data["published"])
            check.equal(movie_after.rating, movie_data["rating"])
            check.equal(movie_after.genre_id, movie_data["genre_id"])
            check.equal(movie_after.created_at, created_movie.created_at)
        with allure.step("Удаление фильма из базы данных"):
            db_helper.delete_movie(created_movie)
