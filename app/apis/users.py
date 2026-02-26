from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.users_model import UserCreate, UserResponse, UserUpdate
from app.services.users_services import create_user, delete_user, get_user, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create(user: UserCreate, current_user=Depends(get_current_user)):
    return create_user(user.dict())


@router.get("/{user_id}", response_model=UserResponse)
def read(user_id: str, current_user=Depends(get_current_user)):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete(user_id: str, current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")

    delete_user(user_id)
    return {"message": "deleted"}


@router.put("/{user_id}", response_model=UserResponse)
def replace(user_id: str, user: UserCreate, current_user=Depends(get_current_user)):
    update_user(user_id, user.dict())
    updated = get_user(user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.patch("/{user_id}", response_model=UserResponse)
def patch(user_id: str, user: UserUpdate, current_user=Depends(get_current_user)):
    data = user.dict(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_user(user_id, data)
    updated = get_user(user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
