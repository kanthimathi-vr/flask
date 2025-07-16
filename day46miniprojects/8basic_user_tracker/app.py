from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """<h1 style="color:green">
    Basic user Tracker</h1>
    """


# Route 1: Greet user by name
@app.route('/user/<name>')
def greet_user(name):
    print(f"[LOG] Accessed /user route with name: {name}")
    return f"<h2>Welcome, {name}!</h2>"

# Route 2: Greet user and mention city
@app.route('/user/<name>/location/<city>')
def user_location(name, city):
    print(f"[LOG] Accessed /user/{name}/location/{city}")
    return f"<h2>Hi {name}, how is {city}?</h2>"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
