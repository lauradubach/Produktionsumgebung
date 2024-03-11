from test import client

def test_get_students(client):
    response = client.get("/students/")
    assert response.json[4]['name'] == 'Mega Tron'

def test_get_student(client):
    response = client.get("/students/2")
    assert response.json["name"] == "Sam Sung"

def test_post_student(client):
    response = client.post("/students/", json={
            'name': 'Nina Hagen', 'level': 'AP'
        })
    assert response.status_code == 201

def test_change_student(client):
    response = client.patch("/students/2", json={'level': 'AP'})
    assert response.json['level'] == 'AP'

def test_register_student(client):
    response = client.post("/students/2/courses", json={'course_id': '1'})
    assert response.status_code == 201

def test_get_student_courses(client):
    response = client.get("/students/5/courses")
    assert response.json[0]['title'] == 'M347 Kubernetes'
