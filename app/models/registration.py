from apiflask import Schema
from apiflask.fields import Integer, Float

# Dies ist eine Association Klasse. Es gibt keine REST Routen dafür.

from app.extensions import db

class RegistrationCourseIn(Schema):
    course_id = Integer()

class RegistrationStudentIn(Schema):
    student_id = Integer()

class RegistrationOut(Schema):
    course_id = Integer()
    student_id = Integer()

# Hilfstabelle für many to many Relation
class Registration(db.Model):
    __tablename__ = 'registrations'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
