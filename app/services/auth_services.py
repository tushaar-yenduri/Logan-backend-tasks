import boto3
import os
import uuid

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
auth_table = dynamodb.Table("auth_users")


def ensure_auth_users_table() -> None:
    client = dynamodb.meta.client

    try:
        client.describe_table(TableName="auth_users")
        return
    except client.exceptions.ResourceNotFoundException:
        pass

    client.create_table(
        TableName="auth_users",
        KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "username", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
        GlobalSecondaryIndexes=[
            {
                "IndexName": "username-index",
                "KeySchema": [{"AttributeName": "username", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
    )
    client.get_waiter("table_exists").wait(TableName="auth_users")


def get_auth_user_by_id(user_id: str):
    response = auth_table.get_item(Key={"user_id": user_id})
    return response.get("Item")


def get_auth_user_by_username(username: str):
    response = auth_table.query(
        IndexName="username-index",
        KeyConditionExpression=Key("username").eq(username),
        Limit=1,
    )
    items = response.get("Items", [])
    return items[0] if items else None


def create_auth_user(username: str, password_hash: str, role: str = "user"):
    user_id = str(uuid.uuid4())
    item = {
        "user_id": user_id,
        "username": username,
        "password_hash": password_hash,
        "role": role,
    }

    try:
        auth_table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(user_id)",
        )
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            return None
        raise

    return item
