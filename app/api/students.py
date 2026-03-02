"""
Students API module for CRUD operations on student records.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.models.students_model import StudentCreate, StudentPatch, StudentPut, StudentResponse
from app.services.students_service import StudentService

router = APIRouter()
student_service = StudentService()


# CREATE (Protected: Needs Token)
@router.post("/", response_model=dict, status_code=201)
def create_student(
    student: StudentCreate,
    _current_user: str = Depends(get_current_user)  # <--- The Lock
):
    """
    Create a new student record.

    Requires authentication token.
    """
    return student_service.create_student(student)


# READ (Public: No Token needed)
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str):
    """
    Get a student by ID.

    Returns student details or 404 if not found.
    """
    student = student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# PUT (Protected: Needs Token)
@router.put("/{student_id}", response_model=dict)
def replace_student(
    student_id: str,
    student: StudentPut,
    _current_user: str = Depends(get_current_user)  # <--- The Lock
):
    """
    Replace a student record completely.

    Requires authentication token.
    """
    existing = student_service.get_student(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_service.replace_student(student_id, student)


# PATCH (Protected: Needs Token)
@router.patch("/{student_id}", response_model=dict)
def patch_student(
    student_id: str,
    student: StudentPatch,
    _current_user: str = Depends(get_current_user)  # <--- The Lock
):
    """
    Partially update a student record.

    Requires authentication token.
    """
    existing = student_service.get_student(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_service.patch_student(student_id, student)


# DELETE (Protected: Needs Token)
@router.delete("/{student_id}")
def delete_student(
    student_id: str,
    _current_user: str = Depends(get_current_user)  # <--- The Lock
):
    """
    Delete a student record.

    Requires authentication token.
    """
    return student_service.delete_student(student_id)
