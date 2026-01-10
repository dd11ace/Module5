import pytest

from entities.user import User


class TestMoviesNegative:
    def test_create_movie_without_authorization(
        self, common_user: User, test_movie: dict
    ) -> None:
        response = common_user.api.movies_api.create_movie(test_movie, 403).json()

        assert response["message"] == "Forbidden resource"
        assert response["error"] == "Forbidden"
        assert response["statusCode"] == 403

    def test_get_movie_not_found(
        self, super_admin: User, nonexistent_movie_id: int
    ) -> None:
        """Тест получение несуществующего фильма"""
        response_data = super_admin.api.movies_api.get_movie_info(
            movie_id=nonexistent_movie_id, expected_status=404
        ).json()

        assert response_data["message"] == "Фильм не найден"
        assert response_data["error"] == "Not Found"
        assert response_data["statusCode"] == 404

    def test_methods_unauthorized(
        self,
        common_user: User,
        test_movie: dict,
        movie_id: int,
    ) -> None:
        """Тестирование запросов без авторизации"""
        methods = ["create_movie", "delete_movie", "patch_movie"]
        for method in methods:
            if method == "create_movie":
                response = common_user.api.movies_api.create_movie(
                    test_movie, expected_status=401
                )

            elif method == "delete_movie":
                response = common_user.api.movies_api.delete_movie(
                    movie_id, expected_status=401
                )

            elif method == "patch_movie":
                response = common_user.api.movies_api.patch_movie(
                    movie_id, test_movie, expected_status=401
                )

        response_data = response.json()

        assert response_data["message"] == "Forbidden resource"
        assert response_data["error"] == "Forbidden"
        assert response_data["statusCode"] == 403

    def test_create_movie_with_existing_name(
        self,
        existing_movie_name: str,
        super_admin: User,
        test_movie: dict,
    ) -> None:
        """Тест создания фильма с уже существующим в базе именем"""
        test_movie["name"] = existing_movie_name

        response_data = super_admin.api.movies_api.create_movie(
            movie_data=test_movie, expected_status=409
        ).json()

        assert response_data["message"] == "Фильм с таким названием уже существует"
        assert response_data["error"] == "Conflict"
        assert response_data["statusCode"] == 409

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
        test_movie: dict[str : str | int | bool],
    ) -> None:
        """Тестирование создания фильма с путым полем"""
        test_movie[field] = None

        response_data = super_admin.api.movies_api.create_movie(
            test_movie, expected_status=400
        ).json()

        assert response_data["message"] is not None, (
            "Отсутствует сообщение об ошибке в логе ответа"
        )
        assert response_data["error"] == "Bad Request"
        assert response_data["statusCode"] == 400

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
        test_movie: dict[str : str | int | bool],
        field_name: str,
        invalid_value: str | int,
        super_admin: User,
    ) -> None:
        """Тестирование создания фильма с неверными типами данных в полях"""
        test_movie[field_name] = invalid_value

        response_data = super_admin.api.movies_api.create_movie(
            test_movie, expected_status=400
        ).json()

        assert response_data["message"] is not None, (
            "Отсутствует сообщение об ошибке в логе ответа"
        )
        assert response_data["error"] == "Bad Request"
        assert response_data["statusCode"] == 400
