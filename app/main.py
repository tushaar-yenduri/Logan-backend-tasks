from fastapi import FastAPI
from app.api.employees import router as employees_router

app = FastAPI(
    title="Employees API",
    description="CRUD Operations for Employees using DynamoDB",
    version="1.0.0"
)

# Include Employees Routes
app.include_router(employees_router)
