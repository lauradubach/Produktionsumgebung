# API-Blueprint für Benutzerverwaltung mit CRUD-Operationen und Authentifizierung.

from app.users import bp
from flask import request
from apiflask import abort
from app.extensions import db
from app.auth.token_auth import token_auth
from app.auth.auth_service import authenticate_user
from werkzeug.security import generate_password_hash
from app.models.user import User, UserIn, UserOut, LoginIn, TokenOut

# Gibt einen einzelnen Nutzer zurück, wenn ein gültiger Token vorliegt.

@bp.get('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.output(UserOut)
def get_one_user(user_id):
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")

    return db.get_or_404(User, user_id)

# Gibt eine Liste aller Nutzer zurück, wenn ein gültiger Token vorhanden ist.

@bp.get('/')
@bp.auth_required(token_auth)
@bp.output(UserOut(many=True))
def get_all_users():
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")
    
    return User.query.all()

# Erstellt einen neuen Nutzer mit den übermittelten Daten und gibt ein Auth-Token zurück.

@bp.post('/')
@bp.input(UserIn, location='json')
@bp.output(UserOut, status_code=201)
def create_user(json_data):
    user = User(**json_data)
    db.session.add(user)
    db.session.commit()
    
    token = user.generate_auth_token(600)

    return {
        'token': token,
        'duration': 600,
        'user_id': user.id
    }

# Aktualisiert Nutzerdaten und gibt ggf. ein neues Token bei Passwortänderung zurück.

@bp.patch('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.input(UserIn(partial=True), location='json')
@bp.output(TokenOut, status_code=200)
def update_user(user_id, json_data):
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")

    user = db.get_or_404(User, user_id)
        
    for attr, value in json_data.items():
        if attr == "password":
            user.password = value
            password_changed = True
        else:
            setattr(user, attr, value)
    
    db.session.commit()

    if password_changed:
        token = user.generate_auth_token(600)
        return {'token': token, 'duration': 600}

    return {'token': '', 'duration': 0}

# Authentifiziert den Nutzer anhand von E-Mail und Passwort und gibt ein Auth-Token zurück.

@bp.post('/login')
@bp.input(LoginIn, location='json')
@bp.output(TokenOut, status_code=200)
def login_user(json_data):
    result = authenticate_user(json_data.get('email'), json_data.get('password'))

    if not result:
        abort(401, message='Invalid email or password')

    return result