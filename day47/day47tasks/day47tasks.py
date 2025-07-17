# URL Routing and Dynamic Parameters (/<name>) – 15 Tasks

from flask import Flask, abort, request, render_template_string,redirect,url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Day 47 tasks</h1>"
# 1. Create a route /hello/<name> that returns “Hello, [name]!”
@app.route('/hello/<name>')
def hello(name):
    return f"Hello, {name}!"

# 2. Add a route /square/<int:number> that returns the square of a number
@app.route('/square/<int:number>')
def square(number):
    return f"The square of {number} is {number ** 2}"

# 3. Create a route /greet/<name>/<int:age> that returns a greeting message using both parameters
@app.route('/greet/<name>/<int:age>')
def greet(name, age):
    return f"Hi {name}, you are {age} years old."

# 4. Add a route /status/<username>/<status> to simulate a user’s status update
@app.route('/status/<username>/<status>')
def status(username, status):
    return f"{username} is currently {status}"

# 5. Add route /price/<float:amount> to show price values with decimals
@app.route('/price/<float:amount>')
def price(amount):
    return f"The price is ${amount:.2f}"

# 6. Build a /profile/<username> route that returns a mini user profile in HTML
@app.route('/profile/<username>')
def profile(username):
    return f"""
    <h2>User Profile</h2>
    <p><strong>Username:</strong> {username}</p>
    """

# 7. Handle /math/<int:x>/<int:y> to return their sum, difference, and product
@app.route('/math/<int:x>/<int:y>')
def math(x, y):
    return f"""
    Sum: {x + y}<br>
    Difference: {x - y}<br>
    Product: {x * y}
    """

# 8. Add /file/<path:filename> to demonstrate the path converter
@app.route('/file/<path:filename>')
def file_path(filename):
    return f"You requested the file: {filename}"

# 9. Use <string:color> in route /color/<color> to return an HTML response with that color text
@app.route('/color/<string:color>')
def color_text(color):
    return f"<p style='color:{color}'>This is {color} text.</p>"

# 10. Validate if a dynamic parameter is in a list (e.g., /language/<lang>)
@app.route('/language/<lang>')
def language(lang):
    supported = ['python', 'java', 'javascript']
    if lang.lower() in supported:
        return f"{lang.title()} is a supported language."
    else:
        return f"{lang.title()} is not supported."

# 11. Return “User not found” if the username doesn’t match predefined names
@app.route('/user/<username>')
def check_user(username):
    known_users = ['admin', 'trainer', 'student']
    if username.lower() in known_users:
        return f"Welcome, {username}!"
    else:
        return "User not found", 404

# 12. Create /country/<code> and return full name from a hardcoded dictionary
@app.route('/country/<code>')
def country(code):
    countries = {
        'us': 'United States',
        'in': 'India',
        'uk': 'United Kingdom',
        'ca': 'Canada'
    }
    name = countries.get(code.lower())
    if name:
        return f"Country code '{code.upper()}' stands for {name}."
    else:
        return "Unknown country code", 404

# 13. Add a debug print of the parameter inside the route function
@app.route('/debug/<info>')
def debug(info):
    print(f"[DEBUG] Info received: {info}")
    return f"Debug info printed to console: {info}"


# 14. Use triple-quoted strings to format an HTML output with dynamic values
@app.route('/html/<title>/<content>')
def html_output(title, content):
    return f"""
    <html>
        <head><title>{title}</title></head>
        <body>
            <h1>{title}</h1>
            <p>{content}</p>
        </body>
    </html>
    """

# 15. Create an error route /error/<code> that shows a message based on the status code
@app.route('/error/<int:code>')
def error_route(code):
    messages = {
        404: "Page not found.",
        500: "Internal server error.",
        403: "Access denied.",
        400: "Bad request."
    }
    msg = messages.get(code, "Unknown error.")
    return f"Error {code}: {msg}", code
# Handling GET & POST Requests – 10 Tasks
#1. Create a route /method-check that returns the current HTTP method
@app.route('/method-check', methods=['GET', 'POST'])
def method_check():
    return f"Current HTTP Method: {request.method}"

#2. Add route /submit that allows only POST, and returns confirmation message

@app.route('/submit', methods=['POST'])
def submit():
    return "POST request received and processed!"

#3. Add route /both-methods that supports both GET and POST, return the method used
@app.route('/both-methods', methods=['GET', 'POST'])
def both_methods():
    return f"Received a {request.method} request."

#4. Display a form at /login with method POST
#5. On form submission to /login, return the entered username
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        return f"Welcome, {username}!"
    return '''
    <form method="POST" action="/login">
        Username: <input type="text" name="username">
        <input type="submit" value="Login">
    </form>
    '''

#6. Restrict route /admin to only GET and return a warning if POST is used
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        return "POST not allowed on /admin", 405
    return "Welcome to the admin panel (GET only)."

#7. Print the method in the console during every request
@app.before_request
def log_request_method():
    print(f"[LOG] HTTP Method: {request.method} on {request.path}")


#8. Create a form at /feedback with a textarea and POST it to /submit-feedback
#9. Create a button that submits a POST request using an HTML form
@app.route('/feedback', methods=['GET'])
def feedback():
    return '''
    <form method="POST" action="/submit-feedback">
        <textarea name="message" rows="5" cols="30" placeholder="Your feedback"></textarea><br>
        <button type="submit">Submit Feedback</button>
    </form>
    '''

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    message = request.form.get('message')
    return f"Feedback received: {message}"

#10. Add HTML form with both GET and POST method options and observe the difference
@app.route('/method-form', methods=['GET', 'POST'])
def method_form():
    if request.method == 'POST':
        return f"POST data: {request.form.get('data')}"
    elif request.method == 'GET' and 'data' in request.args:
        return f"GET data: {request.args.get('data')}"
    return '''
    <h3>Submit with GET</h3>
    <form method="GET" action="/method-form">
        <input type="text" name="data" placeholder="Enter something">
        <input type="submit" value="Submit via GET">
    </form>

    <h3>Submit with POST</h3>
    <form method="POST" action="/method-form">
        <input type="text" name="data" placeholder="Enter something">
        <input type="submit" value="Submit via POST">
    </form>
    '''

# Using request.args for Query Parameters – 10 Tasks
# 1. Create a route /search that reads a keyword from query parameters (?keyword=flask)
# 3. Return “No keyword found” if no keyword is in request.args
@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    if keyword:
        return f"Search keyword: {keyword}"
    else:
        return "No keyword found"
    

# 2. Add /filter route to accept multiple query args: type, color, size
@app.route('/filter')
def filter_items():
    item_type = request.args.get('type')
    color = request.args.get('color')
    size = request.args.get('size')
    return f"Filter - Type: {item_type}, Color: {color}, Size: {size}"


# 4. Loop through all query parameters and return them in an HTML list
@app.route('/list-params')
def list_params():
    items = ""
    for key, value in request.args.items():
        items += f"<li>{key}: {value}</li>"
    return f"<h3>Query Parameters:</h3><ul>{items}</ul>"

# 5. Handle /greet with query param ?name=John instead of URL param
@app.route('/greet')
def greet_query():
    name = request.args.get('name', 'Guest')
    return f"Hello, {name}!"

# 6. Add optional query parameter to /profile like /profile?mode=admin
@app.route('/profile')
def profile_mode():
    mode = request.args.get('mode', 'user')
    return f"Profile Mode: {mode}"

# 7. Display the length of request.args to show number of query parameters
@app.route('/args-length')
def args_length():
    return f"Number of query parameters: {len(request.args)}"

# 8. Format the query parameters into a readable HTML table
@app.route('/table-format')
def table_format():
    html = "<h3>Query Parameters:</h3><table border='1'>"
    for key, value in request.args.items():
        html += f"<tr><td>{key}</td><td>{value}</td></tr>"
    html += "</table>"
    return html

# 9. Return a message if a specific query param (e.g., debug=true) is passed
@app.route('/debug-mode')
def debug_mode():
    if request.args.get('debug') == 'true':
        return "Debug mode is ON"
    return "Debug mode is OFF"

# 10. Create a combined route /display that accepts both URL and query parameters
@app.route('/display/<item>')
def display_combined(item):
    info = request.args.get('info', 'none')
    return f"Item: {item}<br>Info: {info}"



# Handling Form Data with request.form – 10 Tasks
# 1. Create a form at /contact to accept name and message
# 2. Use request.form['name'] to retrieve submitted value
# 4. Add basic form validation (check if name or message is empty)
# 8. Print form data to the terminal when the form is submitted
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 2. Access form data
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()

        # 4. Validation
        if not name or not message:
            return "Error: Name and message cannot be empty.", 400

        # 8. Print to terminal
        print(f"[Contact] Name: {name}, Message: {message}")

        # 3. Redirect to thank you page
        return redirect(url_for('thankyou', name=name))

    return '''
    <h2>Contact Form</h2>
    <form method="POST" action="/contact">
        Name: <input type="text" name="name"><br><br>
        Message:<br><textarea name="message"></textarea><br><br>
        <input type="submit" value="Send">
    </form>
    '''


# 3. Show a thank you page at /thankyou after submitting contact form
@app.route('/thankyou')
def thankyou():
    name = request.args.get('name', 'User')
    return f"<h3>Thank you, {name}, for contacting us!</h3>"

# 5. Return submitted data in a styled HTML response
# 6. Use request.form.get('field') safely to avoid KeyError
@app.route('/styled-response', methods=['POST'])
def styled_response():
    name = request.form.get('name', 'Anonymous')
    message = request.form.get('message', '')
    return f"""
    <div style="border:1px solid #ccc; padding:10px;">
        <h3>Submitted Information</h3>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Message:</strong> {message}</p>
    </div>
    """

# 7. Build a feedback form with rating selection and submit it
@app.route('/feedbacks', methods=['GET', 'POST'])
def feedbacks():
    if request.method == 'POST':
        name = request.form.get('name', 'Anonymous')
        rating = request.form.get('rating', 'Not given')
        print(f"[Feedback] {name} rated: {rating}")
        return f"<h3>Thanks {name} for rating us {rating} stars!</h3>"

    return '''
    <h2>Feedback Form</h2>
    <form method="POST">
        Name: <input type="text" name="name"><br>
        Rating:
        <select name="rating">
            <option value="1">1 Star</option>
            <option value="2">2 Stars</option>
            <option value="3">3 Stars</option>
            <option value="4">4 Stars</option>
            <option value="5">5 Stars</option>
        </select><br><br>
        <input type="submit" value="Submit Feedback">
    </form>
    '''

# 9. Build a /register form with fields: name, email, password
# 10. Show form data as a JSON-like dictionary in the HTML response
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'password': request.form.get('password', '')
        }
        print(f"[Register] {data}")
        return f"""
        <h2>Registration Details</h2>
        <pre>{data}</pre>
        """
    return '''
    <h2>Register</h2>
    <form method="POST">
        Name: <input type="text" name="name"><br>
        Email: <input type="email" name="email"><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Register">
    </form>
    '''


# Redirects and URL Building with url_for() – 5 Tasks
# 1. Create a /home route and use redirect(url_for('home')) from /start
@app.route('/start')
def start():
    return redirect(url_for('home'))

@app.route('/home1')
def home1():
    return "<h2>Welcome to the Home Page</h2>"

# 2. Add a /dashboard that redirects to /login if not logged in (simulate)
@app.route('/dashboard')
def dashboard():
    logged_in = request.args.get('login') == 'true'
    if not logged_in:
        return redirect(url_for('login'))
    return "<h2>Welcome to your Dashboard!</h2>"

@app.route('/loginn')
def loginn():
    return '''
    <h2>Login Page</h2>
    <p>You're not logged in. <a href="/dashboard?login=true">Click here to simulate login</a></p>
    '''

# 3. Use url_for('profile', username='mahesh') to build link dynamically in HTML
@app.route('/link-builder')
def link_builder():
    profile_url = url_for('profile', username='mahesh')
    return f'<a href="{profile_url}">Go to Mahesh\'s Profile</a>'

@app.route('/profiles/<username>')
def profiles(username):
    return f"<h2>Welcome, {username.capitalize()}</h2>"

# 4. Create a page with HTML links generated using url_for() inside response string
@app.route('/nav')
def navigation():
    return f"""
    <h3>Navigation Menu</h3>
    <ul>
        <li><a href="{url_for('home')}">Home</a></li>
        <li><a href="{url_for('dashboard')}">Dashboard</a></li>
        <li><a href="{url_for('link_builder')}">Mahesh's Profile Link</a></li>
    </ul>
    """


# 5. Redirect users to /thankyou after submitting any form
@app.route('/feedback-form', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        return redirect(url_for('thankyou'))
    return '''
    <form method="POST">
        Feedback: <input type="text" name="feedback"><br>
        <input type="submit" value="Submit">
    </form>
    '''

@app.route('/thankyouu')
def thankyouu():
    return "<h2>Thank you for your submission!</h2>"


if __name__=='__main__':
    app.run(debug=True)
