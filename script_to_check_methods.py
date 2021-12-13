import requests

# Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.status_code)
print(response.text)


# Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", headers={"method": "HEAD"})
print(response.text)
print(response.status_code)


# Делает запрос с правильным значением method. Описать что будет выводиться в этом случае
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response.text)
print(response.status_code)


# С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method
methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"]

print("_" * 10 + "GET" + "_" * 10)
for i in range(len(methods)):
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": methods[i]})
    if methods[i] == "GET":
        print(methods[i])
        print(response.text)
    else:
        print(methods[i])
        print(response.text)


print("_" * 10 + "PUT" + "_" * 10)
for i in range(len(methods)):
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": methods[i]})
    if methods[i] == "PUT":
        print(methods[i])
        print(response.text)
    else:
        print(methods[i])
        print(response.text)


print("_" * 10 + "PATCH" + "_" * 10)
for i in range(len(methods)):
    response = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": methods[i]})
    if methods[i] == "PATCH":
        print(methods[i])
        print(response.text)
    else:
        print(methods[i])
        print(response.text)


print("_" * 10 + "DELETE" + "_" * 10)
for i in range(len(methods)):
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", headers={"method": methods[i]})
    if methods[i] == "DELETE":
        print(methods[i])
        print(response.text)
    else:
        print(methods[i])
        print(response.text)


print("_" * 10 + "HEAD" + "_" * 10)
for i in range(len(methods)):
    response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", headers={"method": methods[i]})
    if methods[i] == "HEAD":
        print(methods[i])
        print(response.text)
    else:
        print(methods[i])
        print(response.text)


