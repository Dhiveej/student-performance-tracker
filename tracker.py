import sqlite3


def setup_database():
    """Creates the database file and tables if they don't exist."""
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()

    # Create the 'students' table to store student info
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS students
                   (
                       roll_number
                       TEXT
                       PRIMARY
                       KEY,
                       name
                       TEXT
                       NOT
                       NULL
                   )
                   ''')

    # Create the 'grades' table to store grades for each student
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS grades
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       student_roll_number
                       TEXT
                       NOT
                       NULL,
                       subject
                       TEXT
                       NOT
                       NULL,
                       grade
                       INTEGER
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       student_roll_number
                   ) REFERENCES students
                   (
                       roll_number
                   )
                       )
                   ''')

    conn.commit()
    conn.close()


class StudentTracker:
    def __init__(self, db_name='student_performance.db'):
        """Initializes the tracker by setting the database file name."""
        self.db_name = db_name

    def add_student(self, name, roll_number):
        """Adds a student to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (roll_number, name) VALUES (?, ?)", (roll_number, name))
            conn.commit()
            print(f"Student '{name}' with roll number {roll_number} added successfully.")
        except sqlite3.IntegrityError:
            print(f"Error: Student with roll number {roll_number} already exists.")
        finally:
            conn.close()

    def add_grade_for_student(self, roll_number, subject, grade):
        """Finds a student in the DB and adds a grade to their record."""
        # [cite_start]This function handles adding grades for each student [cite: 93]
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # First, check if the student exists
        cursor.execute("SELECT name FROM students WHERE roll_number = ?", (roll_number,))
        student = cursor.fetchone()

        if student:
            if 0 <= grade <= 100:  # [cite_start]Use conditionals to ensure grades are valid (e.g., between 0 and 100). [cite: 107]
                cursor.execute("INSERT INTO grades (student_roll_number, subject, grade) VALUES (?, ?, ?)",
                               (roll_number, subject, grade))
                conn.commit()
                print(f"Grade {grade} for {subject} added for roll number {roll_number}.")
            else:
                print("Invalid Grade. Please enter a value between 0 and 100.")
        else:
            # [cite_start]Handle cases where the student is not found [cite: 108]
            print(f"Error: Student with roll number {roll_number} not found.")
        conn.close()



    def get_all_students(self):
        """Fetches all students from the database."""
        conn = sqlite3.connect(self.db_name)
        # This makes the cursor return rows that can be accessed like dictionaries
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT roll_number, name FROM students ORDER BY name")
        students = cursor.fetchall()

        conn.close()
        return students

    def view_student_details(self, roll_number):
        """Fetches and returns all details for a specific student."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Fetch student details
        cursor.execute("SELECT name FROM students WHERE roll_number = ?", (roll_number,))
        student_record = cursor.fetchone()

        if student_record:
            # Fetch all grades for that student
            cursor.execute("SELECT subject, grade FROM grades WHERE student_roll_number = ?", (roll_number,))
            grades_records = cursor.fetchall()
            conn.close()

            # Calculate average
            total_score = sum(grade['grade'] for grade in grades_records)
            average = total_score / len(grades_records) if grades_records else 0.0

            # Return all data in a dictionary
            return {
                'name': student_record['name'],
                'roll_number': roll_number,
                'grades': grades_records,
                'average': average
            }
        else:
            conn.close()
            return None  # Return None if student not found


def main():
    """Main function to run the student performance tracker application."""
    setup_database()  # Ensure the database and tables are ready
    tracker = StudentTracker()

    # [cite_start]Use a loop to provide a menu-driven interface [cite: 110]
    while True:
        print("\nStudent Performance Tracker")
        print("1. Add Student")
        print("2. Add Grade for Student")
        print("3. View Student Details")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            name = input("Enter student's name: ")
            roll_number = input("Enter student's roll number: ")
            tracker.add_student(name, roll_number)

        elif choice == '2':
            roll_number = input("Enter student's roll number to add grade: ")
            subject = input("Enter subject: ")
            try:
                grade = int(input("Enter grade (0-100): "))
                tracker.add_grade_for_student(roll_number, subject, grade)
            except ValueError:
                print("Invalid input. Please enter a numeric grade.")

        elif choice == '3':
            roll_number = input("Enter student's roll number to view details: ")
            tracker.view_student_details(roll_number)

        elif choice == '4':
            print("Exiting application. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()