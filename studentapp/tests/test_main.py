from fastapi.testclient import TestClient
from app.main import app
from app.models.student import Student
from pydantic import ValidationError
import pytest

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
    assert response.status_code == 422

def test_update_nonexistent_student():
    student = {"name": "Jane"}
    response = client.put("/students/999", json=student)
    assert response.status_code == 404

def test_delete_nonexistent_student():
    response = client.delete("/students/999")
    assert response.status_code == 404

def test_get_student_by_name():
    response = client.post("/students/1", json={"id": 1, "name": "Jane", "age": 17, "class_": "year 12"})
    assert response.status_code == 200
    response = client.get("/students?name=Jane")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Jane", "age": 17, "class_": "year 12"}]

def test_create_existing_student():
    student = Student(id=1, name="John", age=17, class_="year 12")
    response = client.post("/students/1", json=student.model_dump())
    assert response.status_code == 400

def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_student_with_existing_id():
    student = Student(id=1, name="John", age=17, class_="year 12")
    client.post("/students/1", json=student.model_dump())
    response = client.post("/students/1", json=student.model_dump())
    assert response.status_code == 400

def test_update_student_with_invalid_data():
    student = {"age": -1}
    response = client.put("/students/1", json=student)
    assert response.status_code == 422

def test_create_student_with_invalid_data():
    with pytest.raises(ValidationError):
        student = Student(id=1, name="John", age=-1, class_="year 12")

def test_get_student_by_name_multiple_students_same_name():
    student1 = Student(id=2, name="John", age=17, class_="year 12")
    student2 = Student(id=3, name="John", age=18, class_="year 13")
    response1 = client.post("/students/2", json=student1.model_dump())
    response2 = client.post("/students/3", json=student2.model_dump())
    assert response1.status_code == 200
    assert response1.json() == student1.model_dump()
    assert response2.status_code == 200
    assert response2.json() == student2.model_dump()

    response = client.get("/students?name=John")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_all_students_order():
    student1 = Student(id=4, name="John", age=17, class_="year 12")
    student2 = Student(id=5, name="Jane", age=18, class_="year 13")
    client.post("/students/4", json=student1.model_dump())
    client.post("/students/5", json=student2.model_dump())
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert response.json()[1]["id"] == 2
    assert response.json()[2]["id"] == 3
    assert response.json()[3]["id"] == 4
    assert response.json()[4]["id"] == 5