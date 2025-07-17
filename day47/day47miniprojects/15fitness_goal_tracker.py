# 15. Fitness Goal Tracker
'''
Requirements:
- /goal: Form with name, goal (e.g., weight loss)
- POST data to /goal-submit
- Redirect to /goal-status/<name>
- /goals?type=weight filters with query parameters
'''


from flask import Flask, request, redirect, url_for

app = Flask(__name__)


goals = []


@app.route('/goal', methods=['GET', 'POST'])
def goal():
    if request.method == 'POST':
        name = request.form.get('name')
        goal_type = request.form.get('goal')

        goals.append({'name': name, 'goal': goal_type})
        return redirect(url_for('goal_status', name=name))
    
    return '''
    <h2>Fitness Goal Tracker</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br><br>
        Fitness Goal:
        <select name="goal" required>
            <option value="weight loss">Weight Loss</option>
            <option value="muscle gain">Muscle Gain</option>
            <option value="endurance">Endurance</option>
            <option value="flexibility">Flexibility</option>
        </select><br><br>
        <input type="submit" value="Set Goal">
    </form>
    '''


@app.route('/goal-status/<name>')
def goal_status(name):
    user_goal = next((g for g in goals if g['name'].lower() == name.lower()), None)
    if not user_goal:
        return f"<h3>No goal found for {name}.</h3>"
    return f"<h3>{user_goal['name'].title()}, your goal is: <strong>{user_goal['goal'].title()}</strong>.</h3>"


@app.route('/goals')
def goal_filter():
    goal_type = request.args.get('type')
    if goal_type:
        filtered = [g for g in goals if goal_type.lower() in g['goal'].lower()]
    else:
        filtered = goals

    if not filtered:
        return f"<p>No goals found for type: {goal_type}</p>"

    html = f"<h3>Goals{' - ' + goal_type.title() if goal_type else ''}</h3><ul>"
    for g in filtered:
        html += f"<li>{g['name']} → {g['goal'].title()}</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)
