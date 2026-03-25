from __future__ import annotations

from typing import Iterable, Annotated
from pydantic import BaseModel, Field, PositiveInt, field_validator

NameType = Annotated[str, Field(min_length=2)]
CourseType = Annotated[str, Field(min_length=3)]
SkillType = Annotated[str, Field(min_length=1)]


class StudentDTO(BaseModel):
    student_id: str | None = Field(
        default=None,
        description="MongoDB object id",
    )
    name: NameType = Field(...)
    age: PositiveInt = Field(...)
    course: CourseType = Field(...)
    skills: list[SkillType] = Field(
        ..., min_length=1
    )

    @field_validator("skills", mode="before")
    @staticmethod
    def _strip_and_filter(skills: Iterable[str]) -> list[str]:
        normalized = []
        for skill in skills:
            cleaned = skill.strip()
            if cleaned:
                normalized.append(cleaned)
        if not normalized:
            raise ValueError("skills must contain at least one non-empty entry")
        return normalized

    model_config = {
        "json_schema_extra": {
            "example": {
                "student_id": "643f463ce8f1c1d3dc5b1a72",
                "name": "John Doe",
                "age": 20,
                "course": "Computer Science",
                "skills": ["Python", "FastAPI"],
            }
        }
    }


class StudentCreate(BaseModel):
    name: NameType
    age: PositiveInt
    course: CourseType
    skills: list[SkillType]

    @field_validator("skills", mode="before")
    @staticmethod
    def _strip_and_filter(skills: Iterable[str]) -> list[str]:
        normalized = []
        for skill in skills:
            cleaned = skill.strip()
            if cleaned:
                normalized.append(cleaned)
        if not normalized:
            raise ValueError("skills must contain at least one non-empty entry")
        return normalized


class StudentUpdate(BaseModel):
    age: PositiveInt | None = Field(None)
    course: CourseType | None = Field(None)
    skills: list[SkillType] | None = Field(None)

    @field_validator("skills", mode="before")
    @staticmethod
    def _strip_and_filter(skills: Iterable[str] | None) -> list[str] | None:
        if skills is None:
            return None

        normalized = []
        for skill in skills:
            cleaned = skill.strip()
            if cleaned:
                normalized.append(cleaned)
        if not normalized:
            raise ValueError("skills must contain at least one non-empty entry")
        return normalized
