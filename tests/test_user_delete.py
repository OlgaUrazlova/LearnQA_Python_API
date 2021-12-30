import allure
from lib.assertion import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Delete user cases")
@allure.testcase("https://software-testing.ru/lms/mod/assign/view.php?id=234827", "Negative and positive cases to check"
                                                                                  "user deleting")
class TestUserDelete(BaseCase):
    @allure.description("Check if it's possible to delete reserved user")
    def test_delete_reserved_user(self):
        with allure.step("Login with the default user with ids '0-5'"):
            login_data = {
                "email": "vinkotov@example.com",
                "password": "1234"
            }

            response_login = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response_login, "auth_sid")
            token = self.get_header(response_login, "x-csrf-token")

        with allure.step("Delete user '2'"):
            response_delete = MyRequests.delete("/user/2", headers={"x-csrf-token": token},
                                                cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response_delete, 400)
            assert response_delete.content.decode("utf-8") == \
                   "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
                f"Actual error '{response_delete.content.decode('utf-8')}' is not equal to the expected"

    @allure.description("Check user deleting after its creating")
    def test_delete_auth_user(self):
        with allure.step("New user creating"):
            register_data = self.prepare_registration_data()
            response = MyRequests.post("/user/", data=register_data)
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

            email = register_data["email"]
            password = register_data["password"]
            user_id = self.get_json_value(response, "id")

        with allure.step("Login with new user"):
            login_data = {
                "email": email,
                "password": password
            }

            response_login = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response_login, "auth_sid")
            token = self.get_header(response_login, "x-csrf-token")

        with allure.step("Delete new user using authorization of this user"):
            response_delete = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token},
                                                cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response_delete, 200)

        with allure.step("Get info about the delete user"):
            response_check = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid})

            Assertions.assert_code_status(response_check, 404)
            assert response_check.content.decode("utf-8") == "User not found", \
                f"Actual error '{response_check.content.decode('utf-8')}' text is not equal to the expected"

    @allure.description("Check user deleting using another user")
    def test_delete_user_using_another_auth_user(self):
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id_1 = self.get_json_value(response, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # REGISTRATION ANOTHER USER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id_2 = self.get_json_value(response, "id")

        # DELETE
        response_delete = MyRequests.delete(f"/user/{user_id_2}", headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_delete, 200)

        # CHECK DELETED USER
        response_check = MyRequests.get(f"/user/{user_id_2}", headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response_check, 200)
        Assertions.assert_json_has_key(response_check, "username")
