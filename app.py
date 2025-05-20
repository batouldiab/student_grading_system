import streamlit as st
import pandas as pd
import os

# --- Helper Functions ---
def calculate_average(grades):
    if not grades:
        return 0
    return sum(grades) / len(grades)

def assign_letter_grade(average):
    letter = 'F'
    if average >= 60:
        letter = 'D'
    if average >= 70:
        letter = 'C'
    if average >= 80:
        letter = 'B'
    if average >= 90:
        letter = 'A'
    return letter

def save_student_data(student_data, file_path):
    df = pd.DataFrame(student_data)
    file_exists = os.path.isfile(file_path)
    if not file_exists:
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', index=False, header=False)

def modify_student_data(student_name, new_grades, file_path):
    if not os.path.isfile(file_path):
        return False, "Student database not found."

    df = pd.read_csv(file_path)
    if student_name in df['Name'].values:
        avg = calculate_average(new_grades)
        letter = assign_letter_grade(avg)
        df.loc[df['Name'] == student_name, 'Grades'] = str(new_grades)
        df.loc[df['Name'] == student_name, 'Average'] = avg
        df.loc[df['Name'] == student_name, 'Letter Grade'] = letter
        df.to_csv(file_path, index=False)
        return True, f"Student {student_name}'s grades have been updated."
    else:
        return False, f"No student found with the name {student_name}."

def list_students(file_path):
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        st.subheader("Student Information:")
        st.dataframe(df)
    else:
        st.warning("No data available. The student database is empty.")

# --- Streamlit App ---
st.title("🎓 Student Grade Manager")
file_path = "students_grades.csv"

# Sidebar for navigation
option = st.sidebar.radio("Choose an action:", (
    "Add a new student", 
    "Modify a student's grades", 
    "List all students")
)

# Initialize session state for subject count
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

# Option 1: Add new student
if option == "Add a new student":
    with st.form("add_student_form"):
        student_name = st.text_input("Enter the student's name:")
        
        # Display the currently selected number of subjects (readonly)
        st.write(f"Number of subjects: {st.session_state.num_subjects}")
        
        # Dynamically create grade inputs based on session state
        grades = []
        for i in range(st.session_state.num_subjects):
            grade = st.number_input(
                f"Enter grade for subject {i+1}:", 
                min_value=0.0, 
                step=1.0,
                key=f"add_grade_{i}"
            )
            grades.append(grade)
        
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not student_name:
            st.error("Please enter a student name.")
        elif len(grades) != st.session_state.num_subjects:
            st.error(f"Please ensure you've entered all {st.session_state.num_subjects} grades.")
        else:
            avg = calculate_average(grades)
            letter = assign_letter_grade(avg)
            student = {
                'Name': [student_name],
                'Grades': [str(grades)],
                'Average': [avg],
                'Letter Grade': [letter]
            }
            save_student_data(student, file_path)
            st.success(f"Student {student_name} added successfully!")

# # Option 2: Modify student's grades
# elif option == "Modify a student's grades":
#     with st.form("modify_student_form"):
#         # student_name = st.text_input("Enter the student's name to modify:")
#         if os.path.isfile(file_path):
#             df = pd.read_csv(file_path)
#             student_names = df['Name'].unique().tolist()
#             student_name = st.selectbox("Select a student to modify:", student_names)
#         else:
#             st.warning("No student data found.")
#             student_name = None
        
#         # Display the currently selected number of subjects (readonly)
#         st.write(f"Number of subjects: {st.session_state.num_subjects}")
        
#         # Dynamically create grade inputs based on session state
#         new_grades = []
#         for i in range(st.session_state.num_subjects):
#             grade = st.number_input(
#                 f"Enter grade for subject {i+1}:", 
#                 min_value=0.0, 
#                 step=1.0,
#                 key=f"mod_grade_{i}"
#             )
#             new_grades.append(grade)
        
#         submitted = st.form_submit_button("Submit Changes")

#     if submitted:
#         if not student_name:
#             st.error("Please enter a student name.")
#         elif len(new_grades) != st.session_state.num_subjects:
#             st.error(f"Please ensure you've entered all {st.session_state.num_subjects} grades.")
#         else:
#             success, message = modify_student_data(student_name, new_grades, file_path)
#             if success:
#                 st.success(message)
#             else:
#                 st.error(message)

elif option == "Modify a student's grades":

    def update_subject_count():
        selected_name = st.session_state.get("selected_student_name")
        if selected_name and os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            student_row = df[df['Name'] == selected_name]
            if not student_row.empty:
                try:
                    grades = eval(student_row.iloc[0]['Grades'])
                    st.session_state.num_subjects = len(grades)
                except:
                    st.session_state.num_subjects = 1

    # 🔷 Step 1: Student selector OUTSIDE the form so we can use on_change
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        student_names = df['Name'].unique().tolist()

        st.selectbox(
            "Select a student to modify:",
            student_names,
            key="selected_student_name",
            on_change=update_subject_count
        )
        student_name = st.session_state.get("selected_student_name")
    else:
        st.warning("No student data found.")
        student_name = None

    # 🔷 Step 2: Form starts here
    with st.form("modify_student_form"):
        if student_name:
            # Load and parse the student's current grades
            student_row = df[df['Name'] == student_name].iloc[0]
            try:
                prefilled_grades = eval(student_row['Grades'])
                if len(prefilled_grades) < st.session_state.num_subjects:
                    prefilled_grades += [0.0] * (st.session_state.num_subjects - len(prefilled_grades))
                elif len(prefilled_grades) > st.session_state.num_subjects:
                    prefilled_grades = prefilled_grades[:st.session_state.num_subjects]
            except Exception:
                prefilled_grades = [0.0] * st.session_state.num_subjects

            st.write(f"Number of subjects: {st.session_state.num_subjects}")
            new_grades = []
            for i in range(st.session_state.num_subjects):
                grade = st.number_input(
                    f"Enter grade for subject {i+1}:",
                    min_value=0.0,
                    step=1.0,
                    value=prefilled_grades[i],
                    key=f"mod_grade_{i}"
                )
                new_grades.append(grade)

            submitted = st.form_submit_button("Submit Changes")

            if submitted:
                if len(new_grades) != st.session_state.num_subjects:
                    st.error(f"Please enter all {st.session_state.num_subjects} grades.")
                else:
                    success, message = modify_student_data(student_name, new_grades, file_path)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)



# Option 3: List students
elif option == "List all students":
    list_students(file_path)