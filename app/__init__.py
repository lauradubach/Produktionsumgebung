# from apiflask import APIFlask
# from config import Config
# from app.extensions import db
# from flask_migrate import Migrate

# def create_app(config_class=Config):
#     app = APIFlask(
#         __name__,
#         title='Music Events API',
#         version='1.0',
#         docs_path='/docs',
#     )

#     app.config.from_object(config_class)

#     app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#         'pool_pre_ping': True
#     }

#     # Flask-Erweiterungen initialisieren
#     db.init_app(app)
#     migrate = Migrate(app, db)

#     # Blueprints registrieren
#     from app.events import bp as events_bp
#     app.register_blueprint(events_bp, url_prefix='/events')

#     from app.users import bp as users_bp
#     app.register_blueprint(users_bp, url_prefix='/users')

#     from app.ui import bp as ui_bp
#     app.register_blueprint(ui_bp, url_prefix='/ui')

#     from app.favorites import bp as favorites_bp
#     app.register_blueprint(favorites_bp, url_prefix='/favorites')

#     #with app.app_context():
#     #    db.create_all()

#     # Basis-Route
#     @app.get('/')
#     def test_page():
#         return {'message': 'Blueprint Flask - Production Setup (MSVC) - v1.0'}

#     return app

from apiflask import APIFlask
from config import Config
from app.extensions import db
from flask_migrate import Migrate

def create_app(config_class=Config):
    print("Starte create_app()")

    app = APIFlask(
        __name__,
        title='Music Events API',
        version='1.0',
        docs_path='/docs',
    )
    print("APIFlask instanziiert")

    app.config.from_object(config_class)
    print("Konfiguration geladen:")
    print("SQLALCHEMY_DATABASE_URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True
    }

    try:
        db.init_app(app)
        print("db.init_app erfolgreich")
    except Exception as e:
        print("Fehler bei db.init_app:", e)

    try:
        migrate = Migrate(app, db)
        print("Migrate initialisiert")
    except Exception as e:
        print("Fehler bei Migrate:", e)

    try:
        from app.events import bp as events_bp
        app.register_blueprint(events_bp, url_prefix='/events')
        print("events Blueprint geladen")
    except Exception as e:
        print("Fehler beim events Blueprint:", e)

    try:
        from app.users import bp as users_bp
        app.register_blueprint(users_bp, url_prefix='/users')
        print("users Blueprint geladen")
    except Exception as e:
        print("Fehler beim users Blueprint:", e)

    try:
        from app.ui import bp as ui_bp
        app.register_blueprint(ui_bp, url_prefix='/ui')
        print("ui Blueprint geladen")
    except Exception as e:
        print("Fehler beim ui Blueprint:", e)

    try:
        from app.favorites import bp as favorites_bp
        app.register_blueprint(favorites_bp, url_prefix='/favorites')
        print("favorites Blueprint geladen")
    except Exception as e:
        print("Fehler beim favorites Blueprint:", e)

    @app.get('/')
    def test_page():
        return {'message': 'Blueprint Flask - Production Setup (MSVC) - v1.0'}

    print("create_app abgeschlossen")
    return app