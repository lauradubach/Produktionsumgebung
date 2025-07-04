# Definiert eine API-Route zur Abfrage von Event-Daten mit optionalen Filterparametern und strukturierter JSON-Ausgabe.

from flask import request
from app.events import bp
from apiflask import APIBlueprint
from marshmallow import Schema, fields
from app.events.ticketmaster import fetch_events

# Definiert das Schema zur Validierung von Abfrageparametern in der URL

class EventQuerySchema(Schema):
    city = fields.String(required=False, metadata={"description": "Filter by city"})
    keyword = fields.String(required=False, metadata={"description": "Filter by keyword"})
    start_date = fields.String(required=False, metadata={"description": "Start date in ISO format (YYYY-MM-DD)"})
    end_date = fields.String(required=False, metadata={"description": "End date in ISO format (YYYY-MM-DD)"})
    country = fields.String(required=False, metadata={"description": "Filter by country code (e.g. DE, FR, IT)"})

# Definiert das Schema für die strukturierte JSON-Ausgabe der Event-Daten

class EventResponseSchema(Schema):
    id = fields.String()
    title = fields.String()
    start = fields.String()
    location = fields.String()
    city = fields.String()
    country = fields.String()
    url = fields.String()
    artists = fields.String(required=False)

# Definiert eine GET-Route, die Events basierend auf optionalen Filtern zurückliefert

@bp.get("/")
@bp.input(EventQuerySchema, location="query")
@bp.output(EventResponseSchema(many=True))
def get_events(query_data):
    events = fetch_events(
        keyword=query_data.get("keyword"),
        city=query_data.get("city"),
        start_date=query_data.get("start_date"),
        end_date=query_data.get("end_date"),
        country_codes=query_data.get("country")
    )
    return events