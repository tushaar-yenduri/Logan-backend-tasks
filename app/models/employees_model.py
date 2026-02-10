import boto3
import os
from dotenv import load_dotenv

load_dotenv()

TABLE_NAME = "Employees"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

table = dynamodb.Table(TABLE_NAME)


def create_employee_model(data):
    table.put_item(Item=data)


def get_employee_model(emp_id):
    return table.get_item(Key={"emp_id": emp_id})


def get_all_employees_model():
    return table.scan()


def update_employee_model(emp_id, data):
    table.update_item(
        Key={"emp_id": emp_id},
        UpdateExpression="SET #n=:n, #r=:r, salary=:s",
        ExpressionAttributeNames={
            "#n": "name",
            "#r": "role"
        },
        ExpressionAttributeValues={
            ":n": data["name"],
            ":r": data["role"],
            ":s": data["salary"]
        }
    )


def delete_employee_model(emp_id):
    table.delete_item(Key={"emp_id": emp_id})
