"""
Main FastAPI application module for Student Management API.
"""
import logging
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Import your modules
from app.api import students
from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)

# Load environment variables
load_dotenv()

# --- Logging Config ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# --- App Definition ---
app = FastAPI(
    title="Student Management API",
    description="FastAPI application for managing students with DynamoDB and JWT Auth",
    version="1.0.0"
)


# --- LOGIN ENDPOINT (Get Token) ---
@app.post("/token", tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in to get a JWT token.

    User: admin
    Password: secret
    """
    # HARDCODED USER FOR DEMO (Replace with DB check in real app)
    # This checks if the user sent "admin" and "secret"
    if form_data.username != "admin" or form_data.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # If correct, create a token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    logger.info("User %s logged in successfully", form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


# --- Register Routers ---
app.include_router(students.router, prefix="/students", tags=["Students"])


# --- Base Endpoints ---
@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    logger.info("Root endpoint accessed")
    return {"message": "Student Management API is running!"}


@app.get("/health")
async def health_check():
    """Health check endpoint that returns the service status."""
    return {"status": "healthy"}
