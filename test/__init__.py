# Importiert notwendige Module für das Test-Setup der Flask-Anwendung

import pytest
from app import create_app
from test.create_test_data import create_test_data

# Initialisiert die Testumgebung für die Flask-App mit Testdaten

@pytest.fixture
def client():

    app = create_app()
    app.config.update({
        "SECRET_KEY": "test_secret_key",
        "TESTING": True,
    })

    with app.app_context():
        create_test_data()

    return app.test_client()
