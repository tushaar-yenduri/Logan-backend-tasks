from fastapi import FastAPI
import boto3
from pydantic import BaseModel

app = FastAPI()

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("students")


# Request body model
class Student(BaseModel):
    student_id: str
    name: str
    age: int
    course: str


@app.get("/")
def home():
    return {"message": "FastAPI + DynamoDB working!"}


# CREATE
@app.post("/students")
def create_student(student: Student):
    table.put_item(Item=student.model_dump())
    return {"message": "Student added successfully"}

# READ
@app.get("/students/{student_id}")
def get_student(student_id: str):
    response = table.get_item(
        Key={"student_id": student_id}
    )

    if "Item" not in response:
        return {"error": "Student not found"}

    return response["Item"]

# UPDATE
@app.put("/students/{student_id}")
def update_student(student_id: str, student: Student):
    response = table.update_item(
        Key={"student_id": student_id},
        UpdateExpression="set #n=:n, age=:a, course=:c",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={
            ":n": student.name,
            ":a": student.age,
            ":c": student.course
        },
        ReturnValues="UPDATED_NEW"
    )

    return {"message": "Student updated", "updated": response}
# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    table.delete_item(
        Key={"student_id": student_id}
    )

    return {"message": "Student deleted"}


