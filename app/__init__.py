from apiflask import APIFlask

from config import Config
from app.extensions import db



def create_app(config_class=Config):
    app = APIFlask(__name__)
    app.config.from_object(config_class)

    # Flask Erweiterungen initialisieren
    db.init_app(app)
        
    # Blueprints registrieren
    from app.students import bp as students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    from app.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    with app.app_context():
        db.create_all()

    @app.route('/')
    def test_page():
        return {'message': 'Blueprint Flask - Production Setup (MSVC) - v1.0'}

    return app