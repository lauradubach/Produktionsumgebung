from app.users import bp
from app.extensions import db
from app.models.user import User, UserIn, UserOut, LoginIn, TokenOut

from werkzeug.security import generate_password_hash

from app.auth import token_auth

####
## view functions
####    
@bp.get('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.output(UserOut)
def get_user(user_id):
    return db.get_or_404(User, user_id)

@bp.post('/')
@bp.input(UserIn, location='json')
@bp.output(UserOut, status_code=201)
def create_user(json_data):
    user = User(**json_data)
    db.session.add(user)
    db.session.commit()
    return user

@bp.patch('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.input(UserIn(partial=True), location='json')
@bp.output(UserOut)
def update_user(course_id, json_data):
    user = db.get_or_404(User, course_id)
    for attr, value in json_data.items():
        # If the attribute is 'password', hash it before saving
        if attr == 'password':
            hashed_password = generate_password_hash(value)
            setattr(user, attr, hashed_password)
        else:
            # For all other attributes, save them as they are
            setattr(user, attr, value)
    db.session.commit()
    return user

@bp.delete('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.output({}, status_code=204)
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return ''

@bp.post('/login')
@bp.input(LoginIn, location='json')
@bp.output(TokenOut, status_code=200)
def login_user(json_data):
    # Find user by email
    user = User.query.filter_by(email=json_data.get('email')).first()
    # If user doesn't exist or password is wrong
    if not user or not user.check_password(json_data.get('password')):
        return {'message': 'Invalid email or password'}, 401
    
    token = user.generate_auth_token(600)
    return { 'token': token, 'duration': 600 }
