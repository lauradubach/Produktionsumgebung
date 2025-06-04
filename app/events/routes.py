from flask import Blueprint, request, jsonify
from app.events.ticketmaster import fetch_events

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["GET"])
def get_events():
    city = request.args.get("city")
    keyword = request.args.get("keyword")
    events = fetch_events(city, keyword)
    return jsonify(events)
