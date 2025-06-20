from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from app.events.ticketmaster import fetch_event_by_id, fetch_events
from app.models.favorite import Favorite
from app.ui import bp
import requests

API_BASE = 'http://localhost:5000/'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
 
        response = requests.post(f'{API_BASE}/users/login', json={
            'email': email,
            'password': password
        })
        print("Registrierungsantwort:", response.text)

        if response.status_code == 200:
            data = response.json()
            session['auth_token'] = data['token']
            session['user_id'] = data['user_id']
            flash('Login successful', 'success')
            return redirect(url_for('ui.search'))
        else:
            flash('Invalid credentials', 'danger')
 
    return render_template('users/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        response = requests.post(f'{API_BASE}/users', json={
            'name': name,
            'email': email,
            'password': password
        })
        if response.status_code == 201:
            flash('Registrierung erfolgreich! Bitte einloggen.', 'success')
            return redirect(url_for('ui.login'))  
        else:
            flash('Registration failed', 'danger')
    return render_template('users/register.html')


@bp.route("/search", methods=["GET"])
def search():
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login'))

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

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('ui.login'))

@bp.route("/favorites")
def favorites_page():
    user_id = session.get("user_id")
    if not user_id:
        flash("Bitte zuerst einloggen.")
        return redirect(url_for("ui.login"))

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
