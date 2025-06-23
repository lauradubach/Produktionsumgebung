from app.users import bp
from app.extensions import db
from app.models.user import User, UserIn, UserOut, LoginIn, TokenOut
from app.auth.token_auth import token_auth
from apiflask import abort
 
from werkzeug.security import generate_password_hash
from flask import request

#  Holt einen einzelnen Nutzer anhand der ID, wenn ein gültiger Token vorhanden ist.
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

# Aktualisiert ausgewählte Nutzerdaten und gibt ggf. ein neues Token zurück, wenn das Passwort geändert wurde.
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

# Löscht einen Nutzer anhand der ID, wenn ein gültiger Token vorhanden ist.
@bp.delete('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.output({}, status_code=204)
def delete_user(user_id):
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")

    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return 'User succesfully deleted'

# Authentifiziert den Nutzer anhand von E-Mail und Passwort und gibt ein Auth-Token zurück.
@bp.post('/login')
@bp.input(LoginIn, location='json')
@bp.output(TokenOut, status_code=200)
def login_user(json_data):
    user = User.query.filter_by(email=json_data.get('email')).first()

    if not user or not user.check_password(json_data.get('password')):
        abort(401, message='Invalid email or password')

    token = user.generate_auth_token(600)

    return {
        'token': token,
        'duration': 600,
        'user_id': user.id
    }