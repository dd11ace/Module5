import pytest
from entities.user import User
from db_requester.db_helpers import DBHelper
from db_models.movie import MovieDBSchema
from models.movie_models import MovieBase

from utils.data_generator import DataGenerator


class TestDatabaseMovies:
    def test_movie_creation_and_deletion(
        self, super_admin: User, db_helper: DBHelper, test_movie: MovieBase
    ):
        movie_data = test_movie
        movie_before = db_helper.get_movie_by_id(movie_data["id"])

        assert movie_before is None

        created_movie = db_helper.create_test_movie(movie_data)

        movie_after = db_helper.get_movie_by_id(created_movie.id)

        assert movie_after is not None
        assert movie_after.id == movie_data["id"]
        assert movie_after.name == movie_data["name"]
        assert movie_after.price == movie_data["price"]
        assert movie_after.description == movie_data["description"]
        assert movie_after.image_url == movie_data["image_url"]
        assert movie_after.published == movie_data["published"]
        assert movie_after.rating == movie_data["rating"]
        assert movie_after.genre_id == movie_data["genre_id"]
        assert movie_after.created_at == created_movie.created_at

        db_helper.delete_movie(created_movie)
