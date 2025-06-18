from test import client
import pytest

def test_add_favorites(client, auth_token):
    headers = { 'Authorization': 'Bearer {}'.format(auth_token) }
    favorite_data = {
        "event_id": "E999",
        "user_id": 1,
        "is_favorite": True
    }
    response = client.post("/favorites/user", headers=headers, json=favorite_data)
    print(f"Response Status Code: {response.status_code}")
    if 'Location' in response.headers:
        print(f"Redirect Location: {response.headers['Location']}")
    else:
        print("No Location header found in response.")


#def test_remove_favorite(client):
#    with client.session_transaction() as sess:
#        sess["user_id"] = 4

#    response = client.post("/favorites/", json={
#        "event_id": "E001",
#        "is_favorite": True
#    })
#    assert response.status_code == 200
#    assert "entfernt" in response.json["message"]

#def test_get_user_favorites(client):
#    with client.session_transaction() as sess:
#        sess["user_id"] = 4

#    response = client.get("/favorites/user")
#    assert response.status_code == 200
#    assert isinstance(response.json, list)

#def test_get_favorite_event_details(client):
#    with client.session_transaction() as sess:
#        sess["user_id"] = 4

#    response = client.get("/favorites")
#    assert response.status_code in [200, 201]
#    assert "events" in response.json