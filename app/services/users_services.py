import boto3
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
TABLE_NAME = os.getenv("DYNAMODB_TABLE")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)


def create_user(data: dict):
    user_id = str(uuid.uuid4())
    item = {"user_id": user_id, **data}
    table.put_item(Item=item)
    return item


def get_user(user_id: str):
    response = table.get_item(Key={"user_id": user_id})
    return response.get("Item")


def delete_user(user_id: str):
    table.delete_item(Key={"user_id": user_id})


def update_user(user_id: str, data: dict):
    update_expression = []
    expression_values = {}
    expression_names = {}

    for key, value in data.items():
        update_expression.append(f"#{key} = :{key}")
        expression_values[f":{key}"] = value
        expression_names[f"#{key}"] = key

    table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET " + ", ".join(update_expression),
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names,
    )
