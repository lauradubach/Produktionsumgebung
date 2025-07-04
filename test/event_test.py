# Testet die Events-API mit Filtern und überprüft den erfolgreichen Antwortstatus und das Antwortformat.

from test import client

def test_get_events(client):
    response = client.get("/events?keyword=rock&city=Berlin&country=DE", follow_redirects=True)
    assert response.status_code == 200
    assert isinstance(response.json, list) or isinstance(response.json, dict)