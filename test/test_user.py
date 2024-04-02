from test import client
import pytest

def test_get_user(client):
    response0 = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    access_token = response0.json["token"]
    headers = { 'Authorization': 'Bearer {}'.format(access_token) }    
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 200
    assert response.json['name'] == 'Test'

def test_create_user(client):
    response = client.post("/users/", json={
            'name': 'Hans Meier', 'email': 'hans.maier@google.ch', 'password': '12345'
        })
    assert response.status_code == 201

def test_login_user_positiv(client):
    response = client.post("/users/login", json={
            'email': 'test@test.ch', 'password': 'test'
        })
    assert response.status_code == 200

def test_login_user_negativ(client):
    response = client.post("/users/login", json={
            'email': 'hans.maier@google.ch', 'password': '555'
        })
    assert response.status_code == 401