from app.models.favorite import Favorite
from app.models.user import User
from app.models.event import Event
from app.extensions import db
from apiflask import APIFlask


def test_user_can_favorite_event():
    app = APIFlask(__name__)
    with app.app_context():
        user = User(email="fav@user.com", favorite_genre="Pop")
        event = Event(city="berlin")
        db.session.add(user)
        db.session.add(event)
        db.session.commit()

        favorite = Favorite(user_id=user.id, event_id=event.id, mark=4.5)
        db.session.add(favorite)
        db.session.commit()

        saved_fav = Favorite.query.filter_by(user_id=user.id, event_id=event.id).first()
        assert saved_fav is not None
        assert saved_fav.mark == 4.5