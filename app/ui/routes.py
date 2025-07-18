# UI-Blueprint mit Routen für Benutzer-Authentifizierung, Registrierung, Event-Suche, Favoritenverwaltung und Logout.

import http
import email
from app.ui import bp
from app.extensions import db
from app.models.favorite import Favorite
from app.auth.auth_service import authenticate_user
from app.events.ticketmaster import fetch_event_by_id, fetch_events
from app.models.user import User, UserIn, UserOut, LoginIn, TokenOut
from flask import Blueprint, request, render_template, session, flash, redirect, url_for

# Zeigt die Login-Seite an.

@bp.route('/login', methods=['GET'])
def login_get():
    return render_template('users/login.html')

# Verarbeitet das Login-Formular und authentifiziert den Nutzer.

@bp.route('/login', methods=['POST'])
@bp.input(LoginIn, location='form')
def login_post(form_data=None):

    email = form_data['email']
    password = form_data['password']

    data = authenticate_user(email, password)
    if data:
        session['auth_token'] = data['token']
        session['user_id'] = data['user_id']
        flash('Login erfolgreich', 'success')
        return redirect(url_for('ui.search'))
    else:
        flash('Login fehlgeschlagen. Bitte E-Mail und Passwort kontrollieren.', 'danger')
        return redirect(url_for('ui.login_get'))

# Zeigt die Registrierungsseite an.

@bp.route('/register', methods=['GET'])
def register_get():
    return render_template('users/register.html')

# Verarbeitet das Registrierungsformular und legt einen neuen Nutzer an.

@bp.route('/register', methods=['POST'])
@bp.input(UserIn, location='form')
def register_post(form_data=None):

    name = form_data['name']
    email = form_data['email']
    password = form_data['password']
    
    user = User(**form_data)
    db.session.add(user)
    db.session.commit()

    flash('Registrierung erfolgreich! Bitte einloggen.', 'success')
    return redirect(url_for('ui.login_get'))
        
# Zeigt die Event-Suchseite an und gibt Events zurück, falls Suchparameter vorhanden sind.

@bp.route("/search", methods=["GET"])
def search():
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))

    keyword = request.args.get("keyword")
    city = request.args.get("city")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    country = request.args.get("country")

    if any([keyword, city, start_date, end_date, country]):
        events = fetch_events(
            keyword=keyword,
            city=city,
            start_date=start_date,
            end_date=end_date,
            country_codes=country
        )
    else:
        events = []
   
    favorite_event_ids = []
    if user_id:
        favorite_event_ids = [
            fav.event_id for fav in Favorite.query.filter_by(user_id=user_id).all()
        ]
    
    return render_template(
        "events/search.html",
        events=events,
        user_id=user_id,
        user_name=session.get("user_name"),
        favorite_event_ids=favorite_event_ids
    )

# Löscht die aktuelle Sitzung und loggt den Nutzer aus.

@bp.route('/logout')
def logout():
    session.clear()
    flash('Erfolgreich Ausgeloggt.', 'info')
    return redirect(url_for('ui.login_get'))

# Zeigt die Favoriten-Seite des aktuell angemeldeten Nutzers an.

@bp.route("/favorites")
def favorites_page():
    user_id = session.get("user_id")
    if not user_id:
        flash("Bitte zuerst einloggen.")
        return redirect(url_for("ui.login_get"))

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    event_ids = [f.event_id for f in favorites if f.event_id]

    events = []
    for eid in event_ids:
        event = fetch_event_by_id(eid)
        if event:
            events.append(event)

    return render_template(
        "users/favorites.html",
        events=events,
        favorite_event_ids=event_ids,
        user_id=user_id
    )
