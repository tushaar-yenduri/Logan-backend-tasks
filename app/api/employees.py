from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from app.services.employees_service import *
from app.utils.auth import verify_token

router = APIRouter()

# =========================
# JWT Security Setup
# =========================

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# =========================
# DTOs
# =========================

class CreateEmployeeDTO(BaseModel):
    name: str
    role: str
    salary: int
    department: str
    email: str
    joining_date: str
    is_active: bool


class UpdateEmployeeDTO(BaseModel):  # PUT (full update)
    name: str
    role: str
    salary: int
    department: str
    email: str
    joining_date: str
    is_active: bool


class PatchEmployeeDTO(BaseModel):  # PATCH (partial update)
    name: Optional[str] = None
    role: Optional[str] = None
    salary: Optional[int] = None
    department: Optional[str] = None
    email: Optional[str] = None
    joining_date: Optional[str] = None
    is_active: Optional[bool] = None


class EmployeeResponseDTO(BaseModel):
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
    user=Depends(get_current_user)
):
    return create_employee_service(dto)


@router.get("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def get_employee(
    emp_id: str,
    user=Depends(get_current_user)
):
    result = get_employee_service(emp_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.get("/employees", response_model=List[EmployeeResponseDTO])
def get_all_employees(
    user=Depends(get_current_user)
):
    return get_all_employees_service()


# PUT → Full Update
@router.put("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def update_employee(
    emp_id: str,
    dto: UpdateEmployeeDTO,
    user=Depends(get_current_user)
):
    result = update_employee_service(emp_id, dto)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


# PATCH → Partial Update
@router.patch("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def patch_employee(
    emp_id: str,
    dto: PatchEmployeeDTO,
    user=Depends(get_current_user)
):
    result = patch_employee_service(emp_id, dto)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.delete("/employees/{emp_id}")
def delete_employee(
    emp_id: str,
    user=Depends(get_current_user)
):
    return delete_employee_service(emp_id)