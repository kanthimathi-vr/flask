# 10. Daily Mood Logger
# Requirements:
# - /log-mood: Form with name, mood, and reason
# - POST to /mood-result, show mood data
# - Query route: /logs?mood=happy filters mood entries
# - Redirect to /thank-you/<name> with dynamic message

from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory mood log (would be a database in real apps)
mood_logs = []

# HTML form template
log_mood_form = """
<h2>Log Your Mood</h2>
<form action="/mood-result" method="post">
    Name: <input type="text" name="name" required><br><br>
    Mood:
    <select name="mood">
        <option value="happy">Happy</option>
        <option value="sad">Sad</option>
        <option value="angry">Angry</option>
        <option value="excited">Excited</option>
        <option value="anxious">Anxious</option>
    </select><br><br>
    Reason:<br>
    <textarea name="reason" required></textarea><br><br>
    <input type="submit" value="Submit Mood">
</form>
"""

@app.route('/log-mood')
def log_mood():
    return render_template_string(log_mood_form)

@app.route('/mood-result', methods=['POST'])
def mood_result():
    name = request.form['name']
    mood = request.form['mood']
    reason = request.form['reason']
    
    # Save entry
    mood_logs.append({'name': name, 'mood': mood, 'reason': reason})
    
    # Redirect to dynamic thank-you page
    return redirect(url_for('thank_you', name=name))

@app.route('/thank-you/<name>')
def thank_you(name):
    return f"<h3>Thank you, {name}, for sharing your mood!</h3><a href='/log-mood'>Log another mood</a>"

@app.route('/logs')
def view_logs():
    mood_filter = request.args.get('mood')
    if mood_filter:
        filtered_logs = [log for log in mood_logs if log['mood'] == mood_filter]
    else:
        filtered_logs = mood_logs

    html = f"<h2>Mood Logs{' (Filtered)' if mood_filter else ''}</h2><ul>"
    for log in filtered_logs:
        html += f"<li><strong>{log['name']}</strong> felt <em>{log['mood']}</em> because: {log['reason']}</li>"
    html += "</ul><a href='/log-mood'>Log a mood</a>"
    return html

if __name__ == '__main__':
    app.run(debug=True)



