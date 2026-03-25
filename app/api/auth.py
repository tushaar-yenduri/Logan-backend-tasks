from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.core.security import create_access_token, verify_token

router = APIRouter()
security = HTTPBearer()

HARDCODED_USER = "admin"
HARDCODED_PASSWORD = "admin123"
INVALID_LOGIN_DETAIL = "Invalid username or password"
INVALID_CREDENTIALS_DETAIL = "Could not validate credentials"
TOKEN_TYPE = "bearer"


class LoginRequest(BaseModel):
    """Payload for the login endpoint."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Response returned after successful authentication."""

    access_token: str
    token_type: str = TOKEN_TYPE


def _authentication_exception(detail: str) -> HTTPException:
    """Return a standardized HTTP exception for authentication failures."""

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Return the username embedded in a valid authorization token."""

    try:
        return verify_token(credentials.credentials)
    except Exception as exception:  # pylint: disable=broad-except
        raise _authentication_exception(INVALID_CREDENTIALS_DETAIL) from exception


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    """Validate the administrator credentials and issue a token."""

    if payload.username != HARDCODED_USER or payload.password != HARDCODED_PASSWORD:
        raise _authentication_exception(INVALID_LOGIN_DETAIL)

    return TokenResponse(access_token=create_access_token(payload.username))
