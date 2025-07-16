from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <h1 style= "background-color:purple; color:white; text-align: center;padding:3%;" >Health remainder display</h1>
        """


# Health advice messages rotating every few hours
health_tips = [
    "💧 Drink water to stay hydrated!",
    "🧘 Take a moment to stretch your body.",
    "🍎 Have a healthy snack.",
    "🚶‍♂️ Take a short walk.",
    "😴 Remember to rest your eyes.",
    "🧴 Apply sunscreen if you're going outside.",
]

@app.route('/reminder/<int:hour>')
def reminder(hour):
    if hour < 0 or hour > 23:
        return """
        <html>
            <body style="font-family: Arial; background-color: #f8d7da; text-align: center; padding: 40px;">
                <h2 style="color: #721c24;">❌ Invalid hour! Please enter an hour between 0 and 23.</h2>
                <p>See <a href="/reminder/help">/reminder/help</a> for usage.</p>
            </body>
        </html>
        """
    
    # Rotate health tips based on hour
    tip = health_tips[hour % len(health_tips)]
    
    return f"""
    <html>
        <head>
            <title>Health Reminder for Hour {hour}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #d1ecf1;
                    color: #0c5460;
                    text-align: center;
                    padding: 50px;
                }}
                .tip-box {{
                    background-color: #bee5eb;
                    border-radius: 10px;
                    padding: 30px;
                    display: inline-block;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                h2 {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="tip-box">
                <h2>🕒 Health Reminder at Hour {hour}</h2>
                <p style="font-size: 22px;">{tip}</p>
                <hr>
                <p><a href="/reminder/help">How to use this reminder</a></p>
            </div>
        </body>
    </html>
    """

@app.route('/reminder/help')
def reminder_help():
    return """
    <html>
        <head>
            <title>Health Reminder Help</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    text-align: center;
                    padding: 50px;
                }
                .help-box {
                    background-color: white;
                    border-radius: 10px;
                    padding: 30px;
                    display: inline-block;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    max-width: 600px;
                }
                h2 {
                    color: #17a2b8;
                    margin-bottom: 20px;
                }
                code {
                    background-color: #e9ecef;
                    padding: 3px 6px;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <div class="help-box">
                <h2>ℹ️ How to Use Health Reminder</h2>
                <p>Send a GET request to <code>/reminder/&lt;hour&gt;</code>, where <code>hour</code> is an integer from 0 to 23.</p>
                <p>Example URLs:</p>
                <ul style="list-style:none; font-size: 18px; padding-left: 0;">
                    <li><a href="/reminder/9">/reminder/9</a> - Reminder for 9 AM</li>
                    <li><a href="/reminder/15">/reminder/15</a> - Reminder for 3 PM</li>
                    <li><a href="/reminder/22">/reminder/22</a> - Reminder for 10 PM</li>
                </ul>
                <p>The reminder rotates through different health tips based on the hour provided.</p>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("🩺 Health Reminder app running on http://127.0.0.1:5000")
    app.run(debug=True)
