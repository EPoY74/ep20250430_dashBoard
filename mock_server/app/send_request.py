"""
посылаю информацию по адресу
"""


import httpx

data={
  "name": "Камера",
  "description": "IP-видеокамера",
  "price": 199.99,
  "in_stock": True
}
ENDPOINT = "http://127.0.0.1:8000/items/"

response = httpx.post(ENDPOINT, json=data)
print(response.json()) #noqa
