import requests
from getpass import getpass

# authenticate first
auth_endpoint = "http://127.0.0.1:8000/api/auth/"

# username = input('What is your username?\n')
# password = getpass('What is your password? \n')

username = 'jayanti.pesa'
password = '123'

auth_response = requests.post(auth_endpoint, json={
    'username': username, 'password': password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        'Authorization': f'bearer {token}'
    }

    endpoint = "http://127.0.0.1:8000/api/products/"
    response = requests.get(endpoint, headers=headers)
    print(response.json())
