import boto3
from botocore.exceptions import ClientError
from app.models.students_model import Student

class StudentService:
    def __init__(self):
        # Initialize DynamoDB resource
        # In a real app, use environment variables for region and table name!
        self.dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        self.table = self.dynamodb.Table("students")

    def create_student(self, student: Student):
        try:
            self.table.put_item(Item=student.model_dump())
            return {"message": "Student added successfully"}
        except ClientError as e:
            return {"error": str(e)}

    def get_student(self, student_id: str):
        response = self.table.get_item(Key={"student_id": student_id})
        return response.get("Item")

    def update_student(self, student_id: str, student: Student):
        try:
            response = self.table.update_item(
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
            return {"message": "Student updated", "updated": response.get("Attributes")}
        except ClientError as e:
            return {"error": str(e)}

    def delete_student(self, student_id: str):
        try:
            self.table.delete_item(Key={"student_id": student_id})
            return {"message": "Student deleted"}
        except ClientError as e:
            return {"error": str(e)}