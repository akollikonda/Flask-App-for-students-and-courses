from flask import Flask
from routes import add_student_course, create_student, create_course, get_courses, get_students, get_students_with_courses, get_students_without_courses
from database import get_db_connection

app = Flask(__name__)

# Database setup
conn = get_db_connection()
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        course_code TEXT NOT NULL,
        description TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_courses (
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id)
    )
''')
conn.commit()
conn.close()


# Register routes
app.add_url_rule('/create_student', view_func=create_student, methods=['POST'])
app.add_url_rule('/create_course', view_func=create_course, methods=['POST'])
app.add_url_rule('/students_with_courses', view_func=get_students_with_courses, methods=['GET'])
app.add_url_rule('/students_without_courses', view_func=get_students_without_courses, methods=['GET'])
app.add_url_rule('/add_student_course', view_func=add_student_course, methods=['POST'])
app.add_url_rule('/show_students', view_func=get_students, methods=['GET'])
app.add_url_rule('/show_courses', view_func=get_courses, methods=['GET'])



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8080)