from flask import Flask, render_template

app = Flask(__name__)

@app.route("/courses")
def courses():
    course_list = [
        {
            "title": "Intro to Python",
            "instructor": "John Doe",
            "duration": "4 weeks",
            "level": "beginner"
        },
        {
            "title": "Flask Web Development",
            "instructor": "Jane Smith",
            "duration": "6 weeks",
            "level": "intermediate"
        },
        {
            "title": "Advanced Machine Learning",
            "instructor": "Dr. AI",
            "duration": "8 weeks",
            "level": "advanced"
        }
    ]
    return render_template("courses.html", title="Courses", courses=course_list)

if __name__ == "__main__":
    app.run(debug=True)
