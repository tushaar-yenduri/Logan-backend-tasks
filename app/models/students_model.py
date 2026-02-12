from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# --- Shared Properties ---
class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, example="Tushaar")
    age: int = Field(..., gt=0, lt=120, example=22)
    course: str = Field(..., min_length=2, example="Computer Science")
    email: EmailStr = Field(..., example="tushaar@example.com") # Requires 'pip install email-validator'
    enrollment_year: int = Field(..., ge=2000, le=2100, example=2025)
    is_active: bool = Field(default=True, example=True)

# --- 1. POST (Create) ---
# User provides base fields; Backend generates ID.
class StudentCreate(StudentBase):
    pass

# --- 2. PUT (Full Update) ---
# User must provide ALL fields to replace the record completely.
class StudentPut(StudentBase):
    pass

# --- 3. PATCH (Partial Update) ---
# All fields are optional. User can send just {"is_active": false}.
class StudentPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_year: Optional[int] = None
    is_active: Optional[bool] = None

# --- 4. GET (Response) ---
# Returns everything + the ID.
class StudentResponse(StudentBase):
    student_id: str

    model_config = {
        "from_attributes": True
    }