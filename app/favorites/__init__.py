from apiflask import APIBlueprint

bp = APIBlueprint('favorites', __name__)

from app.favorites import routes