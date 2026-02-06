import requests

BASE_URL = "http://127.0.0.1:8000"


# ======================================
# helper function
# ======================================
def print_response(title, response):
    print(f"\n===== {title} =====")
    print("Status:", response.status_code)
    print("Response:", response.json())


# ======================================
# CREATE 5 EMPLOYEES
# ======================================

employees = [
    {"emp_id": "101", "name": "Alice", "role": "Developer", "salary": 60000},
    {"emp_id": "102", "name": "Bob", "role": "Tester", "salary": 45000},
    {"emp_id": "103", "name": "Charlie", "role": "Manager", "salary": 90000},
    {"emp_id": "104", "name": "David", "role": "DevOps", "salary": 75000},
    {"emp_id": "105", "name": "Eva", "role": "HR", "salary": 50000},
]

for emp in employees:
    res = requests.post(f"{BASE_URL}/employees", json=emp)
    print_response(f"CREATE {emp['emp_id']}", res)


# ======================================
# READ ALL
# ======================================

res = requests.get(f"{BASE_URL}/employees")
print_response("READ ALL AFTER CREATE", res)


# ======================================
# UPDATE ONE EMPLOYEE (103)
# ======================================

updated_emp = {
    "emp_id": "103",
    "name": "Charlie",
    "role": "Senior Manager",
    "salary": 120000
}

res = requests.put(f"{BASE_URL}/employees/103", json=updated_emp)
print_response("UPDATE 103", res)


# ======================================
# DELETE ONE EMPLOYEE (104)
# ======================================

res = requests.delete(f"{BASE_URL}/employees/104")
print_response("DELETE 104", res)


# ======================================
# READ ALL AGAIN
# ======================================

res = requests.get(f"{BASE_URL}/employees")
print_response("FINAL READ ALL", res)
