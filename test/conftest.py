
import pytest

@pytest.fixture
def auth_token(client):
    """Fixture to log in and return the authentication token."""
    response = client.post("/users/login", json={'email': 'test@test.ch', 'password': 'test'})
    token = response.json["token"]
    return token