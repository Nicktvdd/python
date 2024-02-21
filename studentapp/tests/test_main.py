from fastapi.testclient import TestClient
from app.main import app
from app.models.student import Student

client = TestClient(app)

def test_root():
	response = client.get("/")
	assert response.status_code == 200
	assert response.json() == {"message": "Hello World"}

def test_get_student_not_found():
	response = client.get("/students/999")
	assert response.status_code == 404

def test_create_student():
    student = Student(id=1, name="John", age=17, class_="year 12")
    response = client.post("/students/1", json=student.model_dump())
    assert response.status_code == 200
    assert response.json() == student.model_dump()

def test_get_student():
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John", "age": 17, "class_": "year 12"}

def test_update_student():
    student = {"name": "Jane"}
    response = client.put("/students/1", json=student)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane"

def test_delete_student():
    response = client.delete("/students/1")
    assert response.status_code == 200
    assert response.json() == {"Message": "Student deleted successfully"}

def test_get_student_by_name_not_found():
    response = client.get("/students?name=John")
    assert response.status_code == 404

def test_create_student_without_required_fields():
    student = {"name": "John"}
    response = client.post("/students/1", json=student)
    assert response.status_code == 400

def test_update_nonexistent_student():
    student = {"name": "Jane"}
    response = client.put("/students/999", json=student)
    assert response.status_code == 404

def test_delete_nonexistent_student():
    response = client.delete("/students/999")
    assert response.status_code == 404

def test_get_student_by_name():
    response = client.get("/students?name=Jane")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Jane", "age": 17, "class_": "year 12"}

def test_create_existing_student():
    student = Student(id=1, name="John", age=17, class_="year 12")
    response = client.post("/students/1", json=student.model_dump())
    assert response.status_code == 400

def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)