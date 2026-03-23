from pydantic import BaseModel, Field
from typing import List, Optional

class StudentBase(BaseModel):
    student_id: str = Field(..., description="Unique identifier for the student")
    name: str = Field(..., description="Full name of the student")
    age: int = Field(..., description="Age of the student")
    course: str = Field(..., description="Course the student is enrolled in")
    skills: List[str] = Field(default=[], description="List of skills the student possesses")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    course: Optional[str] = None
    skills: Optional[List[str]] = None

class StudentResponse(StudentBase):
    pass
