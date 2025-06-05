from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

from app.extensions import db
from app.models.user import User

class EventIn(Schema):
    title = String(required=True, validate=Length(0, 32))
   
class EventOut(Schema):
    id = Integer()
    title = String()

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    city = db.Column(db.String(120))

    favorites = db.relationship(
        'Favorite',
        backref='event',
        cascade='all, delete-orphan'
    )