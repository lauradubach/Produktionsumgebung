from test import client

# simple test to check if test framework is working

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200