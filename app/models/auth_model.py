from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str | None = None


class RegisterResponse(BaseModel):
    user_id: str
    username: str
    role: str


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
