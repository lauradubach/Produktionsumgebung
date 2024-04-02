from apiflask import HTTPTokenAuth
from app.models.user import User

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    return True