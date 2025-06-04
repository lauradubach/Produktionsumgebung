from app.extensions import db
from apiflask import Schema
from apiflask.fields import Integer, Float

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    mark = db.Column(db.Float)

class FavoriteEventIn(Schema):
    event_id = Integer(required=True)
    mark = Float(load_default=None)

class FavoriteUserIn(Schema):
    user_id = Integer(required=True)

class FavoriteOut(Schema):
    user_id = Integer()
    event_id = Integer()
    mark = Float()