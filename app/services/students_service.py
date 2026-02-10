import boto3
import os
from decimal import Decimal
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from app.models.students_model import Student

# Load environment variables
load_dotenv()

class StudentService:
    def __init__(self):
        # DEBUG: Print the config to the terminal
        region = os.getenv("AWS_REGION", "us-east-1")
        table_name = os.getenv("DYNAMODB_TABLE", "students")
        print(f"--> SERVICE INIT: Connecting to DynamoDB in region: '{region}'")
        print(f"--> SERVICE INIT: Looking for table: '{table_name}'")

        self.dynamodb = boto3.resource(
            "dynamodb", 
            region_name=region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.table = self.dynamodb.Table(table_name)
        self.table = self.dynamodb.Table(os.getenv("DYNAMODB_TABLE", "students"))

    def _decimal_to_native(self, obj):
        """Helper to convert DynamoDB Decimal types to standard Python int/float."""
        if isinstance(obj, list):
            return [self._decimal_to_native(i) for i in obj]
        if isinstance(obj, dict):
            return {k: self._decimal_to_native(v) for k, v in obj.items()}
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return obj

    def create_student(self, student: Student):
        try:
            self.table.put_item(Item=student.model_dump())
            return {"message": "Student added successfully"}
        except ClientError as e:
            return {"error": str(e)}

    def get_student(self, student_id: str):
        try:
            response = self.table.get_item(Key={"student_id": student_id})
            item = response.get("Item")
            if item:
                return self._decimal_to_native(item)
            return None
        except ClientError as e:
            # In production, log this error instead of returning it
            print(f"Error fetching student: {e}") 
            return None

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
            updated_attributes = self._decimal_to_native(response.get("Attributes"))
            return {"message": "Student updated", "updated": updated_attributes}
        except ClientError as e:
            return {"error": str(e)}

    def delete_student(self, student_id: str):
        try:
            self.table.delete_item(Key={"student_id": student_id})
            return {"message": "Student deleted"}
        except ClientError as e:
            return {"error": str(e)}