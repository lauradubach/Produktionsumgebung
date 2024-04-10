import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very_secret_string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONITORING_DASHBOARD_ENABLED = os.environ.get('FLASK_MONITORING_DASHBOARD_ENABLED') or False
    MONITORING_DATABASE_URL = os.getenv('FLASK_MONITORING_DASHBOARD_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'fmd.db')
    MONITORING_TABLE_PREFIX = os.getenv('FLASK_MONITORING_DASHBOARD_TABLE_PREFIX') or "FMD_"
