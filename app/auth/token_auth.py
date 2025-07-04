# Richtet eine Token-basierte Authentifizierung ein und prüft, ob ein übermitteltes Token gültig ist.

from app.models.user import User
from apiflask.security import HTTPTokenAuth
 
token_auth = HTTPTokenAuth(scheme='Bearer')
 
@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    return user