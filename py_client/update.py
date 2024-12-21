import requests


endpoint = "http://127.0.0.1:8000/api/products/2/"

data = {"title": "Banana two", "price": 25, "content": ""}

response = requests.put(endpoint, json=data)
print(response.json())
