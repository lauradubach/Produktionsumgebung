# Definiert das Datenbankmodell und die API-Schemas für Favoriten, die Benutzer mit Events verknüpfen.

from apiflask import Schema
from app.extensions import db
from sqlalchemy import UniqueConstraint
from apiflask.fields import Integer, String, Boolean

# Datenbankmodell für Favoriten, das Benutzer und Events verbindet und Duplikate verhindert.

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.String(64), nullable=False)
    
    user = db.relationship('User', backref='favorites')

    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uix_user_event'),
    )

# Schema für die Eingabedaten beim Erstellen oder Aktualisieren eines Favoriten.

class FavoriteIn(Schema):
    event_id = String(required=True)
    user_id  = Integer(required=False)
    is_favorite = Boolean(required=False)

# Schema für die Ausgabe von Favoritendaten in API-Antworten.

class FavoriteOut(Schema):
    user_id = Integer()
    event_id = String()