from app.models.event import Event
from app.extensions import db

def test_get_events(client):
    with client.application.app_context():
        event = Event(title="Test Event", city="berlin")
        db.session.add(event)
        db.session.commit()

    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json, list)