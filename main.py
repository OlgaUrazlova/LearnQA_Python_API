import requests

url = "https://playground.learnqa.ru/api/"


def request_get_text(uri):
    response = requests.get(url + uri)
    print(response.text)


if __name__ == '__main__':
    request_get_text('get_text')

