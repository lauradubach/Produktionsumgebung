from app.models.user import User
from app.extensions import db

def test_create_user(client):
    with client.application.app_context():
        user = User(email="newuser@example.com", favorite_genre="Jazz")
        db.session.add(user)
        db.session.commit()

        result = User.query.filter_by(email="newuser@example.com").first()
        assert result is not None
        assert result.favorite_genre == "Jazz"