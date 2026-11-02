# Software Engineering Assignment 1

This repository contains my Software Engineering Assignment 1, developed using Python and Flask.

## Project Tasks

### Task 1: Database-Driven Flask API with Streamlit Interface
- Developed a Flask REST API using SQLite.
- Implemented CRUD operations (Create, Read, Update, Delete).
- Created a Streamlit interface for managing student records.

### Task 2: API Key Generation and Sharing
- Generated three unique API keys using Python's `secrets` module.
- Implemented API key authentication.
- Created a text-processing API that converts text into uppercase.
- Tested valid and invalid API keys.

### Task 3: Authentication and Authorization
- Developed an Employee Management API using Flask.
- Implemented login authentication.
- Added two user roles: Employee and Administrator.
- Employees can view employee records.
- Administrators can add, update, view, and delete employee records.
- Implemented role-based access control.

## Technologies Used
- Python
- Flask
- SQLite
- Streamlit
- REST API
- VS Code

## Repository Structure

```text
Software-engineering-assignment1/
│
├── Task 1/
│   ├── app.py
│   ├── frontend.py
│   ├── students.db
│   └── Demonstration Video
│
├── Task 2/
│   ├── app.py
│   └── Demonstration Video
│
├── Task 3/
│   ├── app.py
│   └── Demonstration Video
│
├── README.md
└── .gitignore
```

## How to Run

1. Install Python.
2. Install the required libraries:
   `pip install flask streamlit`
3. Open the required task folder in VS Code.
4. Run the Flask application:
   `python app.py`
5. For Task 1, run the Streamlit interface:
   `streamlit run frontend.py`

## Author
Software Engineering Student

## Conclusion
This assignment demonstrates practical implementation of Flask APIs, database operations, API key authentication, and role-based access control.
