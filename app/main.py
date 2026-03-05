"""
Main entry point for Employees API application.
Initializes FastAPI and includes routers.
"""
from fastapi import FastAPI
from app.api.employees import router as employees_router
from app.api.auth import router as auth_router   # ✅ add this

app = FastAPI(
    title="Employees API",
    description="CRUD Operations for Employees using DynamoDB",
    version="1.0.0"
)

# Include Auth Routes
app.include_router(auth_router)   # ✅ add this

# Include Employees Routes
app.include_router(employees_router)
