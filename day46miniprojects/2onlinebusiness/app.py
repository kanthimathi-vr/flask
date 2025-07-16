from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Business hours: 9:00 to 17:00 (9 AM to 5 PM)
@app.route('/')
def check_business_hours():
    now = datetime.now()
    current_hour = now.hour

    if 9 <= current_hour < 17:
        message = "<h2 style='color:green;'>We are open!</h2>"
    else:
        message = "<h2 style='color:red;'>Closed</h2>"

    return f"""
    <html>
        <body>
            <h1>Welcome to Our Online Store</h1>
            {message}
            <p>Current server time: {now.strftime('%H:%M:%S')}</p>
            <hr>
        </body>
    </html>
    """

# Contact page with HTML formatting
@app.route('/contact')
def contact():
    return """
    <html>
        <body>
            <h2>Contact Us</h2>
            <p><b>Email:</b> support@onlinebusiness.com</p>
            <p><b>Phone:</b> +1-800-555-1234</p>
            <hr>
            <p>We typically respond within 24 hours.</p>
        </body>
    </html>
    """

# Run app in debug mode
if __name__ == '__main__':
    print("🚀 Starting server in debug mode...")
    app.run(debug=True)
