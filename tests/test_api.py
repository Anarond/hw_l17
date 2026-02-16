import json
import os
import pytest
import requests
from jsonschema import validate


def load_schema(filename):
    current = os.path.dirname(__file__)
    parent = os.path.dirname(current)
    path = os.path.join(parent, "schemas", filename)
    with open(path) as file:
        return json.load(file)


def test_get_all_products():
    response = requests.get("https://fakestoreapi.com/products")
    assert response.status_code == 200
    schema = load_schema("get_all_products.json")
    validate(instance=response.json(), schema=schema)

def test_delete_product():
    response = requests.delete("https://fakestoreapi.com/products/1")
    assert response.status_code == 200
    schema = load_schema("delete_product.json")
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
    schema = load_schema("delete_product.json")
    validate(instance=response.json(), schema=schema)

def test_user_add():
    response = requests.post("https://fakestoreapi.com/users")
    assert response.status_code == 201
    schema = load_schema("user_add.json")
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
        schema = load_schema("user_login.json")
        validate(instance=response.json(), schema=schema)
    else:
        assert response.text == "username or password is incorrect"
