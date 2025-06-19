# import pytest

# @pytest.fixture
# def auth_token(client):
#     """Fixture to log in and return the authentication token."""
#     response = client.post("/users/login", json={'email': 'admin@example.com', 'password': 'admin123'})
#     token = response.json["token"]
#     return token


import pytest

@pytest.fixture
def auth_token(client):
    """Fixture to log in and return the authentication token in the correct header format."""
    response = client.post("/users/login", json={'email': 'admin@example.com', 'password': 'admin123'})
    token = response.json["token"]
    # Gib das Dictionary im richtigen Header-Format zurück
    return {"Authorization": f"Bearer {token}"}