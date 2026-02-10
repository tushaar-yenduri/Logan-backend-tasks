from fastapi import APIRouter, HTTPException
from models.users import UserCreate, UserResponse
from services.users import create_user, get_user, delete_user

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
