from fastapi.testclient import TestClient

from main import app
import pytest
from datetime import date, timedelta

client = TestClient(app)


# example

def test_hello_name():
    name = 'Kamila'
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"msg": f"Hello {name}"}


def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "1"
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "2"
    # 3rd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "3"


# task 1.1

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


# task 1.2

def test_method():
    response = client.get(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

    response = client.delete(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}

    response = client.put(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}

    response = client.options(f"/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}

    response = client.post(f"/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}


# task 1.3

def test_auth():
    response = client.get(f"/auth")
    assert response.status_code == 401

    response = client.get("/auth?password=''")
    assert response.status_code == 401

    response = client.get(
        "/auth?password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 401

    response = client.get(
        "/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 204

    response = client.get(
        "/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == 401

    response = client.get(
        "/auth?password=password123&password_hash=w9skdf4b3ae1e2csf92e2vabb60dc0412651c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == 401


# task 1.4

def test_register():
    patient = {'name': 'Adam', 'surname': 'Kowalski'}
    response = client.post(f'/register', json=patient)
    assert response.status_code == 201
    assert response.json() == {"id": 1,
                               "name": "Adam",
                               "surname": "Kowalski",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(days=12)).strftime("%Y-%m-%d")}

    patient = {'name': 'Alojzy', 'surname': 'Niezdąży'}
    response = client.post(f'/register', json=patient)
    assert response.status_code == 201


# task 1.5

def test_get_patient():

    response = client.get("/patient/1")
    assert response.json() == {"id": 1,
                               "name": "Adam",
                               "surname": "Kowalski",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(days=12)).strftime("%Y-%m-%d")}
    assert response.status_code == 200

    response = client.get("/patient/0")
    assert response.status_code == 400

    response = client.get("/patient/10")
    assert response.status_code == 404
