import requests


endpoint = "http://127.0.0.1:8000/api/products/"

data = {"title": "CreateMixin book 2", "price": 20}

response = requests.post(endpoint, json=data)
print(response.json())
