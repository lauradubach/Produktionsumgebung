from app.extensions import db
from app.models.user import User
from app.models.event import Event
from app.models.favorite import Favorite

def create_test_data():
    db.drop_all()
    db.create_all()

    user = User(email='demo@user.com', favorite_genre='Rock')
    db.session.add(user)

    event = Event(city='berlin')
    db.session.add(event)

    db.session.commit()

    # Favorite-Verknüpfung
    favorite = Favorite(user_id=user.id, event_id=event.id, mark=5.0)
    db.session.add(favorite)

    db.session.commit()
