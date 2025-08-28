# 1. Update this import line
from flask import Flask, render_template, request, redirect, url_for
from tracker import StudentTracker, setup_database

app = Flask(__name__)

setup_database()
tracker = StudentTracker()


@app.route('/')
def index():
    all_students = tracker.get_all_students()
    return render_template('index.html', students=all_students)


# 2. Add this new route to handle the form submission
@app.route('/add', methods=['POST'])
def add_student():
    # Get the data from the form
    name = request.form['name']
    roll_number = request.form['roll_number']

    # Use your existing tracker method to add the student
    tracker.add_student(name, roll_number)

    # Redirect back to the home page to see the updated list
    return redirect(url_for('index'))
@app.route('/student/<roll_number>')
def student_details(roll_number):
    # Get the student data using your modified method
    details = tracker.view_student_details(roll_number)
    if details:
        return render_template('student_details.html', student=details)
    else:
        return "Student not found!", 404


@app.route('/student/<roll_number>/add_grade', methods=['POST'])
def add_grade(roll_number):
    # Get the data from the form
    subject = request.form['subject']
    try:
        grade = int(request.form['grade'])
        # Use your existing tracker method to add the grade
        tracker.add_grade_for_student(roll_number, subject, grade)
    except ValueError:
        # Handle cases where grade is not a valid number (optional)
        print("Invalid grade entered.")

    # Redirect back to the student's details page to see the new grade
    return redirect(url_for('student_details', roll_number=roll_number))
if __name__ == '__main__':
    app.run(debug=True)