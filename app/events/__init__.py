from apiflask import APIBlueprint

bp = APIBlueprint('events', __name__)

from app.events import routes