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


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    try:
        return verify_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc



@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    if payload.username != HARDCODED_USER or payload.password != HARDCODED_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(access_token=create_access_token(payload.username))


@router.get("/students/{name}")
def get_student(
    name: str,
    service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> dict[str, object]:
    try:
        return service.get_student(name)
    except StudentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/students")
def create_student(
    student: StudentDTO,
    service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> dict[str, object]:
    try:
        created_student = service.create_student(student)
    except StudentAlreadyExistsError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "message": "Student created successfully",
        "student": created_student,
    }


@router.put("/students/{name}")
def update_student(
    name: str,
    student: StudentUpdate,
    service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> dict[str, object]:
    try:
        updated_student = service.update_student(name, student)
    except NoUpdateFieldsError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except StudentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return {
        "message": "Student updated successfully",
        "student": updated_student,
    }


@router.patch("/students/{name}")
def patch_student(
    name: str,
    student: StudentUpdate,
    service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> dict[str, object]:
    try:
        updated_student = service.update_student(name, student)
    except NoUpdateFieldsError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except StudentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return {
        "message": "Student updated successfully",
        "student": updated_student,
    }


@router.delete("/students/{name}")
def delete_student(
    name: str,
    service: StudentService = Depends(get_student_service),
    _current_user: str = Depends(get_current_user),
) -> dict[str, str]:
    try:
        service.delete_student(name)
    except StudentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return {"message": "Student deleted successfully"}
