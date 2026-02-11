from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.employees_service import *

router = APIRouter()


# ==============================
# DTOs
# ==============================

class CreateEmployeeDTO(BaseModel):
    name: str
    role: str
    salary: int


class UpdateEmployeeDTO(BaseModel):
    role: str
    salary: int


class EmployeeResponseDTO(BaseModel):
    emp_id: str
    name: str
    role: str
    salary: int


# ==============================
# Routes
# ==============================

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


@router.put("/employees/{emp_id}", response_model=EmployeeResponseDTO)
def update_employee(emp_id: str, dto: UpdateEmployeeDTO):
    return update_employee_service(emp_id, dto)


@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: str):
    return delete_employee_service(emp_id)
