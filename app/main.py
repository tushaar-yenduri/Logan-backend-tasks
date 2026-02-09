from fastapi import FastAPI
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Organization Management API",
    description="FastAPI application for managing organizations with DynamoDB",
    version="1.0.0"
)


@app.get("/")
async def root():
    print("Organization Management API is running!")
    return {"message": "Organization Management API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}