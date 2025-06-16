from flask import Blueprint, request, redirect, url_for, session, flash
from app.extensions import db
from app.favorites import bp
from app.models.favorite import Favorite, FavoriteOut
from flask import render_template

# GET-Route bleibt (optional, falls du sie brauchst)
@bp.route('', methods=['GET'])
def get_user_favorites():
    user_id = session.get('user_id')
    if not user_id:
        flash('Nicht eingeloggt.')
        return redirect(url_for('ui.login'))
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return FavoriteOut(many=True).dump(favorites), 200

# Toggle-Funktion: Favorit hinzufügen oder entfernen
@bp.route('', methods=['POST'])
def toggle_favorite():
    user_id = session.get('user_id')
    print("TOGGLE_FAVORITE aufgerufen")
    print(f"user_id: {user_id}")
    print(f"form data: {request.form}")
    if not user_id:
        flash('Nicht eingeloggt.')
        return redirect(url_for('ui.search'))

    event_id = request.form.get('event_id')
    next_url = request.form.get('next') or url_for('ui.search')
    is_favorite = request.form.get('is_favorite') == '1'  # aus dem Formular

    if not event_id or not event_id.isdigit():
        flash('Ungültige Event-ID.')
        return redirect(next_url)

    event_id = int(event_id)

    existing = Favorite.query.filter_by(user_id=user_id, event_id=event_id).first()

    if is_favorite and existing:
        # Favorit entfernen
        db.session.delete(existing)
        db.session.commit()
        flash('Event wurde aus deinen Favoriten entfernt.')
    elif not is_favorite and not existing:
        # Favorit hinzufügen
        favorite = Favorite(user_id=user_id, event_id=event_id)
        db.session.add(favorite)
        db.session.commit()
        flash('Event wurde zu deinen Favoriten hinzugefügt.')
    else:
        # Status unverändert, nichts tun
        pass

    return redirect(next_url)

@bp.route('/page', methods=['GET'])
def get_favorites_api():
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "Nicht eingeloggt"}, 401

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    # z.B. als JSON zurückgeben, kein Template:
    return FavoriteOut(many=True).dump(favorites), 200