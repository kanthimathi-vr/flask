from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Go to /student/<name>?age=xx&course=yyy to see the student bio."

@app.route('/student/<name>')
def student(name):
    age = request.args.get('age', 'N/A')
    course = request.args.get('course', 'N/A')
    return render_template('student.html', name=name, age=age, course=course)

if __name__ == '__main__':
    app.run(debug=True)
