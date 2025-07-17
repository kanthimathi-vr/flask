
# 16. Customer Complaint Portal
'''
Requirements:
- /complaint: Form (name, issue, urgency)
- POST to /complaint-submit
- Redirect to /complaint-status/<name>
- Query: /complaints?urgency=high
'''

from flask import Flask, request, redirect, url_for

app = Flask(__name__)


complaints = []


@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if request.method == 'POST':
        name = request.form.get('name')
        issue = request.form.get('issue')
        urgency = request.form.get('urgency')

        complaints.append({'name': name, 'issue': issue, 'urgency': urgency})
        return redirect(url_for('complaint_status', name=name))

    return '''
    <h2>Customer Complaint Form</h2>
    <form method="POST">
        Name: <input type="text" name="name" required><br><br>
        Issue:<br>
        <textarea name="issue" rows="4" cols="40" required></textarea><br><br>
        Urgency:
        <select name="urgency" required>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
        </select><br><br>
        <input type="submit" value="Submit Complaint">
    </form>
    '''


@app.route('/complaint-status/<name>')
def complaint_status(name):
    user = next((c for c in complaints if c['name'].lower() == name.lower()), None)
    if not user:
        return f"<h3>No complaint found for {name}</h3>"

    return f"""
    <h3>Thank you, {user['name'].title()}!</h3>
    <p>Your issue has been received: <strong>{user['issue']}</strong></p>
    <p>Urgency Level: <strong>{user['urgency'].title()}</strong></p>
    <p>We will get back to you shortly.</p>
    """


@app.route('/complaints')
def view_complaints():
    urgency = request.args.get('urgency')
    if urgency:
        filtered = [c for c in complaints if c['urgency'].lower() == urgency.lower()]
    else:
        filtered = complaints

    if not filtered:
        return "<p>No complaints found.</p>"

    html = f"<h3>Complaints{' with urgency: ' + urgency.title() if urgency else ''}</h3><ul>"
    for c in filtered:
        html += f"<li><strong>{c['name']}:</strong> {c['issue']} (Urgency: {c['urgency'].title()})</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)

