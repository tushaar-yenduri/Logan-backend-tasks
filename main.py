from fastapi import FastAPI

from pymongo import MongoClient

from app.api import students as students_api
from app.services.students_service import configure_student_service

app = FastAPI(title="Student CRUD API")
print("CRUD API started")

client = MongoClient("mongodb://localhost:27017/")
db = client["school_db"]
students_collection = db["students"]

configure_student_service(students_collection)
app.include_router(students_api.router)
