from app.models.user import User
from app.extensions import db
from apiflask import APIFlask

def test_create_user():
    app = APIFlask(__name__)
    with app.app_context():
        user = User(email="demo@user.com", favorite_genre="Rock")
        db.session.add(user)
        db.session.commit()

        result = User.query.filter_by(email="demo@user.com").first()
        assert result is not None
        assert result.favorite_genre == "Rock"
