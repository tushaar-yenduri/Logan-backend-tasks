from fastapi import APIRouter, Depends, HTTPException

from app.models.students_model import StudentDTO, StudentUpdate
from app.services.students_service import (
    NoUpdateFieldsError,
    StudentAlreadyExistsError,
    StudentNotFoundError,
    StudentService,
    get_student_service,
)

router = APIRouter()


@router.get("/students/{name}")
def get_student(
    name: str, service: StudentService = Depends(get_student_service)
) -> dict[str, object]:
    try:
        return service.get_student(name)
    except StudentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.post("/students")
def create_student(
    student: StudentDTO, service: StudentService = Depends(get_student_service)
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
    name: str, service: StudentService = Depends(get_student_service)
) -> dict[str, str]:
    try:
        service.delete_student(name)
    except StudentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return {"message": "Student deleted successfully"}
