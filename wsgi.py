# Startet die Flask-Anwendung und lädt Umgebungsvariablen aus einer .env-Datei

from app import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run()