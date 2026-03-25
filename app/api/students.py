from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.core.security import create_access_token, verify_token
from app.models.students_model import StudentDTO, StudentUpdate
from app.services.students_service import (
    NoUpdateFieldsError,
    StudentAlreadyExistsError,
    StudentNotFoundError,
    StudentService,
    get_student_service,
)

router = APIRouter()
security = HTTPBearer()

HARDCODED_USER = "admin"
HARDCODED_PASSWORD = "admin123"
INVALID_LOGIN_DETAIL = "Invalid username or password"
INVALID_CREDENTIALS_DETAIL = "Could not validate credentials"
TOKEN_TYPE = "bearer"
JSON_RESPONSE = Dict[str, Any]


class LoginRequest(BaseModel):
    """Payload for the login endpoint."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Response returned after successful authentication."""

    access_token: str
    token_type: str = TOKEN_TYPE


def _authentication_exception(detail: str) -> HTTPException:
    """Return a standardized HTTP exception for authentication failures."""

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Return the username embedded in a valid authorization token."""

    try:
        return verify_token(credentials.credentials)
    except Exception as exception:  # pylint: disable=broad-except
        raise _authentication_exception(INVALID_CREDENTIALS_DETAIL) from exception



@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    """Validate the administrator credentials and issue a token."""

    if payload.username != HARDCODED_USER or payload.password != HARDCODED_PASSWORD:
        raise _authentication_exception(INVALID_LOGIN_DETAIL)

    return TokenResponse(access_token=create_access_token(payload.username))


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
        return student_service.get_student(student_name)
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
