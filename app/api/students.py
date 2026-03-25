from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import get_current_user
from app.models.students_model import StudentDTO, StudentUpdate
from app.services.students_service import (
    NoUpdateFieldsError,
    StudentAlreadyExistsError,
    StudentNotFoundError,
    StudentService,
    get_student_service,
)

router = APIRouter()
JSON_RESPONSE = Dict[str, Any]


def _handle_student_not_found(exception: StudentNotFoundError) -> None:
    """Translate missing-student errors into HTTP 404 responses."""

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))


def _handle_student_exists_error(exception: StudentAlreadyExistsError) -> None:
    """Translate duplicate-student errors into HTTP 400 responses."""

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))


def _handle_no_update_error(exception: NoUpdateFieldsError) -> None:
    """Translate missing update fields into HTTP 400 responses."""

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))


def _get_student_response(
    student_name: str, student_service: StudentService
) -> JSON_RESPONSE:
    """Load a student record or raise a 404."""

    try:
        student = student_service.get_student(student_name)
        return {"student": student}
    except StudentNotFoundError as exception:
        _handle_student_not_found(exception)


@router.get("/students/{name}")
def get_student(
    name: str,
    student_service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> JSON_RESPONSE:
    """Return a student by name."""

    return _get_student_response(name, student_service)


@router.post("/students")
def create_student(
    student: StudentDTO,
    student_service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> JSON_RESPONSE:
    """Add a student record to the system."""

    try:
        created_student = student_service.create_student(student)
    except StudentAlreadyExistsError as exception:
        _handle_student_exists_error(exception)

    return {
        "message": "Student created successfully",
        "student": created_student,
    }


@router.put("/students/{name}")
def update_student(
    name: str,
    student: StudentUpdate,
    student_service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> JSON_RESPONSE:
    """Fully replace a student record."""

    try:
        updated_student = student_service.update_student(name, student)
    except NoUpdateFieldsError as no_update_exception:
        _handle_no_update_error(no_update_exception)
    except StudentNotFoundError as not_found_exception:
        _handle_student_not_found(not_found_exception)

    return {
        "message": "Student updated successfully",
        "student": updated_student,
    }


@router.patch("/students/{name}")
def patch_student(
    name: str,
    student: StudentUpdate,
    student_service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> JSON_RESPONSE:
    """Apply a partial update to an existing student."""

    try:
        updated_student = student_service.update_student(name, student)
    except NoUpdateFieldsError as no_update_exception:
        _handle_no_update_error(no_update_exception)
    except StudentNotFoundError as not_found_exception:
        _handle_student_not_found(not_found_exception)

    return {
        "message": "Student updated successfully",
        "student": updated_student,
    }


@router.delete("/students/{name}")
def delete_student(
    name: str,
    student_service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> JSON_RESPONSE:
    """Delete a student record if it exists."""

    try:
        student_service.delete_student(name)
    except StudentNotFoundError as exception:
        _handle_student_not_found(exception)

    return {"message": "Student deleted successfully"}
