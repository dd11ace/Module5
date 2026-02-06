from api.api_manager import APIManager


class User:
    def __init__(self, email: str, password: str, roles: list, api: APIManager) -> None:
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self) -> tuple:
        """Возвращает кортеж (email, password)"""
        return self.email, self.password
