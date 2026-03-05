"""
Service layer for Employees.
Contains business logic for employee operations.
"""

import uuid
from app.models.employees_model import (
    create_employee_model,
    get_employee_model,
    get_all_employees_model,
    update_employee_model,
    delete_employee_model,
)


def create_employee_service(dto):
    """Handle business logic for creating an employee."""
    emp_id = str(uuid.uuid4())

    employee_data = {
        "emp_id": emp_id,
        "name": dto.name,
        "role": dto.role,
        "salary": dto.salary,
        "department": dto.department,
        "email": dto.email,
        "joining_date": dto.joining_date,
        "is_active": dto.is_active,
    }

    create_employee_model(employee_data)

    return employee_data


def get_employee_service(emp_id):
    """Fetch single employee."""
    response = get_employee_model(emp_id)

    if "Item" not in response:
        return None

    return response["Item"]


def get_all_employees_service():
    """Fetch all employees."""
    response = get_all_employees_model()
    return response.get("Items", [])


# PUT → Full Update
def update_employee_service(emp_id, dto):
    """Handle full update (PUT)."""

    response = get_employee_model(emp_id)
    if "Item" not in response:
        return None

    updated_data = {
        "name": dto.name,
        "role": dto.role,
        "salary": dto.salary,
        "department": dto.department,
        "email": dto.email,
        "joining_date": dto.joining_date,
        "is_active": dto.is_active,
    }

    update_employee_model(emp_id, updated_data)

    return {**updated_data, "emp_id": emp_id}


# PATCH → Partial Update
def patch_employee_service(emp_id, dto):
    """Handle partial update (PATCH)."""

    response = get_employee_model(emp_id)
    if "Item" not in response:
        return None

    existing_data = response["Item"]

    updated_data = {
        "name": (
            dto.name
            if dto.name is not None
            else existing_data.get("name")
        ),
        "role": (
            dto.role
            if dto.role is not None
            else existing_data.get("role")
        ),
        "salary": (
            dto.salary
            if dto.salary is not None
            else existing_data.get("salary")
        ),
        "department": (
            dto.department
            if dto.department is not None
            else existing_data.get("department")
        ),
        "email": (
            dto.email
            if dto.email is not None
            else existing_data.get("email")
        ),
        "joining_date": (
            dto.joining_date
            if dto.joining_date is not None
            else existing_data.get("joining_date")
        ),
        "is_active": (
            dto.is_active
            if dto.is_active is not None
            else existing_data.get("is_active")
        ),
    }

    update_employee_model(emp_id, updated_data)

    return {**updated_data, "emp_id": emp_id}


def delete_employee_service(emp_id):
    """Delete employee."""
    delete_employee_model(emp_id)
    return {"message": "Employee deleted successfully"}
