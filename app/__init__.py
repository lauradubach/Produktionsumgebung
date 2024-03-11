from apiflask import APIFlask

from config import Config
from app.extensions import db



def create_app(config_class=Config):
    app = APIFlask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
        
    with app.app_context():
        db.create_all()

    # Register blueprints here
    from app.students import bp as students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    from app.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    @app.route('/')
    def test_page():
        return {'message': 'Testing the Flask Application Factory Pattern'}

    return app