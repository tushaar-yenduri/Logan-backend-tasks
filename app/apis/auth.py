from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.auth_model import RegisterRequest, RegisterResponse, TokenRequest, TokenResponse
from app.services.auth_services import create_auth_user, ensure_auth_users_table, get_auth_user_by_username

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest):
    ensure_auth_users_table()

    existing = get_auth_user_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    role = payload.role or "user"
    if role not in {"user", "admin"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    created = create_auth_user(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        role=role,
    )

    if created is None:
        raise HTTPException(status_code=400, detail="Unable to create user")

    return {
        "user_id": created["user_id"],
        "username": created["username"],
        "role": created["role"],
    }


@router.post("/login", response_model=TokenResponse)
def login(payload: TokenRequest):
    ensure_auth_users_table()

    user = get_auth_user_by_username(payload.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password_hash = user.get("password_hash")
    if not password_hash or not verify_password(payload.password, password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({
        "user_id": user["user_id"],
        "role": user.get("role", "user"),
    })
    return {"access_token": access_token, "token_type": "bearer"}
