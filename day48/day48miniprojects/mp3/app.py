from flask import Flask, render_template

app = Flask(__name__)

@app.route("/result")
def result():
    student = {
        "name": "John Doe",
        "grade": "B",
        "subjects": [
            {"name": "Math", "marks": 85},
            {"name": "Science", "marks": 78},
            {"name": "History", "marks": 90},
            {"name": "English", "marks": 88},
        ]
    }
    return render_template("result.html", title="Student Result Dashboard", student=student)

if __name__ == "__main__":
    app.run(debug=True)
