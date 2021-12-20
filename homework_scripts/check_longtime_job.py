import requests
import time

# Создаем задачу
response_1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
parsed_response_1 = response_1.json()
token = parsed_response_1["token"]
time_wait = parsed_response_1["seconds"]


# Задача еще не готова
response_2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
parsed_response_2 = response_2.json()
if parsed_response_2["status"] == "Job is NOT ready":
    print("Задача еще не готова")
else:
    print(f"Error {parsed_response_2['status']}")
time.sleep(time_wait)


# Задача должна быть готова
response_3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
parsed_response_3 = response_3.json()
if parsed_response_3["status"] == "Job is ready" and parsed_response_3["result"] != None:
    print(f"Задача готова, статус задачи {parsed_response_3['status']} и результат {parsed_response_3['result']}")
else:
    print(f"Ошибка статус задачи {parsed_response_3['status']}")