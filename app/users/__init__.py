# Erstellt ein API-Blueprint für Benutzer-bezogene Endpunkte und lädt die zugehörigen Routen.

from apiflask import APIBlueprint

bp = APIBlueprint('users', __name__)

from app.users import routes