from json.decoder import JSONDecodeError
import requests

url = "https://playground.learnqa.ru/api/"


def request_get_text(uri):
    response = requests.get(url + uri)
    print(response.text)
    try:
        parsed_response_text = response.json()
        print(parsed_response_text)
    except JSONDecodeError:
        print('Response is not a JSON object')


def request_get_hello(uri):
    response = requests.get(url + uri, params={'name' : 'User'})
    parsed_response_text = response.json()
    print(parsed_response_text['answer'])


if __name__ == '__main__':
    request_get_text('get_text')
    request_get_hello('hello')

