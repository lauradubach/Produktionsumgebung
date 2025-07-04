# Fixture zur Authentifizierung und Rückgabe des Bearer-Tokens für API-Tests

import pytest

@pytest.fixture
def auth_token(client):
    """Fixture to log in and return the authentication token in the correct header format."""
    response = client.post("/users/login", json={'email': 'admin@example.com', 'password': 'admin123'})
    token = response.json["token"]
    return {"Authorization": f"Bearer {token}"}