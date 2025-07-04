# Erstellt ein API-Blueprint für die UI-Komponenten und lädt die zugehörigen Routen.

from apiflask import APIBlueprint

bp = APIBlueprint('ui', __name__)

from app.ui import routes