from pydantic import BaseModel, Field
from typing import Optional

class StudentBase(BaseModel):
    name: str = Field(..., example="Tushaar")
    age: int = Field(..., example=22)
    course: str = Field(..., example="CSE")

class StudentCreate(StudentBase):
    pass 


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None


class StudentResponse(StudentBase):
    student_id: str


    model_config = {
        "from_attributes": True
    }