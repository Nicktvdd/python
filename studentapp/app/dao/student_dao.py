from fastapi import HTTPException
from app.models.student import Student, UpdateStudent

class StudentDAO:
    def __init__(self):
        self._students = {}

    def get_student(self, student_id: int):
        if student_id not in self._students:
            raise HTTPException(status_code=404, detail="Student not found")
        return self._students[student_id]

    def get_student_by_name(self, name: str = None):
        if name is None:
            return list(self._students.values())
        for student in self._students.values(): 
            if student.name == name:
                return student
        raise HTTPException(status_code=404, detail="Student not found")

    def create_student(self, student_id: int, student: Student):
        if student_id in self._students:
            raise HTTPException(status_code=400, detail="Student already exists")
        self._students[student_id] = student
        return self._students[student_id]

    def update_student(self, student_id: int, student: UpdateStudent):
        if student_id not in self._students:
            raise HTTPException(status_code=404, detail="Student not found")
        self._students[student_id] = student
        return self._students[student_id]

    def delete_student(self, student_id: int):
        if student_id not in self._students:
            raise HTTPException(status_code=404, detail="Student not found")
        del self._students[student_id]
        