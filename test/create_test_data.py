
from app.extensions import db
from app.models.student import Student
from app.models.course import Course
from app.models.user import User

# Hilfsfunktion (Testdaten erstellen, Tabellen erstellen)
def create_test_data():
    db.drop_all() # dieser Befehl löscht alle vorhandenen Datenbankeintraege und Tabellen
    db.create_all()

    # Beispieldaten
    students = [
        {'name': 'Freda Kids', 'level': 'HF'},
        {'name': 'Sam Sung', 'level': 'HF'},
        {'name': 'Chris P. Bacon', 'level': 'AP'},
        {'name': 'Saad Maan', 'level': 'PE'}
    ]
    for student_data in students:
        student = Student(**student_data)
        db.session.add(student)

    # create an additional student and safe ref for later
    student_ref = Student(name='Mega Tron', level='HF')
    db.session.add(student_ref)

    courses = [
        {'title': 'M231 Security'},
        {'title': 'M254 BPMN'}
    ]
    for course_data in courses:
        course = Course(**course_data)
        db.session.add(course)

    # create an additional course and safe ref for later
    course_ref = Course(title='M347 Kubernetes')
    db.session.add(course_ref)
    student_ref.courses.append(course_ref)

    ###
    # User Test Data
    # Beispieldaten
    users = [
        {'name': 'Test', 'email': 'test@test.ch', 'password': 'test'},
        {'name': 'Boris Langer', 'email': 'boris@langer.ch', 'password': 'secret0'},
        {'name': 'technical user 1', 'email': 'tech1@tbz.ch.ch', 'password': 'secret1'},
        {'name': 'technical user 2', 'email': 'tech2@tbz.ch', 'password': 'secret2'},
    ]

    for user_data in users:
        user = User(**user_data)
        db.session.add(user)

    db.session.commit()