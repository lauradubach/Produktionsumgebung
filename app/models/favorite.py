from app.extensions import db
from apiflask import Schema
from apiflask.fields import Integer, String, Boolean
from sqlalchemy import UniqueConstraint

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.String(64), nullable=False)
    
    user = db.relationship('User', backref='favorites')

    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uix_user_event'),
    )

class FavoriteIn(Schema):
    event_id = String(required=True)
    user_id  = Integer(required=False)
    #next = String(required=False)
    is_favorite = Boolean(required=False)

class FavoriteOut(Schema):
    user_id = Integer()
    event_id = String()