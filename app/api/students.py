from fastapi import APIRouter, HTTPException
from app.models.students_model import StudentCreate, StudentUpdate, StudentResponse
from app.services.students_service import StudentService

router = APIRouter()
student_service = StudentService()

# CREATE: Uses StudentCreate (No ID required from user)
@router.post("/", response_model=dict)
def create_student(student: StudentCreate):
    return student_service.create_student(student)

# READ: Returns StudentResponse (Includes ID)
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str):
    student = student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# UPDATE: Uses StudentUpdate (Optional fields)
@router.put("/{student_id}")
def update_student(student_id: str, student: StudentUpdate):
    return student_service.update_student(student_id, student)

# DELETE: No DTO needed
@router.delete("/{student_id}")
def delete_student(student_id: str):
    return student_service.delete_student(student_id)