from __future__ import annotations

from typing import Any

from pymongo.collection import Collection

from app.models.students_model import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)


class StudentAlreadyExistsError(Exception):
    pass


class StudentNotFoundError(Exception):
    pass


class NoUpdateFieldsError(Exception):
    pass


class StudentService:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def _serialize(self, student: dict[str, Any]) -> StudentResponse:
        return StudentResponse(
            id=str(student["_id"]),
            name=student["name"],
            age=student["age"],
            grade=student["grade"],
            email=student["email"],
        )

    def create_student(self, payload: StudentCreate) -> StudentResponse:
        if self._collection.find_one({"name": payload.name}):
            raise StudentAlreadyExistsError("Student with this name already exists")

        result = self._collection.insert_one(payload.model_dump())
        created = self._collection.find_one({"_id": result.inserted_id})
        return self._serialize(created)

    def get_all_students(self) -> list[StudentResponse]:
        return [self._serialize(student) for student in self._collection.find()]

    def update_student(self, name: str, payload: StudentUpdate) -> StudentResponse:
        update_data = {
            key: value for key, value in payload.model_dump().items() if value is not None
        }
        if not update_data:
            raise NoUpdateFieldsError("No fields provided for update")

        result = self._collection.update_one({"name": name}, {"$set": update_data})
        if result.matched_count == 0:
            raise StudentNotFoundError("Student not found")

        updated = self._collection.find_one({"name": name})
        return self._serialize(updated)

    def delete_student(self, name: str) -> None:
        result = self._collection.delete_one({"name": name})
        if result.deleted_count == 0:
            raise StudentNotFoundError("Student not found")


_student_service: StudentService | None = None


def configure_student_service(collection: Collection) -> None:
    global _student_service
    _student_service = StudentService(collection)


def get_student_service() -> StudentService:
    if _student_service is None:
        raise RuntimeError("StudentService has not been configured")
    return _student_service
