"""
Employees API routes.
Handles CRUD operations with JWT protection.
"""

# =========================
# Standard Library Imports
# =========================
from typing import List, Optional

# =========================
# Third Party Imports
# =========================
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# =========================
# Local Application Imports
# =========================
from app.services.employees_service import (
    create_employee_service,
    get_employee_service,
    get_all_employees_service,
    update_employee_service,
    patch_employee_service,
    delete_employee_service,
)
from app.utils.auth import verify_token


router = APIRouter()

# =========================
# JWT Security Setup
# =========================

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Extract and validate JWT token."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# =========================
# DTOs
# =========================

class CreateEmployeeDTO(BaseModel):
    """DTO for creating employee."""
    name: str
    role: str
    salary: int
    department: str
    email: str
    joining_date: str
    is_active: bool


class UpdateEmployeeDTO(BaseModel):
    """DTO for full update (PUT)."""
    name: str
    role: str
    salary: int
    department: str
    email: str
    joining_date: str
    is_active: bool


class PatchEmployeeDTO(BaseModel):
    """DTO for partial update (PATCH)."""
    name: Optional[str] = None
    role: Optional[str] = None
    salary: Optional[int] = None
    department: Optional[str] = None
    email: Optional[str] = None
    joining_date: Optional[str] = None
    is_active: Optional[bool] = None


class EmployeeResponseDTO(BaseModel):
    """DTO for employee response."""
    emp_id: str
    name: str
    role: str
    salary: int
    department: Optional[str] = None
    email: Optional[str] = None
    joining_date: Optional[str] = None
    is_active: Optional[bool] = None


# =========================
# Routes (All Protected)
# =========================

@router.post("/employees", response_model=EmployeeResponseDTO)
def create_employee(
    dto: CreateEmployeeDTO,
    _user=Depends(get_current_user),  # renamed to fix pylint
):
    """Create a new employee."""
    return create_employee_service(dto)


@router.get("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def get_employee(
    emp_id: str,
    _user=Depends(get_current_user),
):
    """Get employee by ID."""
    result = get_employee_service(emp_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.get("/employees", response_model=List[EmployeeResponseDTO])
def get_all_employees(
    _user=Depends(get_current_user),
):
    """Get all employees."""
    return get_all_employees_service()


@router.put("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def update_employee(
    emp_id: str,
    dto: UpdateEmployeeDTO,
    _user=Depends(get_current_user),
):
    """Full update employee."""
    result = update_employee_service(emp_id, dto)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.patch("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def patch_employee(
    emp_id: str,
    dto: PatchEmployeeDTO,
    _user=Depends(get_current_user),
):
    """Partial update employee."""
    result = patch_employee_service(emp_id, dto)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.delete("/employees/{emp_id}")
def delete_employee(
    emp_id: str,
    _user=Depends(get_current_user),
):
    """Delete employee."""
    return delete_employee_service(emp_id)
