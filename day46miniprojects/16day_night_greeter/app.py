from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
            <h1 style= "background-color:brown; color:white; text-align: center;padding:3%;">
            Day Night Greeter</h1>
            """
# Function to return greeting based on hour
def get_greeting(hour):
    if hour < 0 or hour > 23:
        return "❌ Invalid hour! Please enter a value between 0 and 23."
    elif 5 <= hour < 12:
        return "☀️ Good Morning!"
    elif 12 <= hour < 17:
        return "🌤️ Good Afternoon!"
    elif 17 <= hour < 21:
        return "🌇 Good Evening!"
    else:
        return "🌙 Good Night!"

# Route: /greet/<hour> manually entered
@app.route('/greet/<int:hour>')
def greet(hour):
    greeting = get_greeting(hour)
    return f"""
    <html>
        <head>
            <title>Day/Night Greeter</title>
            <style>
                body {{
                    font-family: Arial;
                    text-align: center;
                    padding: 50px;
                    background-color: #eef6f7;
                }}
                .box {{
                    background: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    display: inline-block;
                }}
            </style>
        </head>
        <body>
            <div class="box">
                <h2>{greeting}</h2>
                <p><i>(Based on hour: {hour})</i></p>
                <hr>
                <p><a href="/greet/info">See usage info</a> | <a href="/greet/now">Check current time</a></p>
            </div>
        </body>
    </html>
    """

# Route: /greet/now — auto-detect current hour
@app.route('/greet/now')
def greet_now():
    current_hour = datetime.now().hour
    greeting = get_greeting(current_hour)

    return f"""
    <html>
        <head>
            <title>Greet Now</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 60px;">
            <h2>{greeting}</h2>
            <p><strong>Current Hour:</strong> {current_hour}</p>
            <hr>
            <p><a href="/greet/info">How it works</a></p>
        </body>
    </html>
    """

# Route: /greet/info — instructions
@app.route('/greet/info')
def greet_info():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>🕒 Greet App Info</h2>
            <p>Use this app to get a greeting based on the hour.</p>
            <p><strong>Manual:</strong> /greet/&lt;hour&gt; (e.g. /greet/14)</p>
            <p><strong>Live:</strong> /greet/now (uses your system time)</p>
        </body>
    </html>
    """

# Run with debug mode
if __name__ == '__main__':
    print("🌞 Day/Night Greeter running at http://127.0.0.1:5000")
    app.run(debug=True)
