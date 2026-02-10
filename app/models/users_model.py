from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    user_id: str
    name: str
    age: int
