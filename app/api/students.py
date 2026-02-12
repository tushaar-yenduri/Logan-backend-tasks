from fastapi import APIRouter, HTTPException
from app.models.students_model import StudentCreate, StudentPut, StudentPatch, StudentResponse
from app.services.students_service import StudentService

router = APIRouter()
student_service = StudentService()

# CREATE
@router.post("/", response_model=dict, status_code=201)
def create_student(student: StudentCreate):
    return student_service.create_student(student)

# READ
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str):
    student = student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# PUT (Full Replace)
@router.put("/{student_id}", response_model=dict)
def replace_student(student_id: str, student: StudentPut):
    # Check if exists first (optional, but good practice for PUT)
    existing = student_service.get_student(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student_service.replace_student(student_id, student)

# PATCH (Partial Update)
@router.patch("/{student_id}", response_model=dict)
def patch_student(student_id: str, student: StudentPatch):
    existing = student_service.get_student(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_service.patch_student(student_id, student)

# DELETE
@router.delete("/{student_id}")
def delete_student(student_id: str):
    return student_service.delete_student(student_id)