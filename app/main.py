from fastapi import FastAPI
import logging
from app.api import students  # <--- IMPORT THE NEW ROUTER

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- App Definition ---
app = FastAPI(
    title="Organization Management API",
    description="FastAPI application for managing organizations with DynamoDB",
    version="1.0.0"
)

# --- Register Routers ---
# This connects your 'students.py' controller to the main app
app.include_router(students.router, prefix="/students", tags=["Students"])

# --- Existing Routes ---
@app.get("/")
async def root():
    logger.info("Root endpoint accessed") # I updated print() to logger.info()
    return {"message": "Organization Management API is running!"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}