import boto3
from dotenv import load_dotenv
import os

load_dotenv()

region = os.getenv("AWS_REGION", "us-east-1")
print(f"Checking for tables in region: {region}...")

try:
    dynamodb = boto3.client(
        "dynamodb", 
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    response = dynamodb.list_tables()
    print("Tables found:", response['TableNames'])
except Exception as e:
    print("Error:", e)