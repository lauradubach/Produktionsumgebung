import pytest
from app import create_app
from test.create_test_data import create_test_data


# Initialize the testing environment

@pytest.fixture
def client():

    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        create_test_data()

    return app.test_client()
