import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Get the database URL from the environment variable.
# Render will set this automatically. For local use, you'll create a .env file.
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL is not set.")

# SQLAlchemy requires a small change to the URL for compatibility.
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --- DATABASE MODELS ---
class Student(db.Model):
    roll_number = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grades = db.relationship('Grade', backref='student', cascade="all, delete-orphan")


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    student_roll_number = db.Column(db.String(50), db.ForeignKey('student.roll_number'), nullable=False)


# Create tables in the database if they don't exist
with app.app_context():
    db.create_all()


# --- WEB ROUTES ---
@app.route('/')
def index():
    all_students = Student.query.order_by(Student.name).all()
    return render_template('index.html', students=all_students)


@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll_number = request.form['roll_number']

    existing_student = Student.query.get(roll_number)
    if not existing_student:
        new_student = Student(name=name, roll_number=roll_number)
        db.session.add(new_student)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/student/<roll_number>')
def student_details(roll_number):
    student = Student.query.get(roll_number)
    if student:
        total_score = sum(g.grade for g in student.grades)
        average = total_score / len(student.grades) if student.grades else 0.0
        return render_template('student_details.html', student=student, average=average)
    return "Student not found!", 404


@app.route('/student/<roll_number>/add_grade', methods=['POST'])
def add_grade(roll_number):
    student = Student.query.get(roll_number)
    if student:
        subject = request.form['subject']
        try:
            grade_value = int(request.form['grade'])
            if 0 <= grade_value <= 100:
                new_grade = Grade(subject=subject, grade=grade_value, student_roll_number=roll_number)
                db.session.add(new_grade)
                db.session.commit()
        except ValueError:
            print("Invalid grade entered.")
    return redirect(url_for('student_details', roll_number=roll_number))


if __name__ == '__main__':
    app.run(debug=True)