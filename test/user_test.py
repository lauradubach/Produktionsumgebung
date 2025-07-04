# Tests zur Benutzer-Authentifizierung und Benutzerverwaltung in der API

import pytest
from test import client


# Testet den erfolgreichen Login eines Benutzers und prüft, ob ein Token zurückgegeben wird.

def test_login_user(client):
    response = client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "token" in response.json

# Testet das Abrufen aller Benutzer mit gültigem Token.

def test_get_all_users(client):
    login_response = client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert login_response.status_code == 200
    token = login_response.json["token"]

    response = client.get("/users/", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    users = response.json

    assert isinstance(users, list)
    assert any(user["email"] == "admin@example.com" for user in users)

# Testet das Abrufen eines einzelnen Benutzers anhand seiner ID mit gültigem Token.

def test_get_one_user(client):
    login_response = client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert login_response.status_code == 200
    token = login_response.json["token"]
    user_id = login_response.json["user_id"]

    response = client.get(f"/users/{user_id}", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    user = response.json

    assert isinstance(user, dict)
    assert user["id"] == user_id
    assert user["email"] == "admin@example.com"