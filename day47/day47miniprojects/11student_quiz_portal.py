# 11. Student Quiz Portal
# Requirements:
# - /quiz: Form with name and 3 MCQ questions
# - POST to /quiz-result and display answers
# - Redirect using url_for() to /quiz-summary/<name>
# - Filter score with /leaderboard?score=10
 

from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory leaderboard (name + score)
leaderboard = []

# Quiz form HTML
quiz_form = """
<h2>Student Quiz</h2>
<form action="/quiz-result" method="post">
  Name: <input type="text" name="name" required><br><br>
  
  <strong>1. What is the capital of France?</strong><br>
  <input type="radio" name="q1" value="Paris" required> Paris<br>
  <input type="radio" name="q1" value="London"> London<br>
  <input type="radio" name="q1" value="Berlin"> Berlin<br><br>
  
  <strong>2. 5 + 7 = ?</strong><br>
  <input type="radio" name="q2" value="12" required> 12<br>
  <input type="radio" name="q2" value="10"> 10<br>
  <input type="radio" name="q2" value="14"> 14<br><br>

  <strong>3. Which planet is known as the Red Planet?</strong><br>
  <input type="radio" name="q3" value="Mars" required> Mars<br>
  <input type="radio" name="q3" value="Jupiter"> Jupiter<br>
  <input type="radio" name="q3" value="Venus"> Venus<br><br>

  <input type="submit" value="Submit Quiz">
</form>
"""

# Correct answers
correct_answers = {
    "q1": "Paris",
    "q2": "12",
    "q3": "Mars"
}

@app.route('/quiz')
def quiz():
    return render_template_string(quiz_form)

@app.route('/quiz-result', methods=['POST'])
def quiz_result():
    name = request.form['name']
    score = 0

    # Check answers
    for key in correct_answers:
        if request.form.get(key) == correct_answers[key]:
            score += 1

    # Save to leaderboard
    leaderboard.append({'name': name, 'score': score})

    # Redirect to summary page
    return redirect(url_for('quiz_summary', name=name))

@app.route('/quiz-summary/<name>')
def quiz_summary(name):
    user = next((entry for entry in leaderboard if entry['name'] == name), None)
    if not user:
        return f"<h3>No quiz found for {name}</h3>", 404
    return f"""
    <h2>Quiz Summary for {name}</h2>
    <p>Your score: {user['score']} / 3</p>
    <a href="/quiz">Take Again</a> | <a href="/leaderboard">View Leaderboard</a>
    """

@app.route('/leaderboard')
def show_leaderboard():
    score_filter = request.args.get('score')
    if score_filter:
        try:
            score_filter = int(score_filter)
            filtered = [entry for entry in leaderboard if entry['score'] == score_filter]
        except ValueError:
            filtered = []
    else:
        filtered = leaderboard

    html = f"<h2>Leaderboard {'(Filtered)' if score_filter is not None else ''}</h2><ul>"
    for entry in filtered:
        html += f"<li>{entry['name']}: {entry['score']} / 3</li>"
    html += "</ul><a href='/quiz'>Back to Quiz</a>"
    return html

if __name__ == '__main__':
    app.run(debug=True)
