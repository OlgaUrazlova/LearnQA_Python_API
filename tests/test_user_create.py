import pytest
from lib.base_case import BaseCase
from lib.assertion import Assertions
from lib.my_requests import MyRequests


class TestUserCreate(BaseCase):
    test_data = [
        (None, "learn_qa", "learn_qa", "learn_qa", "learnqatest1@example.com", "password"),
        ("123", None, "learn_qa", "learn_qa", "learnqatest1@example.com", "username"),
        ("123", "learn_qa", None, "learn_qa", "learnqatest1@example.com", "firstName"),
        ("123", "learn_qa", "learn_qa", None, "learnqatest1@example.com", "lastName"),
        ("123", "learn_qa", "learn_qa", "learn_qa", None, "email")
    ]

    def test_create_user_success(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_exiting_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content " \
                                                                      f"{response.content}"

    def test_create_user_with_invalid_email(self):
        invalid_email = "test123eaxample.com"
        data = self.prepare_registration_data(invalid_email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Email format is incorrect. " \
                                                                            f"Email: {invalid_email}"

    @pytest.mark.parametrize("password, username, firstName, lastName, email, missed_value", test_data)
    def test_create_user_without_required_params(self, password, username, firstName, lastName, email, missed_value):
        data = {
            "password": password,
            "username": username,
            "firstName": firstName,
            "lastName": lastName,
            "email": email
        }
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missed_value}", \
            f"The response is successful unless the missing required field {missed_value}"

    def test_create_user_with_short_name(self):
        short_name = "V"
        data = self.prepare_registration_data(username=short_name)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"The response is successful unless username is too short {data['username']}"

    def test_create_user_with_long_name(self):
        long_username = "V" * 251
        data = self.prepare_registration_data(username=long_username)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"The response is successful unless username is too long {data['username']}"





