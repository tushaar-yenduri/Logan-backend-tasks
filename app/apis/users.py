"""User CRUD API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.users_model import UserCreate, UserResponse, UserUpdate
from app.services.users_services import (
    create_user,
    delete_user,
    get_user,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create(user: UserCreate, _current_user=Depends(get_current_user)) -> UserResponse:
    """Create a new user."""

    return create_user(user.dict())


@router.get("/{user_id}", response_model=UserResponse)
def read(user_id: str, _current_user=Depends(get_current_user)) -> UserResponse:
    """Retrieve a user by ID."""

    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete(user_id: str, _current_user=Depends(get_current_user)) -> dict:
    """Delete a user; only admins are allowed to perform this action."""

    if _current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )

    delete_user(user_id)
    return {"message": "deleted"}


@router.put("/{user_id}", response_model=UserResponse)
def replace(
    user_id: str,
    user: UserCreate,
    _current_user=Depends(get_current_user),
) -> UserResponse:
    """Replace an existing user with the provided payload."""

    update_user(user_id, user.dict())
    updated = get_user(user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.patch("/{user_id}", response_model=UserResponse)
def patch(
    user_id: str,
    user: UserUpdate,
    _current_user=Depends(get_current_user),
) -> UserResponse:
    """Apply a partial update to an existing user."""

    data = user.dict(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_user(user_id, data)
    updated = get_user(user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
