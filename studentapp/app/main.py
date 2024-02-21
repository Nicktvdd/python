from fastapi import FastAPI
from app.models.student import Student, UpdateStudent
from app.dao.student_dao import StudentDAO
from typing import Optional

app = FastAPI()
student_dao = StudentDAO()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return student_dao.get_student(student_id)

@app.get("/students")
def get_student_by_name(name: Optional[str] = None):
    return student_dao.get_student_by_name(name)

@app.post("/students/{student_id}")
def create_student(student_id: int, student: Student):
    return student_dao.create_student(student_id, student)

@app.put("/students/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    return student_dao.update_student(student_id, student)

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    student_dao.delete_student(student_id)
    return {"Message": "Student deleted successfully"}