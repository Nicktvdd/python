from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    id: int
    name: str
    age: int
    class_: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_: Optional[str] = None