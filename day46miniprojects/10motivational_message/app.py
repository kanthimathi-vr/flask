from flask import Flask
import random

app = Flask(__name__)

# List of motivational messages
messages = [
    "Believe in yourself and all that you are.",
    "Every day is a second chance.",
    "Push yourself, because no one else is going to do it for you.",
    "Success doesn't just find you. You have to go out and get it.",
    "Don't watch the clock; do what it does. Keep going.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Dream bigger. Do bigger."
]

# Inline CSS for styling
STYLE = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f8ff;
        color: #333;
        padding: 50px;
        text-align: center;
    }
    .message {
        font-size: 24px;
        color: #0077cc;
        border-left: 5px solid #0077cc;
        border-bottom: 5px solid #0077cc;
        border-top: 2px solid #0077cc;
        border-right: 2px solid #0077cc;
        padding: 20px;
        background-color: #e6f2ff;
        margin: auto;
        width: 60%;
        border-radius: 10px;
    }
</style>
"""
@app.route('/')
def home():
    return """
        <h1 style="background-color : pink; color : blue;">
        Motivational Message</h1>"""
# Route 1: Random/rotating message
@app.route('/message')
def random_message():
    msg = random.choice(messages)
    return f"""
    {STYLE}
    <div class="message">
        <p>{msg}</p>
    </div>
    """

# Route 2: Message by index
@app.route('/message/<int:index>')
def message_by_index(index):
    if 0 <= index < len(messages):
        msg = messages[index]
        return f"""
        {STYLE}
        <div class="message">
            <p>{msg}</p>
        </div>
        """
    else:
        return f"""
        {STYLE}
        <div class="message">
            <p>❌ Invalid index. Please use /message/0 to /message/{len(messages) - 1}</p>
        </div>
        """

# Run Flask app with debug mode
if __name__ == '__main__':
    print("🌟 Motivational Message Rotator is running...")
    app.run(debug=True)
