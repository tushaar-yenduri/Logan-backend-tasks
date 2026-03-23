import requests
import json

# Example Base URL
BASE_URL = "http://localhost:8000"

# Example test data
test_students = [
    {
        "student_id": "STU001",
        "name": "John Doe",
        "age": 20,
        "course": "Computer Science",
        "skills": ["Python", "C++", "JavaScript"]
    },
    {
        "student_id": "STU002",
        "name": "Jane Smith",
        "age": 22,
        "course": "Data Science",
        "skills": ["Python", "SQL", "Machine Learning"]
    }
]

def seed_data():
    """
    Function to seed the database with example data using the API endpoints.
    Note: Requires the FastAPI server to be running.
    """
    print("Starting data seeding...")
    for student in test_students:
        response = requests.post(f"{BASE_URL}/students/", json=student)
        if response.status_code == 201:
            print(f"Successfully added student: {student['name']}")
        else:
            print(f"Failed to add student {student['name']}: {response.text}")

# --- Example JSON requests for manual testing ---

create_request = {
    "student_id": "STU003",
    "name": "Alice Brown",
    "age": 21,
    "course": "Mathematics",
    "skills": ["Calculus", "Statistics"]
}

update_request = {
    "course": "Applied Mathematics",
    "skills": ["Calculus", "Statistics", "R Programming"]
}

if __name__ == "__main__":
    # To run this script, ensure the FastAPI app is running (e.g., in another terminal)
    # python main.py
    try:
        seed_data()
    except Exception as e:
        print(f"Error seeding data: {e}. Make sure the server is running.")
