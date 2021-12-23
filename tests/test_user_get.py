import requests
import pytest
from lib.base_case import BaseCase
from lib.assertion import Assertions


class TestUserGet(BaseCase):
    def test_get_not_authorized_user(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_1, "user_id")

        response_2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(response_2, expected_fields)

    def test_get_user_details_auth_as_different_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")

        response_2 = requests.get(
            f"https://playground.learnqa.ru/api/user/1",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response_2, "username")
        Assertions.assert_json_has_not_key(response_2, "email")
        Assertions.assert_json_has_not_key(response_2, "firstName")
        Assertions.assert_json_has_not_key(response_2, "lastName")

