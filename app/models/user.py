from datetime import datetime, timezone
from flask import current_app
from app.extensions import db
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, Email, Regexp, OneOf
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

#### Schemas für OpenAPI und Validierung ####

class UserIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    email = String(required=True)
    password = String(required=True, validate=Length(0, 128))

class UserOut(Schema):
    id = Integer()
    name = String()
    email = String()
    password = String()

class LoginIn(Schema):
    email = String(required=True)
    password = String(required=True)
 
class TokenOut(Schema):
    token = String()
    duration = Integer()
    user_id = Integer()

#### Datenbankmodell ####

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    favorites = db.Column(db.String(80))

    favorites = db.relationship(
       'Favorite',
        backref='user',
        cascade='all, delete-orphan'
    )

    def get_favorites(self):
        return [f.event for f in self.favorites]
    
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_auth_token(self, expires_in=600):
        exp_timestamp = int(datetime.now(timezone.utc).timestamp()) + expires_in
        return encode(
            {'id': self.id, 'exp': exp_timestamp},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    def verify_auth_token(token):
        try:
            data = decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            return None
        except InvalidTokenError:
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None