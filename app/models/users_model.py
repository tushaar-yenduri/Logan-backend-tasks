from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    user_id: str
    name: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None