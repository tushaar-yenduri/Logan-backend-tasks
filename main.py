from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient


app = FastAPI(title="Student CRUD API")

print("CRUD API started")
# Update this connection string if your MongoDB server is running elsewhere.
client = MongoClient("mongodb://localhost:27017/")
db = client["school_db"]
students_collection = db["students"]


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


def serialize_student(student: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "grade": student["grade"],
        "email": student["email"],
    }


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Student CRUD API is running. Open /docs for Swagger UI.",
    }


@app.post("/students")
def create_student(student: StudentCreate) -> dict[str, Any]:
    existing_student = students_collection.find_one({"name": student.name})
    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this name already exists")

    result = students_collection.insert_one(student.model_dump())
    created_student = students_collection.find_one({"_id": result.inserted_id})
    return {
        "message": "Student created successfully",
        "student": serialize_student(created_student),
    }


@app.get("/students")
def get_all_students() -> dict[str, list[dict[str, Any]]]:
    students = [serialize_student(student) for student in students_collection.find()]
    return {"students": students}


@app.put("/students/{name}")
def update_student(name: str, student: StudentUpdate) -> dict[str, Any]:
    update_data = {key: value for key, value in student.model_dump().items() if value is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    result = students_collection.update_one({"name": name}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_student = students_collection.find_one({"name": name})
    return {
        "message": "Student updated successfully",
        "student": serialize_student(updated_student),
    }


@app.delete("/students/{name}")
def delete_student(name: str) -> dict[str, str]:
    result = students_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}



