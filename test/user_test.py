from test import client
import pytest

def test_login_user(client):
    response = client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_get_all_users(client):
    # Login beim richtigen Endpoint
    login_response = client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert login_response.status_code == 200
    token = login_response.json["token"]

    # Authentifizierter Request an /users/
    response = client.get("/users/", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    users = response.json

    assert isinstance(users, list)
    assert any(user["email"] == "admin@example.com" for user in users)

def test_get_one_user(client):
    # Einloggen, um ein Token zu bekommen
    login_response = client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert login_response.status_code == 200
    token = login_response.json["token"]
    user_id = login_response.json["user_id"]

    # Authentifizierter Zugriff auf /users/<user_id>
    response = client.get(f"/users/{user_id}", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    user = response.json

    assert isinstance(user, dict)
    assert user["id"] == user_id
    assert user["email"] == "admin@example.com"