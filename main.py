from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError


# ==================================================
# FastAPI App
# ==================================================

app = FastAPI()


# ==================================================
# Home Route (health check)
# ==================================================

@app.get("/")
def home():
    return {"message": "FastAPI + DynamoDB is running"}


# ==================================================
# DynamoDB Connection
# ==================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)

TABLE_NAME = "Employees"


# ==================================================
# Create Table Automatically
# ==================================================

def create_table():
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]

    if TABLE_NAME not in existing_tables:
        print("Creating DynamoDB table...")

        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "emp_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "emp_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        table.wait_until_exists()
        print("Table created successfully")


create_table()

table = dynamodb.Table(TABLE_NAME)


# ==================================================
# Pydantic Model
# ==================================================

class Employee(BaseModel):
    emp_id: str
    name: str
    role: str
    salary: int


# ==================================================
# CRUD APIs
# ==================================================

# ----------------------------
# Create Employee
# ----------------------------
@app.post("/employees")
def create_employee(emp: Employee):
    table.put_item(Item=emp.dict())
    return {"message": "Employee created successfully"}


# ----------------------------
# Get One Employee
# ----------------------------
@app.get("/employees/{emp_id}")
def get_employee(emp_id: str):
    response = table.get_item(Key={"emp_id": emp_id})

    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Employee not found")

    return response["Item"]


# ----------------------------
# Get All Employees
# ----------------------------
@app.get("/employees")
def get_all_employees():
    response = table.scan()
    return response.get("Items", [])


# ----------------------------
# Update Employee (FIXED)
# ----------------------------
@app.put("/employees/{emp_id}")
def update_employee(emp_id: str, emp: Employee):
    try:
        table.update_item(
            Key={"emp_id": emp_id},

            # 🔥 FIX: alias BOTH name & role
            UpdateExpression="SET #n=:n, #r=:r, salary=:s",

            ExpressionAttributeNames={
                "#n": "name",
                "#r": "role"
            },

            ExpressionAttributeValues={
                ":n": emp.name,
                ":r": emp.role,
                ":s": emp.salary
            }
        )

        return {"message": "Employee updated successfully"}

    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------
# Delete Employee
# ----------------------------
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: str):
    table.delete_item(Key={"emp_id": emp_id})
    return {"message": "Employee deleted successfully"}
