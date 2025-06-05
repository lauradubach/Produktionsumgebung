from app.models.favorite import Favorite
from app.models.user import User
from app.models.event import Event
from app.extensions import db

def test_user_can_favorite_event(client):
    with client.application.app_context():
        user = User(email="newuser@example.com", favorite_genre="Jazz")
        event = Event(city="hamburg")
        db.session.add(user)
        db.session.add(event)
        db.session.commit()

        favorite = Favorite(user_id=user.id, event_id=event.id, mark=4.5)
        db.session.add(favorite)
        db.session.commit()

        saved_fav = Favorite.query.filter_by(user_id=user.id, event_id=event.id).first()
        assert saved_fav is not None
        assert saved_fav.mark == 4.5