from fastapi import APIRouter, HTTPException, Depends
from app.models.students_model import StudentCreate, StudentPut, StudentPatch, StudentResponse
from app.services.students_service import StudentService
from app.auth import get_current_user  # <--- Import the security dependency

router = APIRouter()
student_service = StudentService()

# CREATE (Protected: Needs Token)
@router.post("/", response_model=dict, status_code=201)
def create_student(
    student: StudentCreate, 
    current_user: str = Depends(get_current_user) # <--- The Lock
):
    # You could log who created it: print(f"Created by {current_user}")
    return student_service.create_student(student)

# READ (Public: No Token needed)
# We usually leave GET public, but you can add Depends(get_current_user) here too if you want.
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str):
    student = student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# PUT (Protected: Needs Token)
@router.put("/{student_id}", response_model=dict)
def replace_student(
    student_id: str, 
    student: StudentPut, 
    current_user: str = Depends(get_current_user) # <--- The Lock
):
    existing = student_service.get_student(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student_service.replace_student(student_id, student)

# PATCH (Protected: Needs Token)
@router.patch("/{student_id}", response_model=dict)
def patch_student(
    student_id: str, 
    student: StudentPatch, 
    current_user: str = Depends(get_current_user) # <--- The Lock
):
    existing = student_service.get_student(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_service.patch_student(student_id, student)

# DELETE (Protected: Needs Token)
@router.delete("/{student_id}")
def delete_student(
    student_id: str, 
    current_user: str = Depends(get_current_user) # <--- The Lock
):
    return student_service.delete_student(student_id)