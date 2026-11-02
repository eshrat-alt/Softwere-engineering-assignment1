from flask import Flask, request, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)

# Demo user accounts
users = {
    "employee": {
        "password": generate_password_hash("emp123"),
        "role": "Employee"
    },
    "admin": {
        "password": generate_password_hash("admin123"),
        "role": "Administrator"
    }
}

# Store active login tokens
tokens = {}

# Sample employee records
employees = [
    {"id": 1, "name": "Ali Khan", "department": "IT", "email": "ali@example.com"},
    {"id": 2, "name": "Sara Ahmed", "department": "HR", "email": "sara@example.com"},
    {"id": 3, "name": "Ahmed Raza", "department": "Finance", "email": "ahmed@example.com"}
]


# Authentication: check whether user is logged in
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = request.headers.get("Authorization", "").replace("Bearer ", "", 1)

        if not token or token not in tokens:
            return jsonify({"error": "Please login first"}), 401

        request.current_user = tokens[token]

        return func(*args, **kwargs)

    return wrapper


# Authorization: check user's role
def admin_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):

        if request.current_user["role"] != "Administrator":
            return jsonify({"error": "Admin access required"}), 403

        return func(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    return "Employee Management API is Running!"


# Login API
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if username not in users or not password:
        return jsonify({"error": "Invalid username or password"}), 401

    if not check_password_hash(users[username]["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = secrets.token_hex(16)

    tokens[token] = {
        "username": username,
        "role": users[username]["role"]
    }

    return jsonify({
        "message": "Login successful",
        "username": username,
        "role": users[username]["role"],
        "token": token
    }), 200


# View employees: Employee and Administrator
@app.route("/employees", methods=["GET"])
@login_required
def get_employees():

    return jsonify(employees), 200


# Add employee: Administrator only
@app.route("/employees", methods=["POST"])
@admin_required
def add_employee():

    data = request.get_json(silent=True) or {}

    if not all(data.get(field) for field in ["name", "department", "email"]):
        return jsonify({"error": "Name, department and email are required"}), 400

    new_employee = {
        "id": max([e["id"] for e in employees], default=0) + 1,
        "name": data["name"],
        "department": data["department"],
        "email": data["email"]
    }

    employees.append(new_employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": new_employee
    }), 201


# Update employee: Administrator only
@app.route("/employees/<int:employee_id>", methods=["PUT"])
@admin_required
def update_employee(employee_id):

    employee = next((e for e in employees if e["id"] == employee_id), None)

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}

    for field in ["name", "department", "email"]:
        if field in data:
            employee[field] = data[field]

    return jsonify({
        "message": "Employee updated successfully",
        "employee": employee
    }), 200


# Delete employee: Administrator only
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
@admin_required
def delete_employee(employee_id):

    employee = next((e for e in employees if e["id"] == employee_id), None)

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    employees.remove(employee)

    return jsonify({"message": "Employee deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
