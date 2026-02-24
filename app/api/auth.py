from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.auth import create_access_token

router = APIRouter()

class LoginDTO(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(dto: LoginDTO):

    # Dummy check (replace with DB later)
    if dto.username != "admin" or dto.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": dto.username})

    return {"access_token": token, "token_type": "bearer"}