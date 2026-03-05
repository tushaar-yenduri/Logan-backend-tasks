"""Pydantic models for user CRUD operations."""

from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Model representing payload for creating a user."""

    name: str
    age: int


class UserResponse(BaseModel):
    """Model used when returning user information from the API."""

    user_id: str
    name: str
    age: int


class UserUpdate(BaseModel):
    """Model representing partial updates to a user."""

    name: Optional[str] = None
    age: Optional[int] = None
