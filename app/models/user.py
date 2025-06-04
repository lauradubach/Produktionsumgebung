from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from app.extensions import db
from app.models.favorite import Favorite

####
## Schemas for OpenAPI and validation
####

class UserIn(Schema):
    name = String(required=True, validate=Length(0, 32))

class UserOut(Schema):
    id = Integer()
    name = String()
    level = String()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorite_genre = db.Column(db.String(80))

    favorites = db.relationship(
        'Favorite',
        backref='user',
        cascade='all, delete-orphan'
    )

    def get_favorite_events(self):
        return [f.event for f in self.favorites]