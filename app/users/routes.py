from app.users import bp
from app.extensions import db
from app.models.user import User, UserIn, UserOut
from app.models.event import Event, EventOut
from app.models.favorite import Favorite, FavoriteEventIn, FavoriteOut
from flask import abort

# Event als Favorit hinzufügen (inkl. optionaler Bewertung)
@bp.post('/<int:user_id>/favorites')
@bp.input(FavoriteEventIn, location='json')
@bp.output(FavoriteOut, status_code=201)
def add_favorite(user_id, json_data):
    user = db.get_or_404(User, user_id)
    event = db.get_or_404(Event, json_data['event_id'])

    # Doppelte Favoriten vermeiden
    existing = Favorite.query.filter_by(user_id=user.id, event_id=event.id).first()
    if existing:
        abort(400, "Event already favorited by user.")

    fav = Favorite(user_id=user.id, event_id=event.id, mark=json_data.get("mark"))
    db.session.add(fav)
    db.session.commit()
    return fav

# Alle Favoriten eines Users abrufen
@bp.get('/<int:user_id>/favorites')
@bp.output(EventOut(many=True))
def get_user_favorites(user_id):
    user = db.get_or_404(User, user_id)
    return user.get_favorite_events()