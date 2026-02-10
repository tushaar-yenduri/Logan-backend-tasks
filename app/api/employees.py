from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.employees_service import *

router = APIRouter()


class Employee(BaseModel):
    emp_id: str
    name: str
    role: str
    salary: int


@router.get("/")
def home():
    return {"message": "FastAPI + DynamoDB is running"}


@router.post("/employees")
def create_employee(emp: Employee):
    return create_employee_service(emp)


@router.get("/employees/{emp_id}")
def get_employee(emp_id: str):
    result = get_employee_service(emp_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return result


@router.get("/employees")
def get_all_employees():
    return get_all_employees_service()


@router.put("/employees/{emp_id}")
def update_employee(emp_id: str, emp: Employee):
    return update_employee_service(emp_id, emp)


@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: str):
    return delete_employee_service(emp_id)
