from app.extensions import db
from app.models.user import User
from app.models.favorite import Favorite

def create_test_data():
    user = User(email='demo@user.com', favorite_genre='Rock')
    db.session.add(user)

    db.session.commit()

    favorite = Favorite(user_id=user.id, mark=5.0)
    db.session.add(favorite)

    db.session.commit()