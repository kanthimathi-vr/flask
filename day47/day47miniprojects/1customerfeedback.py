# 1. Customer Feedback Collector
'''
Requirements:
- /feedback-form: Shows a form to enter name, email, and message (POST)
- /submit-feedback: Handles POST, retrieves with request.form, then redirects to /thank-you
- /thank-you: Thanks the user
- /feedbacks?user=name: Reads query params to show filtered feedback
- Use dynamic route /user/<username> to show user-specific data
'''


from flask import Flask, request, redirect, url_for

app = Flask(__name__)


feedback_storage = []


@app.route('/feedback-form', methods=['GET'])
def feedback_form():
    return '''
    <h2>Customer Feedback Form</h2>
    <form method="POST" action="/submit-feedback">
        Name: <input type="text" name="name"><br><br>
        Email: <input type="email" name="email"><br><br>
        Message:<br>
        <textarea name="message" rows="5" cols="30"></textarea><br><br>
        <input type="submit" value="Submit">
    </form>
    '''

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name', 'Anonymous').strip()
    email = request.form.get('email', 'No Email').strip()
    message = request.form.get('message', '').strip()

    
    feedback_storage.append({'name': name, 'email': email, 'message': message})

    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return "<h2>Thank you for your feedback!</h2>"

@app.route('/feedbacks')
def feedbacks():
    user = request.args.get('user')
    if user:
        filtered = [fb for fb in feedback_storage if fb['name'].lower() == user.lower()]
        if not filtered:
            return f"<p>No feedback found from user: {user}</p>"
        html = f"<h3>Feedback from {user.title()}</h3><ul>"
        for fb in filtered:
            html += f"<li><strong>Email:</strong> {fb['email']}<br><strong>Message:</strong> {fb['message']}</li><br>"
        html += "</ul>"
        return html
    else:
        return "<p>Please provide a user name using ?user=name in the URL.</p>"

@app.route('/user/<username>')
def user_profile(username):
    html = f"<h2>User Profile: {username.title()}</h2>"
    feedbacks_by_user = [fb for fb in feedback_storage if fb['name'].lower() == username.lower()]
    if feedbacks_by_user:
        html += "<h3>User Feedback:</h3><ul>"
        for fb in feedbacks_by_user:
            html += f"<li>{fb['message']} (Email: {fb['email']})</li>"
        html += "</ul>"
    else:
        html += "<p>No feedback from this user yet.</p>"
    return html

if __name__ == '__main__':
    app.run(debug=True)

