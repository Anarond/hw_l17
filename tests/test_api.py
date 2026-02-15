import json
import pytest
import requests
from jsonschema import validate


#
# url = "https://fakestoreapi.com/products"
#
# payload = {}
#
# response = requests.request("GET", url, data=payload)


def test_get_all_products():
    response = requests.get("https://fakestoreapi.com/products")
    assert response.status_code == 200
    with open("schemas/get_all_products.json") as file:
        schema = json.load(file)

    validate(instance=response.json(), schema=schema)

def test_delete_product():
    response = requests.delete("https://fakestoreapi.com/products/1")
    assert response.status_code == 200
    with open("schemas/delete_product.json") as file:
        schema = json.load(file)

    validate(instance=response.json(), schema=schema)

def test_update_product():
    data = {
"id": 0,
"price": 0.1,
"description": "string",
"image": "http://example.com"
}
    response = requests.put("https://fakestoreapi.com/products/1", json=data)
    assert response.status_code == 200
    with open("schemas/delete_product.json") as file:
        schema = json.load(file)

    validate(instance=response.json(), schema=schema)

def test_user_add():
    response = requests.post("https://fakestoreapi.com/users")
    assert response.status_code == 201
    with open("schemas/user_add.json") as file:
        schema = json.load(file)

    validate(instance=response.json(), schema=schema)

@pytest.mark.parametrize("username, password, status, get_json", [
    ("johnd", "m38rmF$", 201, True),
    ("johnd", "dadadada", 401, False),
])

def test_user_login(username, password, status, get_json):
    data = {"username": username, "password": password}
    response = requests.post("https://fakestoreapi.com/auth/login", json=data)
    assert response.status_code == status
    if get_json:
        with open("schemas/user_login.json",) as file:
            schema = json.load(file)
        validate(instance=response.json(), schema=schema)
    else:
        assert response.text == "username or password is incorrect"

