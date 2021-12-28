import requests


class MyRequests():
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, 'PUT')

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, 'GET')

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"https://playground.learnqa.ru/api{url}"

        if headers is None:
            headers = {}
        elif cookies is None:
            cookies = {}

        if method == "GET":
            response = requests.get(url, headers=headers, cookies=cookies, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, cookies=cookies, data=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, cookies=cookies, data=data)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        return response