# Erstellt ein API-Blueprint für den Bereich "favorites" und lädt die zugehörigen Routen.

from apiflask import APIBlueprint

bp = APIBlueprint('favorites', __name__)

from app.favorites import routes