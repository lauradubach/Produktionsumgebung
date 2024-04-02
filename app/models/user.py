from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, Email

from werkzeug.security import generate_password_hash, check_password_hash

from flask import current_app
from app.extensions import db
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError

from datetime import datetime, timezone
import sqlalchemy as sa

####
## Schemas for OpenAPI and validation
####
class UserIn(Schema):
    email = String(required=True, validate=[Length(0, 128), Email()])
    name = String(required=True, validate=Length(0, 128))
    password = String(required=True, validate=Length(0, 128))

class UserOut(Schema):
    id = Integer()
    email = String()
    name = String()

class LoginIn(Schema):
    email = String(required=True, validate=[Length(0,128), Email()])
    password = String(required=True, validate=Length(0, 128))

class TokenOut(Schema):
    token = String()
    duration = Integer() 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_on = db.Column(db.DateTime)

    def __init__( self, email, name, password ):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
        self.created_on = datetime.now()


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_in = 600):
        exp_timestamp = int(datetime.now(timezone.utc).timestamp()) + expires_in
        return encode(
            { 'id': self.id, 'exp': exp_timestamp },
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            # Handle expired token, if necessary
            return None
        except InvalidTokenError:
            # Handle invalid token, if necessary
            return None
        except Exception as e:
            # Log or handle other exceptions
            print(f"An error occurred: {e}")
            return None