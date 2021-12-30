import json
import allure
from lib.base_case import BaseCase
from lib.assertion import Assertions
from lib.my_requests import MyRequests


@allure.epic("Edit user cases")
@allure.link("https://271821.selcdn.ru/b-webinars/api_python/v1_938957/lesson4/l4m4-edit_user.mp4")
@allure.testcase("https://software-testing.ru/lms/mod/assign/view.php?id=234826", "Negative cases to check user editing")
class TestUserEdit(BaseCase):
    def setup(self):
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data["email"]
        self.firstName = register_data["firstName"]
        password = register_data["password"]
        self.user_id = self.get_json_value(response, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response_login = MyRequests.post("/user/login", data=login_data)

        self.auth_sid = self.get_cookie(response_login, "auth_sid")
        self.token = self.get_header(response_login, "x-csrf-token")

    @allure.description("Editing just created user using its credentials")
    def test_edit_just_created_user(self):
        # EDIT
        new_name = "New_name"

        response_edit = MyRequests.put(f"/user/{self.user_id}", headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_edit, 200)

        # GET USER
        response_get = MyRequests.get(f"/user/{self.user_id}", headers={"x-csrf-token": self.token},
                                      cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            new_name,
            "Wrong new name after user editing"
        )

    @allure.description("User editing without registration")
    def test_user_edit_unauth_user(self):
        # EDIT
        new_name = "New_name"

        response_edit = MyRequests.put(f"/user/{self.user_id}", data={"firstName": new_name})

        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.content.decode("utf-8") == "Auth token not supplied", \
            f"Actual response error is not equal to the expected. Error: {response_edit.content.decode('utf-8')}"

    @allure.description("User editing with another user")
    def test_user_edit_with_another_auth_user(self):
        # REGISTRATION NEW USER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        # EDIT
        new_name = "New_name"

        response_edit = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_edit, 200)

        # GET USER
        response_get = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": self.token},
                                      cookies={"auth_sid": self.auth_sid})

        Assertions.assert_code_status(response_get, 200)
        Assertions.assert_json_has_not_key(response_get, "firstName")

    @allure.description("Editing user email with invalid email data like 'test123example.com'")
    def test_edit_user_email_with_invalid_email(self):
        new_email = "test123example.com"

        response_edit = MyRequests.put(f"/user/{self.user_id}", headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid}, data={"email": new_email})

        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.content.decode("utf-8") == f"Invalid email format", \
            f"Actual response error is not equal to the expected. Error: {response_edit.content.decode('utf-8')}"

    @allure.description("Editing user first name using short name 1 symbol long")
    def test_edit_user_name_with_short_name(self):
        new_first_name = "V"

        response_edit = MyRequests.put(f"/user/{self.user_id}", headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid}, data={"firstName": new_first_name})

        str_content = response_edit.content.decode("utf-8")
        response_to_json = json.loads(str_content)

        Assertions.assert_code_status(response_edit, 400)
        assert response_to_json["error"] == "Too short value for field firstName", \
            "Unless the field firstName is too short, there is no error"

    @allure.description("Editing user using credentials of the reserved user, user ids '1-5'")
    def test_user_edit_using_another_reserved_auth_user(self):
        # LOGIN WITH DEFAULT USER
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # EDIT
        new_name = "New_name"

        response_edit = MyRequests.put(f"/user/{self.user_id}", headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}, data={"firstName": new_name})

        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.content.decode("utf-8") == f"Please, do not edit test users with ID 1, 2, 3, 4 or 5.",\
            "Success editing unless login with another user"


