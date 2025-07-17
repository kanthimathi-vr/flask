

# 7. University Course Search & Registration
'''
Requirements:
- /courses: Show list, allow filtering using /courses?dept=CS
- /register: Show POST form (student name, course code)
- /confirm-registration/<name>: Show personalized message
- Use request.form, and url_for() redirection
'''

from flask import Flask, request, redirect, url_for

app = Flask(__name__)


courses = [
    {'code': 'CS101', 'name': 'Intro to Computer Science', 'dept': 'CS'},
    {'code': 'CS201', 'name': 'Data Structures', 'dept': 'CS'},
    {'code': 'MATH101', 'name': 'Calculus I', 'dept': 'Math'},
    {'code': 'ENG101', 'name': 'English Literature', 'dept': 'English'},
]


@app.route('/courses')
def list_courses():
    dept = request.args.get('dept', '').upper()
    filtered = [c for c in courses if c['dept'].upper() == dept] if dept else courses

    html = "<h2>Available Courses</h2>"
    if dept:
        html += f"<p>Filtering by department: <strong>{dept}</strong></p>"
    html += "<ul>"
    for c in filtered:
        html += f"<li>{c['code']} - {c['name']} ({c['dept']})</li>"
    html += "</ul>"

    html += '''
    <p>Filter by department: 
        <a href="/courses?dept=CS">CS</a> | 
        <a href="/courses?dept=Math">Math</a> | 
        <a href="/courses">All</a>
    </p>'''
    return html


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student = request.form.get('student', 'Student')
        course_code = request.form.get('course_code', '').upper()

       

        return redirect(url_for('confirm_registration', name=student))
    
    return '''
    <h2>Course Registration</h2>
    <form method="POST">
        Student Name: <input type="text" name="student" required><br><br>
        Course Code: <input type="text" name="course_code" required><br><br>
        <input type="submit" value="Register">
    </form>
    '''


@app.route('/confirm-registration/<name>')
def confirm_registration(name):
    return f"<h3>Thank you, {name.title()}! Your registration was successful.</h3>"


if __name__ == '__main__':
    app.run(debug=True)
