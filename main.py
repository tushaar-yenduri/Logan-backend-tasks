from fastapi import FastAPI, HTTPException
from typing import List
from models import StudentCreate, StudentUpdate, StudentResponse
import crud
from database import close_connection
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_connection()

app = FastAPI(title="Student Management API", lifespan=lifespan)

@app.post("/students/", response_model=StudentResponse, status_code=201)
def add_student(student: StudentCreate):
    """
    Endpoint to create a new student.
    """
    result = crud.create_student(student)
    if result and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    if not result:
        raise HTTPException(status_code=500, detail="Could not create student")
    return result

@app.get("/students/", response_model=List[StudentResponse])
def read_all_students():
    """
    Endpoint to fetch all students.
    """
    return crud.get_all_students()

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: str, student_update: StudentUpdate):
    """
    Endpoint to update a student's course or skills.
    """
    result = crud.update_student(student_id, student_update)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    if isinstance(result, dict) and "error" in result:
         raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    """
    Endpoint to delete a student.
    """
    success = crud.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
