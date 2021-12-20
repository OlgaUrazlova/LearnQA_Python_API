import requests


class TestHeaderParams:
    def test_header_params(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        assert "x-secret-homework-header" in response.headers, "There is no x-secret-homework-header value" \
                                                               " in the response"
        header_value = response.headers.get("x-secret-homework-header")
        expected_header = "Some secret value"

        assert header_value == expected_header, "Secret header value from the response is not equal to the expected " \
                                                "value"
