Student Performance Tracker
Project Overview
The Student Performance Tracker is a full-stack web application designed to help teachers efficiently manage and monitor student academic performance. It provides a clean, user-friendly interface to add students, record grades for various subjects, and view detailed performance metrics. The application is built with a Python and Flask backend, uses a PostgreSQL database for persistent data storage, and is deployed on Render for easy and reliable access from any device.

Features
Student Management:

View a complete list of all registered students.

Add new students to the database with a unique roll number.

Prevents the creation of duplicate student entries.

Detailed Performance Viewing:

Click on any student to navigate to a dedicated details page.

View all subjects and corresponding grades for the selected student.

Automatically calculates and displays the student's current grade point average.

Grade Management:

Easily add new grades for any subject directly from the student's detail page.

Class-wide Statistics:

A dedicated statistics page shows the average score for each subject across the entire class.

Includes a feature to find the top-performing student for any given subject.

Technology Stack
Backend: Python, Flask

Database: PostgreSQL with SQLAlchemy ORM

Frontend: HTML, CSS
--   Version Control: Git, GitHub

Deployment: Render

Application Architecture
The application follows a simple client-server model:

User (Client): Interacts with the frontend of the application through a web browser.

Flask (Server): The backend, running on Render, handles all incoming HTTP requests, processes the application logic, and communicates with the database.

PostgreSQL (Database): The database, also hosted on Render, stores all student and grade information, ensuring data persistence.

Deployment
This application is configured for continuous deployment. The main branch of the project's GitHub repository is linked to Render. Any new commits pushed to the main branch will automatically trigger a new build and deploy the latest version of the application.

Future Enhancements
User Authentication: Implement a login system to support multiple teachers and secure data.

Data Visualization: Add charts and graphs to better visualize student and class performance trends.

Public API: Create an API to allow other services to interact with the application's data.
