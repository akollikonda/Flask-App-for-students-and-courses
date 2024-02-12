# Flask API Docker App

This is a simple Flask API application with Docker support. It includes functionality to manage students, courses, and student-course relationships.

## Getting Started

These instructions will help you set up and run the application locally using Docker.

### Prerequisites

- Docker installed on your machine. [Get Docker](https://docs.docker.com/get-docker/)

### Build and Run the Docker Container

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-flask-api-docker-app.git
   cd your-flask-api-docker-app

2. Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://127.0.0.1:8080.

### API Endpoints

Create Student: POST /create_student
Create Course: POST /create_course
Add Student Course: POST /add_student_course

Show all Students: GET /show_students
Show all Courses: GET /show_courses
Show Students with Courses: GET /students_with_courses
Show Students without Courses: GET /students_without_courses


### Curl command example

Create Student
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "Abhilash", "last_name": "Kollikonda"}' http://127.0.0.1:8080/create_student

Create Course
curl -X POST -H "Content-Type: application/json" -d '{"course_name": "Math 101", "course_code": "MATH101", "description": "Introduction to Mathematics"}' http://127.0.0.1:8080/create_course

Add Student course
curl -X POST -H "Content-Type: application/json" -d '{"student_id": 1, "course_id": 1}' http://127.0.0.1:8080/add_student_course

Show Students with Courses
curl http://127.0.0.1:8080/students_with_courses

Show Students without Courses
curl http://127.0.0.1:8080/students_without_courses

show students
curl http://127.0.0.1:8080/show_students

Show courses
curl http://127.0.0.1:8080/show_courses