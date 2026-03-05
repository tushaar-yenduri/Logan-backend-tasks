"""Pydantic models used by the authentication API."""

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Incoming payload for user registration."""

    username: str
    password: str
    role: str | None = None


class RegisterResponse(BaseModel):
    """Response payload returned after successful registration."""

    user_id: str
    username: str
    role: str


class TokenRequest(BaseModel):
    """Incoming payload for requesting an access token."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Response payload containing an issued access token."""

    access_token: str
    token_type: str = "bearer"
