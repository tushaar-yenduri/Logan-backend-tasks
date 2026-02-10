from app.models.employees_model import *


def create_employee_service(emp):
    create_employee_model(emp.dict())
    return {"message": "Employee created successfully"}


def get_employee_service(emp_id):
    response = get_employee_model(emp_id)

    if "Item" not in response:
        return None

    return response["Item"]


def get_all_employees_service():
    response = get_all_employees_model()
    return response.get("Items", [])


def update_employee_service(emp_id, emp):
    update_employee_model(emp_id, emp.dict())
    return {"message": "Employee updated successfully"}


def delete_employee_service(emp_id):
    delete_employee_model(emp_id)
    return {"message": "Employee deleted successfully"}
