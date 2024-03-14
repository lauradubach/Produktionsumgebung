# Microservices - Produktionsumgebung

## Technologien

- Flask (https://flask.palletsprojects.com/en/3.0.x/)
- ApiFlask (https://apiflask.com/)
- SQLAlchemy (https://www.sqlalchemy.org/)
- mySQL (https://www.mysql.com/de/)
- Docker Compose (https://docs.docker.com/compose/)
- pyTest (https://docs.pytest.org/en/8.0.x/)
- Gunicorn (https://gunicorn.org/)

## Zweck

Dies ist eine Beispielapplikation für einen dockerized Flask-Server mit einer Dev und einer Prod Variante.

Es sollen Konzepte demonstriert werden, mit denen man von einer Entwicklungsumgebung einfach auf eine Produktionsumgebung wechseln kann.

Der Source Code ist ausschliesslich für Entwicklungszwecke gedacht.


## Funktionen

- Studenten und Kurse mit CRUD verwalten
- Studenten auf Kurse registrieren
- Kurse mit Studenten verknüpfen
- Alle Studenten eines Kurses anzeigen
- Alle Kurse eines Studenten anzeigen

## Design

```plantuml

class Student {
    name : String
    level : String
    create()
    delete()
    update(student: Student)
    register(course : Course)
}

class Course {
    title : String
    create()
    delete()
    update(course: Course)
    register(student: Student)
}

class Registration

Student "0..*" - "1..*" Course
(Student, Course) .. Registration

hide empty members
hide circle

```

## Installation

klone dieses Repo und wechsle in das Verzeichnis mit der Datei compose.yaml

Development Env (mit Hot Reload):

```bash
docker compose up --build
```

Tests ausführen:

```bash
docker compose -f compose.test.yaml up --build
```

Produktion:

```bash
docker compose -f compose.prod.yaml up --build
```




## Lizenz

© 2024. This work is openly licensed via [CC BY-NC.SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
