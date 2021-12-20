import requests


class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)

        assert "HomeWork" in response.cookies, "There is no HomeWork cookie in the response"

        cookie_value = response.cookies.get("HomeWork")
        expected_cookie = "hw_value"

        assert cookie_value == expected_cookie, "Cookie from the response is not equal to the expected cookie"
