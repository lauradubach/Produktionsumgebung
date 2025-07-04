# Erstellt ein API-Blueprint für den Bereich "events" und lädt die zugehörigen Routen.

from apiflask import APIBlueprint

bp = APIBlueprint('events', __name__)

from app.events import routes