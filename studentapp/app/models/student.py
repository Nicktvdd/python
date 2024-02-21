from pydantic import BaseModel, Field
from typing import Optional

class Student(BaseModel):
    id: int
    name: str
    age: int = Field(..., gt=0, lt=150)
    class_: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(None, gt=0, lt=150)
    class_: Optional[str] = None