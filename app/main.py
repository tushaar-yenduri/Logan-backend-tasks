from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import logging
import os
from dotenv import load_dotenv

# Import your modules
from app.api import students
from app.auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

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
    
    logger.info(f"User {form_data.username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

# --- Register Routers ---
app.include_router(students.router, prefix="/students", tags=["Students"])

# --- Base Endpoints ---
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Student Management API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}