from database import get_collection
from models import StudentCreate, StudentUpdate

def create_student(student_data: StudentCreate):
    """
    Inserts a new student document into the collection.
    """
    collection = get_collection()
    if collection is None:
        return None
    
    # Check if student already exists
    if collection.find_one({"student_id": student_data.student_id}):
        return {"error": "Student ID already exists"}
    
    # Convert Pydantic model to dict
    student_dict = student_data.model_dump()
    result = collection.insert_one(student_dict)
    
    # Remove the internal MongoDB _id if it was added
    student_dict.pop("_id", None)
    
    # Check if insertion was successful
    if result.inserted_id:
        return student_dict
    return None

def get_all_students():
    """
    Fetches all student records from the database.
    """
    collection = get_collection()
    if collection is None:
        return []
    
    # Find all students, exclude MongoDB's internal _id
    students = list(collection.find({}, {"_id": 0}))
    return students

def update_student(student_id: str, update_data: StudentUpdate):
    """
    Updates a student's course or skills using student_id.
    """
    collection = get_collection()
    if collection is None:
        return None
    
    # Only update provided fields
    update_fields = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    if not update_fields:
        return {"error": "No update data provided"}
    
    result = collection.update_one(
        {"student_id": student_id},
        {"$set": update_fields}
    )
    
    if result.matched_count:
        return collection.find_one({"student_id": student_id}, {"_id": 0})
    return None

def delete_student(student_id: str):
    """
    Deletes a student record using student_id.
    """
    collection = get_collection()
    if collection is None:
        return False
    
    result = collection.delete_one({"student_id": student_id})
    return result.deleted_count > 0
