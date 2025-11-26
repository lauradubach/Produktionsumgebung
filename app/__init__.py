# Erstellt und konfiguriert die API-Anwendung mit Blueprints und Datenbankanbindung.

from config import Config
from app.extensions import db
from apiflask import APIFlask
from flask_migrate import Migrate
from flask import url_for, redirect

# Application Factory: Erstellt und konfiguriert die API-Flask-Anwendung inklusive Blueprints und Datenbank

def create_app(config_class=Config):
    app = APIFlask(
        __name__,
        title='Music Events API',
        version='1.0',
        docs_path='/docs',
    )

    app.config.from_object(config_class)

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True
    }

    # Flask-Erweiterungen initialisieren
    db.init_app(app)
    #migrate = Migrate(app, db)

    # Blueprints registrieren
    from app.events import bp as events_bp
    app.register_blueprint(events_bp, url_prefix='/events')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.ui import bp as ui_bp
    app.register_blueprint(ui_bp, url_prefix='/ui')

    from app.favorites import bp as favorites_bp
    app.register_blueprint(favorites_bp, url_prefix='/favorites')

    with app.app_context():
        db.create_all()

    # Basis-Route
    @app.get('/')
    def test_page():
        return redirect(url_for('ui.search'))

    return app