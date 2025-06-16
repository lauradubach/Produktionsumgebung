# app/auth/token_auth.py
 
from apiflask.security import HTTPTokenAuth
from app.models.user import User
 
token_auth = HTTPTokenAuth(scheme='Bearer')  # Uses Authorization: Bearer <token>
 
@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    return user