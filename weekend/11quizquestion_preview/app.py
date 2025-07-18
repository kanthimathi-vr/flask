from flask import Flask, render_template, abort

app = Flask(__name__)

# Sample question database (mock)
questions = {
    "1": {
        "text": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"]
    },
    "2": {
        "text": "Which language is used for web development?",
        "options": ["Python", "HTML", "C++", "Java"]
    }
}

@app.route("/quiz/<question_id>")
def quiz_question(question_id):
    question = questions.get(question_id)
    if not question:
        abort(404)
    return render_template("quiz.html", question=question, qid=question_id)

if __name__ == "__main__":
    app.run(debug=True)
