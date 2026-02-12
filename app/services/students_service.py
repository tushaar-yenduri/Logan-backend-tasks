import boto3
import os
import uuid
from decimal import Decimal
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from app.models.students_model import StudentCreate, StudentPut, StudentPatch

load_dotenv()

class StudentService:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb", 
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.table = self.dynamodb.Table(os.getenv("DYNAMODB_TABLE", "students"))

    def _decimal_to_native(self, obj):
        """Helper to convert DynamoDB Decimal types to standard Python types."""
        if isinstance(obj, list):
            return [self._decimal_to_native(i) for i in obj]
        if isinstance(obj, dict):
            return {k: self._decimal_to_native(v) for k, v in obj.items()}
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return obj

    def create_student(self, student: StudentCreate):
        new_id = str(uuid.uuid4())
        student_data = student.model_dump()
        student_data["student_id"] = new_id
        
        try:
            self.table.put_item(Item=student_data)
            return {"message": "Student created", "student_id": new_id, "data": student_data}
        except ClientError as e:
            return {"error": str(e)}

    def get_student(self, student_id: str):
        try:
            response = self.table.get_item(Key={"student_id": student_id})
            item = response.get("Item")
            return self._decimal_to_native(item) if item else None
        except ClientError as e:
            print(f"Error: {e}")
            return None

    # --- PUT: Full Replacement ---
    def replace_student(self, student_id: str, student: StudentPut):
        """Replaces the entire student record with new data (Idempotent)."""
        student_data = student.model_dump()
        student_data["student_id"] = student_id  # Ensure ID stays the same

        try:
            # put_item overwrites by default
            self.table.put_item(Item=student_data)
            return {"message": "Student replaced successfully", "data": student_data}
        except ClientError as e:
            return {"error": str(e)}

    # --- PATCH: Partial Update ---
    def patch_student(self, student_id: str, student: StudentPatch):
        """Updates only the fields provided in the request."""
        # Filter out None values so we don't overwrite existing data with nulls
        update_data = student.model_dump(exclude_unset=True)

        if not update_data:
            return {"message": "No changes provided"}

        update_expression = "set "
        expression_values = {}
        expression_names = {}

        for key, value in update_data.items():
            attr_key = f"#{key}"  # Use placeholder for attribute name
            val_key = f":{key}"   # Use placeholder for value
            
            update_expression += f"{attr_key} = {val_key}, "
            expression_values[val_key] = value
            expression_names[attr_key] = key

        # Remove trailing comma
        update_expression = update_expression.rstrip(", ")

        try:
            response = self.table.update_item(
                Key={"student_id": student_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_names,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW"
            )
            updated_data = self._decimal_to_native(response.get("Attributes"))
            return {"message": "Student patched successfully", "data": updated_data}
        except ClientError as e:
            return {"error": str(e)}

    def delete_student(self, student_id: str):
        try:
            self.table.delete_item(Key={"student_id": student_id})
            return {"message": "Student deleted"}
        except ClientError as e:
            return {"error": str(e)}