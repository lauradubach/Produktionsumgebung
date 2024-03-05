from apiflask import APIFlask, Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from flask_sqlalchemy import SQLAlchemy
import os

app = APIFlask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

######
# Data Models


# für SQL Alchemy (table definition)
class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.String(8))

# für APIFlask (Input, Output Schemata)
class StudentIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    level = String(required=True, validate=OneOf(['HF', 'PE', 'AP', 'ICT']))

class StudentOut(Schema):
    id = Integer()
    name = String()
    level = String()


# Hilfsfunktion (Testdaten erstellen, Tabellen erstellen)
def init_database():
    db.drop_all() # dieser Befehl löscht alle vorhandenen Datenbankeintraege und Tabellen
    db.create_all()

    students = [
        {'name': 'Freda Kids', 'level': 'HF'},
        {'name': 'Sam Sung', 'level': 'HF'},
        {'name': 'Chris P. Bacon', 'level': 'AP'},
        {'name': 'Saad Maan', 'level': 'PE'}
    ]
    for student_data in students:
        student = StudentModel(**student_data)
        db.session.add(student)
    db.session.commit()


@app.get('/')
def say_hello():
    return {'message': 'Hello!'}


@app.get('/students/<int:student_id>')
@app.output(StudentOut)
def get_student(student_id):
    return db.get_or_404(StudentModel, student_id)


@app.get('/students')
@app.output(StudentOut(many=True))
def get_students():
    return StudentModel.query.all()


@app.post('/students')
@app.input(StudentIn, location='json')
@app.output(StudentOut, status_code=201)
def create_student(json_data):
    student = StudentModel(**json_data)
    db.session.add(student)
    db.session.commit()
    return student


@app.patch('/students/<int:student_id>')
@app.input(StudentIn(partial=True), location='json')
@app.output(StudentOut)
def update_student(student_id, json_data):
    student = db.get_or_404(StudentModel, student_id)
    for attr, value in json_data.items():
        setattr(student, attr, value)
    db.session.commit()
    return student


@app.delete('/students/<int:student_id>')
@app.output({}, status_code=204)
def delete_student(student_id):
    student = db.get_or_404(StudentModel, student_id)
    db.session.delete(student)
    db.session.commit()
    return ''


with app.app_context():
    init_database()