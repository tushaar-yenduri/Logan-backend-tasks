from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=20)
    grade: str = Field(..., example="A")
    email: str = Field(..., example="john.doe@example.com")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "age": 20,
                "grade": "A",
                "email": "john.doe@example.com",
            }
        }
    }


class StudentUpdate(BaseModel):
    age: int | None = Field(default=None, example=21)
    grade: str | None = Field(default=None, example="A+")
    email: str | None = Field(default=None, example="john.updated@example.com")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 21,
                "grade": "A+",
                "email": "john.updated@example.com",
            }
        }
    }


class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    grade: str
    email: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "643f463ce8f1c1d3dc5b1a72",
                "name": "John Doe",
                "age": 20,
                "grade": "A",
                "email": "john.doe@example.com",
            }
        }
    }
