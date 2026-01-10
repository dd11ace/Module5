import requests

from .movies_api import MoviesAPI
from .auth_api import AuthAPI
from .user_api import UserApi


class APIManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    def __init__(self, session: requests.Session) -> None:
        """
        Инициализация APIManager.
        :param session: HTTP-сессия, используемая всеми API-классами
        """
        self.session = session

        self.movies_api = MoviesAPI(session)
        self.auth_api = AuthAPI(session)
        self.user_api = UserApi(session)

    def close_session(self):
        self.session.close()
