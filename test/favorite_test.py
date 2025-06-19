from test import client
from unittest.mock import patch
import pytest

def test_add_favorites(client, auth_token):
    favorite_data = {
        "event_id": "E999",
        "user_id": 1,
        "is_favorite": True
    }
    response = client.post("/favorites/user", headers=auth_token, json=favorite_data)
    print(f"Response Status Code: {response.status_code}")
    if 'Location' in response.headers:
        print(f"Redirect Location: {response.headers['Location']}")
    else:
        print("No Location header found in response.")

def test_remove_favorite(client, auth_token):
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    # Favorit hinzufügen
    response_add = client.post("/favorites/", headers=auth_token, json={
        "event_id": "E001",
        "is_favorite": False
    })
    assert response_add.status_code == 201
    assert response_add.json["message"] == "Favorit hinzugefügt"

    # Favorit entfernen
    response_remove = client.post("/favorites/", headers=auth_token, json={
        "event_id": "E001",
        "is_favorite": True
    })
    assert response_remove.status_code == 200
    assert response_remove.json["message"] == "Favorit entfernt"

def test_get_user_favorites(client, auth_token):
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    # Favorit hinzufügen
    response_add = client.post("/favorites/", headers=auth_token, json={
        "event_id": "E001",
        "is_favorite": False
    })
    assert response_add.status_code == 201

    # Favoriten abrufen
    response = client.get("/favorites/user", headers=auth_token)
    assert response.status_code == 200

    favorites = response.json
    assert isinstance(favorites, list)
    assert any(f["event_id"] == "E001" and f["user_id"] == 1 for f in favorites)
