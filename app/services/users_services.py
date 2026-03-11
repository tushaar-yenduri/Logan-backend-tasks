
import os
import uuid

import boto3
from boto3.dynamodb.conditions import Attr
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
TABLE_NAME = os.getenv("DYNAMODB_TABLE")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)


def create_user(data: dict) -> dict:
    """Create a new user item in DynamoDB"""

    user_id = str(uuid.uuid4())
    item = {"user_id": user_id, **data}
    table.put_item(Item=item)
    return item


def get_user(user_id: str) -> dict | None:
    """Fetch a user by ID from DynamoDB."""

    response = table.get_item(Key={"user_id": user_id})
    return response.get("Item")


def get_user_by_username(username: str) -> dict | None:
    """Fetch a single user item by username."""

    response = table.scan(
        FilterExpression=Attr("username").eq(username),
        Limit=1,
    )
    items = response.get("Items", [])
    return items[0] if items else None


def delete_user(user_id: str) -> None:
    """Delete a user from DynamoDB."""

    table.delete_item(Key={"user_id": user_id})


def update_user(user_id: str, data: dict) -> None:
    """Apply partial updates to a user item in DynamoDB."""

    if not data:
        return

    update_expression: list[str] = []
    expression_values: dict[str, object] = {}
    expression_names: dict[str, str] = {}

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
