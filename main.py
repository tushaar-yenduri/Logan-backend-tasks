from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3

app = FastAPI()

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Users")


# MUST match DynamoDB key name
class User(BaseModel):
    user_id: str
    name: str
    age: int


@app.get("/")
def home():
    return {"ok": True}


@app.post("/users")
def create_user(user: User):
    table.put_item(Item=user.dict())
    return {"message": "created"}


@app.get("/users/{user_id}")
def get_user(user_id: str):
    response = table.get_item(Key={"user_id": user_id})
    item = response.get("Item")

    if not item:
        raise HTTPException(status_code=404, detail="User not found")

    return item


@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    table.put_item(Item=user.dict())
    return {"message": "updated"}


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    table.delete_item(Key={"user_id": user_id})
    return {"message": "deleted"}
