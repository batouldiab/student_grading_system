# 🎓 Student Grading System

This is a simple web-based Student Grade Manager built using [Streamlit](https://streamlit.io). It allows users to:

- Add new students and their subject grades
- Automatically calculate each student’s average and assign a letter grade
- Modify existing student records
- View all saved student data in a table

The grades and student information are saved to a CSV file (`students_grades.csv`), which persists data between sessions.

## 🖥️ Live App

You can try out the deployed app here:  
👉 [https://studentgradingsystem.streamlit.app/](https://studentgradingsystem.streamlit.app/)

## 🛠 How It Works

The core logic of the app (`app.py`) includes:

- **Grade calculation logic** that computes an average from input grades and assigns a letter grade (A–F).
- **Data persistence** using the `pandas` library to save and update student records in a CSV file.
- **Interactive UI** built with Streamlit widgets to manage inputs and forms dynamically, including subject count and grade inputs.

## 🚀 Deployment

This app was easily deployed on [Streamlit Cloud](https://streamlit.io/) by:

1. Signing in with a GitHub account
2. Connecting the repository
3. Selecting `app.py` as the entry point
4. Clicking "Deploy"

No additional setup or hosting configuration was needed.

## 📁 Files

- `app.py`: The main Streamlit app with full functionality
- `students_grades.csv`: Stores student data (name, grades, average, letter grade)

## 📦 Requirements

To run the app locally, install the dependencies:

```bash
pip install streamlit pandas
````

Then start the app by running the following in the terminal where the file app.py exists:
```bash
streamlit run app.py
```

## 🧾 Licence

This project is open-source and free to use under the MIT License.
