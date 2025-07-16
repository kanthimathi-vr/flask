from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Personalised greeting</h1>"

# Route 1: Simple Hello
@app.route('/hello/<name>')
def hello(name):
    return f"<h2>Hello, {name}!</h2>"

# Route 2: Time-based Greeting
@app.route('/greet/<name>/<time>')
def greet(name, time):
    time = time.lower()
    if time == 'morning':
        return f"<h2>Good Morning, {name}!</h2>"
    elif time == 'evening':
        return f"<h2>Good Evening, {name}!</h2>"
    elif time == 'afternoon':
        return f"<h2>Good Afternoon, {name}!</h2>"
    else:
        return f"<h2>Hello {name}, I don't know what time it is!</h2>"

# Run in debug mode
if __name__ == '__main__':
    print("🚀 Running in debug mode...")
    app.run(debug=True)
