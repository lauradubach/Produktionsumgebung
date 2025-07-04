# Konfiguration der Anwendung inklusive Datenbank-URI und Geheimschlüssel, mit spezieller Testkonfiguration

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Allgemeine Konfiguration der Anwendung mit Geheimschlüssel und Datenbank-URI

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very_secret_string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Spezielle Testkonfiguration mit In-Memory SQLite-Datenbank und aktiviertem Testmodus

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
