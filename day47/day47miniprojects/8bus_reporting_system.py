

# 8. Bug Reporting System
'''
Requirements:
- /report: Form with title, description, and priority (POST)
- /submit-report: Saves and redirects to /report-confirm
- /bugs?priority=high to filter reports
- /bug/<id> returns dynamic bug details
'''

from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory bug database (use a real database for production)
bug_reports = []
bug_id_counter = 1

# HTML Form Template
report_form_html = """
<h2>Bug Report Form</h2>
<form action="/submit-report" method="post">
  Title: <input type="text" name="title" required><br><br>
  Description:<br><textarea name="description" required></textarea><br><br>
  Priority:
  <select name="priority">
    <option value="low">Low</option>
    <option value="medium">Medium</option>
    <option value="high">High</option>
  </select><br><br>
  <input type="submit" value="Submit">
</form>
"""

@app.route('/report')
def report():
    return render_template_string(report_form_html)

@app.route('/submit-report', methods=['POST'])
def submit_report():
    global bug_id_counter
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    
    bug = {
        'id': bug_id_counter,
        'title': title,
        'description': description,
        'priority': priority
    }
    bug_reports.append(bug)
    bug_id_counter += 1

    return redirect(url_for('report_confirm'))

@app.route('/report-confirm')
def report_confirm():
    return "<h3>Bug report submitted successfully!</h3>"

@app.route('/bugs')
def list_bugs():
    priority_filter = request.args.get('priority')
    if priority_filter:
        filtered = [b for b in bug_reports if b['priority'] == priority_filter]
    else:
        filtered = bug_reports

    html = "<h2>Bug Reports</h2><ul>"
    for bug in filtered:
        html += f"<li><a href='/bug/{bug['id']}'>#{bug['id']} - {bug['title']} ({bug['priority']})</a></li>"
    html += "</ul>"
    return html

@app.route('/bug/<int:bug_id>')
def bug_detail(bug_id):
    bug = next((b for b in bug_reports if b['id'] == bug_id), None)
    if not bug:
        return f"<h3>No bug found with ID {bug_id}</h3>", 404
    
    return f"""
    <h2>Bug #{bug['id']}</h2>
    <strong>Title:</strong> {bug['title']}<br>
    <strong>Description:</strong><br>{bug['description']}<br>
    <strong>Priority:</strong> {bug['priority']}
    """

if __name__ == '__main__':
    app.run(debug=True)














