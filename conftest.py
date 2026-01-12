import pytest
import requests


from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants import BASE_URL, REGISTER_ENDPOINT
from enums.roles import Roles
from models.base_models import UserData

from api.api_manager import APIManager

from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper


@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture()
def db_helper(db_session) -> DBHelper:
    """Фикстура для экземпляра хелпера"""
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture()
def created_test_user(db_helper: DBHelper):
    """
    Фикстура, которая создает тестового пользователя в БД и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


@pytest.fixture()
def created_movie(db_helper: DBHelper):
    """Фикстура, которая создает тестовый фильм в БД и удаляет его после завершения теста"""
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    yield movie
    # Cleanup после теста
    if db_helper.get_movie_by_id(movie.id):
        db_helper.delete_movie(movie)


@pytest.fixture(name="test_user")
def test_user_data() -> UserData:
    """Генерация случайного пользователя для тестов."""
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return UserData(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER],
    )


@pytest.fixture(name="test_movie")
def test_movie_data() -> dict:
    """Fixture с данными для создания фильма"""
    movie_data = DataGenerator.generate_random_movie_data()

    return movie_data


@pytest.fixture()
def registered_user(requester: CustomRequester, test_user: UserData) -> UserData:
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST", endpoint=REGISTER_ENDPOINT, data=test_user, expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.model_copy()
    registered_user.id = response_data.id
    return registered_user


@pytest.fixture(scope="session")
def requester() -> CustomRequester:
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def session() -> requests.Session:
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session) -> APIManager:
    return APIManager(session)


@pytest.fixture
def user_session() -> APIManager:
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = APIManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture()
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, "[SUPER_ADMIN]", new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture()
def movie_id(super_admin: User, test_movie: dict) -> int:
    """Случайный существующий id фильма"""
    new_movie_id = super_admin.api.movies_api.create_movie(test_movie).json()["id"]
    yield new_movie_id
    super_admin.api.movies_api.delete_movie(new_movie_id)


@pytest.fixture()
def nonexistent_movie_id(super_admin: User, test_movie: dict) -> int:
    """Случайный несуществующий id фильма для негативных тестов"""
    new_movie_id = super_admin.api.movies_api.create_movie(test_movie).json()["id"]
    super_admin.api.movies_api.delete_movie(new_movie_id)
    yield new_movie_id


@pytest.fixture()
def existing_movie_name(super_admin: User, test_movie: dict) -> str:
    """Генерация случайного существующего названия фильма"""
    new_movie = super_admin.api.movies_api.create_movie(test_movie).json()
    yield new_movie["name"]
    super_admin.api.movies_api.delete_movie(new_movie["id"])


@pytest.fixture
def creation_user_data(test_user: UserData) -> UserData:
    data = test_user.model_dump()
    data.update(
        {
            "verified": True,
            "banned": False,
        }
    )

    return UserData.model_construct(**data)


@pytest.fixture
def common_user(
    user_session: APIManager, super_admin: User, creation_user_data: UserData
) -> APIManager:
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        creation_user_data.roles,
        new_session,
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin_user(
    user_session: APIManager, super_admin: User, creation_user_data: UserData
) -> User:
    new_session = user_session()

    admin_user = User(
        creation_user_data.email,
        creation_user_data.password,
        creation_user_data.roles,
        new_session,
    )

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(creation_user_data)

    return admin_user
