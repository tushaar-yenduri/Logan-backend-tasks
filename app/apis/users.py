from fastapi import APIRouter, HTTPException
from app.models.users_model import UserCreate, UserResponse, UserUpdate
from app.services.users_services import create_user, get_user, delete_user, update_user

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse)
def create(user: UserCreate):
    return create_user(user.dict())

@router.get("/{user_id}", response_model=UserResponse)
def read(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete(user_id: str):
    delete_user(user_id)
    return {"message": "deleted"}


@router.put("/{user_id}", response_model=UserResponse)
def replace(user_id: str, user: UserCreate):
    updated = update_user(user_id, user.dict())
    return get_user(user_id)

@router.patch("/{user_id}", response_model=UserResponse)
def patch(user_id: str, user: UserUpdate):
    data = user.dict(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_user(user_id, data)
    return get_user(user_id)

