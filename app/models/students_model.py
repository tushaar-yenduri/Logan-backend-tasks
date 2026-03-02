"""
Student data models for the FastAPI application.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# --- Shared Properties ---
class StudentBase(BaseModel):
    """Base student model with common fields."""
    name: str = Field(..., min_length=2, example="Tushaar")
    age: int = Field(..., gt=0, lt=120, example=22)
    course: str = Field(..., min_length=2, example="Computer Science")
    email: EmailStr = Field(..., example="tushaar@example.com")
    enrollment_year: int = Field(..., ge=2000, le=2100, example=2025)
    is_active: bool = Field(default=True, example=True)


# --- 1. POST (Create) ---
# User provides base fields; Backend generates ID.
class StudentCreate(StudentBase):
    """Model for creating a new student."""


# --- 2. PUT (Full Update) ---
# User must provide ALL fields to replace the record completely.
class StudentPut(StudentBase):
    """Model for replacing a student record entirely."""


# --- 3. PATCH (Partial Update) ---
# All fields are optional. User can send just {"is_active": false}.
class StudentPatch(BaseModel):
    """Model for partially updating a student record."""
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_year: Optional[int] = None
    is_active: Optional[bool] = None


# --- 4. GET (Response) ---
# Returns everything + the ID.
class StudentResponse(StudentBase):
    """Model for student response including ID."""
    student_id: str

    model_config = {
        "from_attributes": True
    }
