import requests

from custom_requester.custom_requester import CustomRequester
from constants import AUTH_URL, USER_ENDPOINT


class UserApi(CustomRequester):
    def __init__(self, session: requests.Session) -> None:
        super().__init__(session, base_url=AUTH_URL)
        self.session = session

    def get_user(self, user_locator: str) -> requests.Response:
        return self.send_request(
            method="GET", endpoint=f"{USER_ENDPOINT}/{user_locator}"
        )

    def create_user(
        self, user_data: dict, expected_status: int = 201
    ) -> requests.Response:
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data,
            expected_status=expected_status,
        )
