from test import client
import pytest

def test_login_user(client):
    response = client.post("/users/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "token" in response.json

#def test_get_all_users(client, auth_headers):
#    response = client.get("/users/", headers=auth_headers)
#    assert response.status_code == 200
#    assert isinstance(response.json, list)

#def test_get_one_user(client, auth_headers):
#    response = client.get("/users/1", headers=auth_headers)
#    assert response.status_code == 200
#    assert "email" in response.json

#def test_patch_user(client, auth_headers):
#    response = client.patch("/users/1", json={"name": "updated_name"}, headers=auth_headers)
#    assert response.status_code == 200

# def test_delete_user(client, auth_headers):
#     response = client.delete("/users/3", headers=auth_headers)
#     assert response.status_code == 204