

# 5. Contact Us with Department Selection
'''
Requirements:
- /contact: Show GET form (name, email, message, department)
- /submit: Handle POST, redirect with flash message to /contact/thank-you
- Use request.form for data, request.args for query param like /submit?source=homepage
- /contact/<department> - dynamic route for each department
'''

from flask import Flask, request, redirect, url_for, flash, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 


contact_form_html = '''
<!DOCTYPE html>
<html>
<head><title>Contact Us</title></head>
<body>
    <h2>Contact Us</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul style="color: green;">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="POST" action="/submit?source=homepage">
        Name: <input type="text" name="name" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        Department:
        <select name="department">
            <option value="support">Support</option>
            <option value="sales">Sales</option>
            <option value="hr">HR</option>
        </select><br><br>
        Message:<br>
        <textarea name="message" rows="5" cols="30" required></textarea><br><br>
        <input type="submit" value="Send">
    </form>
</body>
</html>
'''

thank_you_html = '''
<!DOCTYPE html>
<html>
<head><title>Thank You</title></head>
<body>
    <h3>Thank you for contacting us!</h3>
    <p>We’ll get back to you soon.</p>
</body>
</html>
'''


@app.route('/contact')
def contact_form():
    return render_template_string(contact_form_html)


@app.route('/submit', methods=['POST'])
def submit_contact():
    name = request.form.get('name', 'Anonymous')
    email = request.form.get('email')
    message = request.form.get('message')
    department = request.form.get('department', 'general')

    
    source = request.args.get('source', 'unknown')

    print(f"[Contact Submission] From: {name}, Email: {email}, Dept: {department}, Source: {source}")
    print(f"Message: {message}")

    
    flash(f"Thank you, {name}, your message was sent to {department.upper()}!")

    return redirect(url_for('thank_you'))


@app.route('/contact/thank-you')
def thank_you():
    return render_template_string(thank_you_html)


@app.route('/contact/<department>')
def contact_department(department):
    contact_emails = {
        'support': 'support@example.com',
        'sales': 'sales@example.com',
        'hr': 'hr@example.com'
    }
    email = contact_emails.get(department.lower(), 'info@example.com')
    return f"<h3>Contact {department.title()} Department</h3><p>Email: {email}</p>"


if __name__ == '__main__':
    app.run(debug=True)
