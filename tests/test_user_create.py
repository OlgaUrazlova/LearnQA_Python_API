import requests
import pytest
from lib.base_case import BaseCase
from lib.assertion import Assertions
from datetime import datetime


class TestUserCreate(BaseCase):
    test_data = [
        (None, "learn_qa", "learn_qa", "learn_qa", "learnqatest1@example.com", "password"),
        ("123", None, "learn_qa", "learn_qa", "learnqatest1@example.com", "username"),
        ("123", "learn_qa", None, "learn_qa", "learnqatest1@example.com", "firstName"),
        ("123", "learn_qa", "learn_qa", None, "learnqatest1@example.com", "lastName"),
        ("123", "learn_qa", "learn_qa", "learn_qa", None, "email")
    ]

    def setup(self):
        base_part = "learnqa"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S%")
        domain = "example.com"
        self.email = f"{base_part}{random_part}@{domain}"
        self.invalid_email = f"{base_part}{random_part}{domain}"

    def test_create_user_success(self):
        data = {
            "password": "123",
            "username": "learn_qa",
            "firstName": "learn_qa",
            "lastName": "learn_qa",
            "email": self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_exiting_email(self):
        email = "vinkotov@example.com"
        data = {
            "password": "123",
            "username": "learn_qa",
            "firstName": "learn_qa",
            "lastName": "learn_qa",
            "email": email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content " \
                                                                      f"{response.content}"

    def test_create_user_with_invalid_email(self):
        data = {
            "password": "123",
            "username": "learn_qa",
            "firstName": "learn_qa",
            "lastName": "learn_qa",
            "email": self.invalid_email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Email format is incorrect. " \
                                                                            f"Email: {self.invalid_email}"

    @pytest.mark.parametrize("password, username, firstName, lastName, email, missed_value", test_data)
    def test_create_user_without_required_params(self, password, username, firstName, lastName, email, missed_value):
        data = {
            "password": password,
            "username": username,
            "firstName": firstName,
            "lastName": lastName,
            "email": email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missed_value}", \
            f"The response is successful unless the missing required field {missed_value}"

    def test_create_user_with_short_name(self):
        data = {
            "password": "123",
            "username": "V",
            "firstName": "learn_qa",
            "lastName": "learn_qa",
            "email": self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"The response is successful unless username is too short {data['username']}"

    def test_create_user_with_long_name(self):
        long_username = "V" * 251
        data = {
            "password": "123",
            "username": long_username,
            "firstName": "learn_qa",
            "lastName": "learn_qa",
            "email": self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"The response is successful unless username is too long {data['username']}"





