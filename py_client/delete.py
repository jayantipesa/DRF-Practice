import requests

product_id = input("Enter the product id you want to delete.\n")

try:
    product_id = int(product_id)
except ValueError:
    product_id = None
    print(f'{product_id} is not valid.')

if product_id:
    endpoint = f"http://127.0.0.1:8000/api/products/{product_id}/"

    response = requests.delete(endpoint)
    print(response.status_code, response.status_code == 204)
