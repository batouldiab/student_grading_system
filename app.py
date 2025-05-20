import streamlit as st
import pandas as pd
import os

def calculate_average(grades):
    if not grades:
        return 0
    else:
        s = sum(grades)
        avg = s / len(grades)
        return avg
    
def assign_letter_grade(avg):
    letter = 'F'
    if avg >= 60:
        letter = 'D'
    if avg >= 70:
        letter = 'C'
    if avg >= 80:
        letter = 'B'
    if avg >= 90:
        letter = 'A'
    
    return letter

def save_student_data(student_data, file_path):
    """
    write the code that gets the student data dictionary as the row to append to file.
    don't forget to handle the case if file_path doesn't exist.
    """
    df = pd.DataFrame([student_data])
    file_exists = os.path.isfile(file_path)
    if not file_exists:
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode = 'a', header=False, index=False)

    st.write("Student added successfully!")

def list_students(file_path):
    """
    write the code to print the corresponding students information from the csv file.
    if the data file exists,  it prints:
    Student Information:
       Name           Grades  Average Letter Grade
    0   s1  [4.0, 6.0, 8.0]        6            F

    if file doesn't exist, it prints:
    No data available. The student database is empty.
    """
    try:
        df = pd.read_csv(file_path)
        st.subheader("Students full list")
        st.dataframe(df)
    except FileNotFoundError:
        st.warning("No data available!")

st.title("Student Grade Manager")
file_path = "students_grades.csv"

option  = st.sidebar.radio("Choose an action:",
                           (
                              "Add a new student",
                              "Modify a student's grades",
                              "List all students" 
                           )
                           )

if 'num_subjects' not in st.session_state:
    st.session_state.num_subjects = 1

# Handle number of subjects outside form
if option == "Add a new student" or option == "Modify a student's grades":
    num_subjects = st.number_input(
        "Enter the number of subjects:", 
        min_value=1, 
        step=1,
        value=st.session_state.num_subjects,
        key="num_subjects_outside_form"
    )
    
    # Update the session state 
    if num_subjects != st.session_state.num_subjects:
        st.session_state.num_subjects = num_subjects
        # Force rerun to update the UI with new number of grade fields
        st.rerun()

if option == "Add a new student":
    with st.form("add_student_form"):
        # Get student name
        student_name = st.text_input("Enter the student's name:")

        st.write(f"Number of subejcts: {st.session_state.num_subjects}")
        grades = []
        for i in range(1, st.session_state.num_subjects + 1):
            grade = st.number_input(
                f"Enter the grade for subject {i}",
                min_value=0,
                step = 1,
                key = f"add_grade_{i}"
            )
            grades.append(grade)

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not student_name:
                st.error("Enter student name")

            elif len(grades) != st.session_state.num_subjects:
                st.error("Enter all grades!")

            else:
                avg = calculate_average(grades)
                letter = assign_letter_grade(avg)
                student = {
                    'Name': student_name,
                    'Grades': grades,
                    'Average': avg,
                    'Letter Grade': letter
                }
                save_student_data(student, file_path)

if option == "Modify a student's grades":
    st.write("page: Modify a student's grades was chosen")

if option == "List all students":
    list_students(file_path)
