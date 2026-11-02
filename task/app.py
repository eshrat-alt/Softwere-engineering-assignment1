

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create students table
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


create_table()


# Home route
@app.route("/")
def home():
    return "Student Management API is Running!"


# GET API - Retrieve all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    student_list = [dict(student) for student in students]
    return jsonify(student_list), 200


# POST API - Add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    name = data.get("name")
    department = data.get("department")
    email = data.get("email")

    if not name or not department or not email:
        return jsonify({"error": "Name, department and email are required"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
        (name, department, email)
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student added successfully!",
        "student_id": student_id
    }), 201


# GET API - Retrieve a student by ID
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student)), 200


# PUT API - Update an existing student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    name = data.get("name")
    department = data.get("department")
    email = data.get("email")

    if not name or not department or not email:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    if student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute(
        "UPDATE students SET name = ?, department = ?, email = ? WHERE id = ?",
        (name, department, email, id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Student updated successfully!"}), 200


# DELETE API - Delete a student by ID
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()

    if student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted successfully!"}), 200


# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)
