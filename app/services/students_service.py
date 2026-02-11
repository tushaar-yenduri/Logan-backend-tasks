import boto3
import os
import uuid  # <--- NEW IMPORT
from decimal import Decimal
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from app.models.students_model import StudentCreate, StudentUpdate, StudentResponse # <--- UPDATED IMPORTS

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
        if isinstance(obj, list):
            return [self._decimal_to_native(i) for i in obj]
        if isinstance(obj, dict):
            return {k: self._decimal_to_native(v) for k, v in obj.items()}
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return obj

    # --- UPDATED CREATE METHOD ---
    def create_student(self, student: StudentCreate):
        # Generate a unique ID automatically
        new_id = str(uuid.uuid4())
        
        # Convert the DTO to a dictionary
        student_data = student.model_dump()
        
        # Add the ID to the data
        student_data["student_id"] = new_id

        try:
            self.table.put_item(Item=student_data)
            return {"message": "Student added", "student_id": new_id}
        except ClientError as e:
            return {"error": str(e)}

    # --- UPDATED GET METHOD ---
    def get_student(self, student_id: str):
        try:
            response = self.table.get_item(Key={"student_id": student_id})
            item = response.get("Item")
            if item:
                return self._decimal_to_native(item)
            return None
        except ClientError as e:
            return None

    # --- UPDATED UPDATE METHOD ---
    def update_student(self, student_id: str, student: StudentUpdate):
        # We only want to update fields that the user actually sent (not None values)
        update_data = student.model_dump(exclude_unset=True)

        if not update_data:
            return {"message": "No fields provided for update"}

        # Build the dynamic UpdateExpression
        update_expression = "set "
        expression_values = {}
        expression_names = {}

        for key, value in update_data.items():
            # Handle reserved words like 'name'
            attr_name = f"#{key}" if key == "name" else key
            attr_val = f":{key}"
            
            update_expression += f"{attr_name} = {attr_val}, "
            expression_values[attr_val] = value
            if key == "name":
                expression_names["#name"] = "name"

        # Remove trailing comma
        update_expression = update_expression.rstrip(", ")

        try:
            params = {
                "Key": {"student_id": student_id},
                "UpdateExpression": update_expression,
                "ExpressionAttributeValues": expression_values,
                "ReturnValues": "UPDATED_NEW"
            }
            # Only add ExpressionAttributeNames if we used it (for reserved words)
            if expression_names:
                params["ExpressionAttributeNames"] = expression_names

            response = self.table.update_item(**params)
            
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