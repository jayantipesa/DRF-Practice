import requests

endpoint = "https://httpbin.org/status/200/"
endpoint = "https://httpbin.org/anything"
endpoint = "http://127.0.0.1:8000/api/"

response = requests.post(endpoint, json={"title": "Test book"})
# print('reponse: ', response.headers)
print('text: ', response.text)
# print(response.json())
