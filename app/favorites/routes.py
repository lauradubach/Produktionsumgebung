from flask import Blueprint, request, redirect, url_for, session, flash
from app.extensions import db
from app.favorites import bp
from app.models.favorite import Favorite, FavoriteOut, FavoriteIn
from app.events.ticketmaster import fetch_events

@bp.post('/')
@bp.input(FavoriteIn, location='json')
@bp.output(FavoriteOut, status_code=201)
def toggle_favorite(json_data):
    user_id = session.get('user_id')
    if not user_id:
        return {"message": "Nicht eingeloggt"}, 401

    event_id = json_data['event_id']
    is_fav = json_data.get('is_favorite', False)

    if is_fav:
        # Favorit entfernen
        deleted = Favorite.query.filter_by(user_id=user_id, event_id=event_id).delete()
        db.session.commit()
        if deleted:
            return {"message": "Favorit entfernt"}, 200
        else:
            return {"message": "Favorit war nicht vorhanden"}, 200
    else:
        # Vor dem Hinzufügen prüfen, ob bereits existiert
        exists = Favorite.query.filter_by(user_id=user_id, event_id=event_id).first()
        if exists:
            return {"message": "Favorit existiert bereits"}, 200

        # Favorit hinzufügen
        fav = Favorite(user_id=user_id, event_id=event_id)
        db.session.add(fav)
        db.session.commit()
        return {"message": "Favorit hinzugefügt"}, 201


# Wenn der User eingeloggt ist, werden alle Favoriten aus der Datenbank geladen die diesem Nutzer gehören
# Die geladenen Favoriten werden mithilfe von FavoriteOut (ein API-Schema) in JSON konvertiert
@bp.route('/user', methods=['GET'])
def get_user_favorites():
    user_id = session.get('user_id')
    if not user_id:
        flash('Nicht eingeloggt.')
        return redirect(url_for('ui.login'))
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return FavoriteOut(many=True).dump(favorites), 200

# Diese API-Route gibt die Details aller favorisierten Events des aktuell eingeloggten Nutzers zurück – basierend auf den in der Datenbank gespeicherten event_ids.
@bp.route('', methods=['GET'])
@bp.output(FavoriteOut, status_code=201)
def get_favorite_event_details():
    user_id = session.get('user_id')
    if not user_id:
        return {"error": "Nicht eingeloggt"}, 401

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    event_ids = [fav.event_id for fav in favorites if fav.event_id]

    if not event_ids:
        return {"events": []}, 200

    # Hole alle Events von Ticketmaster (nur diese IDs)
    events = []
    for eid in event_ids:
        event_list = fetch_events(eid)
        if isinstance(event_list, list):
            events.extend(event_list)

    return {"events": events}, 200