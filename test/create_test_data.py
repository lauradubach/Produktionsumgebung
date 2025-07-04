# Erstellt Beispiel-Daten für Tests: Nutzer und Favoriten in der Datenbank anlegen

from app.extensions import db
from app.models.user import User
from app.models.favorite import Favorite

def create_test_data():
    db.drop_all()
    db.create_all()

    # Beispielnutzer
    users = [
        User(
            email='admin@example.com',
            name='admin',
            password='admin123',
        ),
        User(
            email='jane@example.com',
            name='jane_doe',
            password='password1',
        ),
        User(
            email='john@example.com',
            name='john_doe',
            password='password2',
        )
    ]

    for user in users:
        db.session.add(user)

    db.session.flush()

    # Referenzuser für Favoriten
    user_fav_ref = User(
        email='favuser@example.com',
        name='fav_user',
        password='test123',
    )
    db.session.add(user_fav_ref)
    db.session.flush()

    # Beispiel-Favoriten
    favorites = [
        Favorite(user_id=user_fav_ref.id, event_id='E001'),
        Favorite(user_id=user_fav_ref.id, event_id='E002'),
        Favorite(user_id=user_fav_ref.id, event_id='E003'),
    ]
    for fav in favorites:
        db.session.add(fav)

    db.session.commit()