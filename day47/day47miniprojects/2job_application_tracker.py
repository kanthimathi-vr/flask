

# 2. Job Application Tracker
'''
Requirements:
- /apply: Displays a form (name, email, position) – POST to /submit-application
- /submit-application: Reads data using request.form, redirects to /application-status
- /application-status: Returns confirmation
- /applications?position=Python filters by position using request.args
- Add dynamic route /applicant/<name> to display individual applicant
'''


from flask import Flask, request, redirect, url_for

app = Flask(__name__)


applications = []


@app.route('/apply', methods=['GET'])
def apply():
    return '''
    <h2>Job Application Form</h2>
    <form method="POST" action="/submit-application">
        Name: <input type="text" name="name"><br><br>
        Email: <input type="email" name="email"><br><br>
        Position:
        <select name="position">
            <option value="Python">Python Developer</option>
            <option value="JavaScript">JavaScript Developer</option>
            <option value="Designer">UI/UX Designer</option>
        </select><br><br>
        <input type="submit" value="Apply">
    </form>
    '''


@app.route('/submit-application', methods=['POST'])
def submit_application():
    name = request.form.get('name', 'Unknown').strip()
    email = request.form.get('email', 'No Email').strip()
    position = request.form.get('position', 'Not specified').strip()

    applications.append({
        'name': name,
        'email': email,
        'position': position
    })

    return redirect(url_for('application_status'))


@app.route('/application-status')
def application_status():
    return "<h3>Your application has been received. Thank you!</h3>"


@app.route('/applications')
def application_list():
    position_filter = request.args.get('position')
    if position_filter:
        filtered = [app for app in applications if app['position'].lower() == position_filter.lower()]
        if not filtered:
            return f"<p>No applications found for position: {position_filter}</p>"
        html = f"<h3>Applications for {position_filter}:</h3><ul>"
        for app in filtered:
            html += f"<li>{app['name']} - {app['email']}</li>"
        html += "</ul>"
        return html
    else:
        return "<p>Please use <code>?position=PositionName</code> to filter applications.</p>"


@app.route('/applicant/<name>')
def applicant_profile(name):
    applicant_data = [app for app in applications if app['name'].lower() == name.lower()]
    if not applicant_data:
        return f"<h3>No applications found for {name}</h3>"
    html = f"<h3>Applications by {name.title()}:</h3><ul>"
    for app in applicant_data:
        html += f"<li>Email: {app['email']}, Position: {app['position']}</li>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    app.run(debug=True)

