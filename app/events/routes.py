from apiflask import APIBlueprint
from flask import request
from app.events.ticketmaster import fetch_events
from marshmallow import Schema, fields

events_bp = APIBlueprint("events", __name__, url_prefix="/events")

# Schema zur Validierung und Dokumentation
class EventQuerySchema(Schema):
    city = fields.String(required=False, metadata={"description": "Filter by city"})
    keyword = fields.String(required=False, metadata={"description": "Filter by keyword"})
    start_date = fields.String(required=False, metadata={"description": "Start date in ISO format (YYYY-MM-DDTHH:MM:SSZ)"})
    end_date = fields.String(required=False, metadata={"description": "End date in ISO format (YYYY-MM-DDTHH:MM:SSZ)"})

class EventResponseSchema(Schema):
    title = fields.String()
    start = fields.String()
    location = fields.String()
    city = fields.String()
    country = fields.String()
    url = fields.String()
    artists = fields.String(required=False)

from flask import request

@events_bp.get("/")
def get_events():
    events = fetch_events(
        keyword=request.args.get("keyword"),
        city=request.args.get("city"),
        start_date=request.args.get("start_date"),
        end_date=request.args.get("end_date")
    )
    return events
