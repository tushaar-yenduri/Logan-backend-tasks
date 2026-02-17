from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.employees_service import *

router = APIRouter()


# =========================
# DTOs
# =========================

class CreateEmployeeDTO(BaseModel):
    name: str
    role: str
    salary: int


class UpdateEmployeeDTO(BaseModel):  # PUT (full update)
    name: str
    role: str
    salary: int


class PatchEmployeeDTO(BaseModel):  # PATCH (partial update)
    name: Optional[str] = None
    role: Optional[str] = None
    salary: Optional[int] = None


class EmployeeResponseDTO(BaseModel):
    emp_id: str
    name: str
    role: str
    salary: int


# =========================
# Routes
# =========================

@router.post("/employees", response_model=EmployeeResponseDTO)
def create_employee(dto: CreateEmployeeDTO):
    return create_employee_service(dto)


@router.get("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def get_employee(emp_id: str):
    result = get_employee_service(emp_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.get("/employees", response_model=List[EmployeeResponseDTO])
def get_all_employees():
    return get_all_employees_service()


# PUT → Full Update
@router.put("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def update_employee(emp_id: str, dto: UpdateEmployeeDTO):
    result = update_employee_service(emp_id, dto)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


# PATCH → Partial Update
@router.patch("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def patch_employee(emp_id: str, dto: PatchEmployeeDTO):
    result = patch_employee_service(emp_id, dto)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: str):
    return delete_employee_service(emp_id)
