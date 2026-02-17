import uuid
from app.models.employees_model import *


def create_employee_service(dto):
    emp_id = str(uuid.uuid4())

    employee_data = {
        "emp_id": emp_id,
        "name": dto.name,
        "role": dto.role,
        "salary": dto.salary
    }

    create_employee_model(employee_data)

    return employee_data


def get_employee_service(emp_id):
    response = get_employee_model(emp_id)

    if "Item" not in response:
        return None

    return response["Item"]


def get_all_employees_service():
    response = get_all_employees_model()
    return response.get("Items", [])


# PUT → Full Update
def update_employee_service(emp_id, dto):

    response = get_employee_model(emp_id)
    if "Item" not in response:
        return None

    updated_data = {
        "name": dto.name,
        "role": dto.role,
        "salary": dto.salary
    }

    update_employee_model(emp_id, updated_data)

    return updated_data | {"emp_id": emp_id}


# PATCH → Partial Update
def patch_employee_service(emp_id, dto):

    response = get_employee_model(emp_id)
    if "Item" not in response:
        return None

    existing_data = response["Item"]

    updated_data = {
        "name": dto.name if dto.name is not None else existing_data["name"],
        "role": dto.role if dto.role is not None else existing_data["role"],
        "salary": dto.salary if dto.salary is not None else existing_data["salary"],
    }

    update_employee_model(emp_id, updated_data)

    return updated_data | {"emp_id": emp_id}


def delete_employee_service(emp_id):
    delete_employee_model(emp_id)
    return {"message": "Employee deleted successfully"}
