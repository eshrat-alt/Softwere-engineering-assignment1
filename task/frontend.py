
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Student Management System", page_icon="🎓")

st.title("🎓 Student Management System")
st.write("Manage student records using Flask API and Streamlit.")

# Display all students
st.subheader("All Students")

if st.button("Refresh Students"):
    st.rerun()

response = requests.get(f"{API_URL}/students")

if response.status_code == 200:
    students = response.json()

    if students:
        st.dataframe(pd.DataFrame(students), use_container_width=True)
    else:
        st.info("No students found.")
else:
    st.error("Unable to fetch students.")

# Add a new student
st.subheader("Add New Student")

with st.form("add_student_form"):
    name = st.text_input("Student Name")
    department = st.text_input("Department")
    email = st.text_input("Email")

    add_button = st.form_submit_button("Add Student")

    if add_button:
        data = {
            "name": name,
            "department": department,
            "email": email
        }

        result = requests.post(f"{API_URL}/students", json=data)

        if result.status_code == 201:
            st.success("Student added successfully!")
            st.rerun()
        else:
            st.error(result.json().get("error", "Unable to add student."))

# Update an existing student
st.subheader("Update Student")

student_id = st.number_input("Enter Student ID to Update", min_value=1, step=1)

with st.form("update_student_form"):
    new_name = st.text_input("New Student Name")
    new_department = st.text_input("New Department")
    new_email = st.text_input("New Email")

    update_button = st.form_submit_button("Update Student")

    if update_button:
        data = {
            "name": new_name,
            "department": new_department,
            "email": new_email
        }

        result = requests.put(
            f"{API_URL}/students/{student_id}",
            json=data
        )

        if result.status_code == 200:
            st.success("Student updated successfully!")
            st.rerun()
        else:
            st.error(result.json().get("error", "Unable to update student."))

# Delete a student
st.subheader("Delete Student")

delete_id = st.number_input("Enter Student ID to Delete", min_value=1, step=1, key="delete_id")

if st.button("Delete Student"):
    result = requests.delete(f"{API_URL}/students/{delete_id}")

    if result.status_code == 200:
        st.success("Student deleted successfully!")
        st.rerun()
    else:
        st.error(result.json().get("error", "Student not found."))
