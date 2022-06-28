# import requests
# import json

# url = 'http://87.247.28.238:8501/api/weights'
# headers = {'Content-type': 'application/json',  # Определение типа данных
#            'Accept': 'text/plain',
#            'Content-Encoding': 'utf-8'}
# data = {"user_info" : [{"username" : "<user login>",
#                        "key" : "<api_key>"},
#                       {}]}  # Если по одному ключу находится несколько словарей, формируем список словарей
# answer = requests.post(url, data=json.dumps(data), headers=headers)
# print(answer)
# response = answer.json()
# print(response)


# AnimalNumber: "KZC154000000",
#     Date: "2019-04-16T13:15:00",
#     Weight: 300.5,
# 	ScalesModel: ""


import requests
import json

url = 'http://87.247.28.238:8501/api/weights'
headers = {'Content-type': 'application/json'}

data = {"AnimalNumber" : "32153165131351",
        "Date" : "2019-07-1T19:51:00",
        "Weight" : "300.5" ,
        "ScalesModel" : "test_1"}  # Если по одному ключу находится несколько словарей, формируем список словарей

answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
