"""Security and authentication helpers (password hashing and JWT handling)."""

from datetime import datetime, timedelta, timezone
import hashlib
import os

import boto3
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
AWS_REGION = os.getenv("AWS_REGION")

security = HTTPBearer()
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
auth_users_table = dynamodb.Table("auth_users")


def get_password_hash(password: str) -> str:
    """Return a SHA-256 hash for the given password."""

    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check whether the plain password matches the stored hash."""

    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_access_token(data: dict) -> str:
    """Create a signed JWT access token containing the given payload."""

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Resolve and return the current user from the Authorization header."""

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    response = auth_users_table.get_item(Key={"user_id": user_id})
    user = response.get("Item")

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
