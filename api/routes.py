from flask import jsonify, request
from database import get_db_connection

def create_student():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)', (data['first_name'], data['last_name']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student created successfully"}), 201

def create_course():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert course data into the database
    cursor.execute('INSERT INTO courses (course_name, course_code, description) VALUES (?, ?, ?)',
                   (data['course_name'], data['course_code'], data['description']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Course created successfully"}), 201

def add_student_course():
    data = request.get_json()

    student_id = data.get('student_id')
    course_id = data.get('course_id')

    if not student_id or not course_id:
        return jsonify({"error": "Both student_id and course_id are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if student and course exist
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course = cursor.fetchone()

    if not student or not course:
        return jsonify({"error": "Student or course not found"}), 404

    # Check if the student has already taken the course
    cursor.execute('SELECT * FROM student_courses WHERE student_id = ? AND course_id = ?', (student_id, course_id))
    existing_entry = cursor.fetchone()

    if existing_entry:
        return jsonify({"error": "Student has already taken the course"}), 409

    # Add student-course relationship
    cursor.execute('INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student successfully enrolled in the course"}), 201


def get_students_with_courses():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get students with courses
    cursor.execute('''
        SELECT students.id, first_name, last_name, GROUP_CONCAT(course_name) AS courses_taken
        FROM students
        LEFT JOIN student_courses ON students.id = student_courses.student_id
        INNER JOIN courses ON student_courses.course_id = courses.id
        GROUP BY students.id
    ''')

    students_with_courses = []
    for row in cursor.fetchall():
        student = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'courses_taken': row[3].split(',') if row[3] else []
        }
        students_with_courses.append(student)

    conn.close()
    return jsonify({"students_with_courses": students_with_courses})


def get_students_without_courses():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get students without courses
    cursor.execute('''
        SELECT id, first_name, last_name
        FROM students
        WHERE id NOT IN (SELECT DISTINCT student_id FROM student_courses)
    ''')

    students_without_courses = []
    for row in cursor.fetchall():
        student = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
        }
        students_without_courses.append(student)

    conn.close()
    return jsonify({"students_without_courses": students_without_courses})


def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get students without courses
    cursor.execute('''
        SELECT course_name,course_code,description
        FROM courses
    ''')

    courses = []
    for row in cursor.fetchall():
        course = {
            'course_name': row[0],
            'course_code': row[1],
            'description': row[2],
        }
        courses.append(course)

    conn.close()
    return jsonify({"courses_available": courses})


def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get students without courses
    cursor.execute('''
        SELECT first_name,last_name
        FROM students
    ''')

    students = []
    for row in cursor.fetchall():
        student = {
            'first_name': row[0],
            'last_name': row[1]
        }
        students.append(student)

    conn.close()
    return jsonify({"students_available": students})
