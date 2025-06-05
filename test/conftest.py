import pytest
from app import create_app
from app.extensions import db
from test.create_test_data import create_test_data

@pytest.fixture
def client():
    app = create_app()
    app.config.update({"TESTING": True})

    with app.app_context():
        db.drop_all()
        db.create_all()
        create_test_data()
        yield app.test_client()