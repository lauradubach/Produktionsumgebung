from apiflask import APIFlask
from config import Config
from app.extensions import db
from flask_migrate import Migrate

def create_app(config_class=Config):
    app = APIFlask(
        __name__,
        title='Music Events API',
        version='1.0',
        docs_path='/docs',      # Swagger UI
    )

    app.config.from_object(config_class)

    # Flask-Erweiterungen initialisieren
    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprints registrieren
    from app.events.routes import events_bp
    app.register_blueprint(events_bp)

    from app.users.routes import bp as users_bp
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

    # Basis-Route
    @app.get('/')
    def test_page():
        return {'message': 'Blueprint Flask - Production Setup (MSVC) - v1.0'}

    return app