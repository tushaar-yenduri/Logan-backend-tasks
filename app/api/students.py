from fastapi import APIRouter, HTTPException
from app.models.students_model import Student
from app.services.students_service import StudentService

# 1. Create the router (This was missing/wrong in your error)
router = APIRouter()

# 2. Initialize the service
student_service = StudentService()

# CREATE
@router.post("/", response_model=dict)
def create_student(student: Student):
    return student_service.create_student(student)

# READ
@router.get("/{student_id}", response_model=Student)
def get_student(student_id: str):
    student = student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# UPDATE
@router.put("/{student_id}")
def update_student(student_id: str, student: Student):
    return student_service.update_student(student_id, student)

# DELETE
@router.delete("/{student_id}")
def delete_student(student_id: str):
    return student_service.delete_student(student_id)