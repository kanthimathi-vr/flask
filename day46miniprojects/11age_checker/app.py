from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <h1 style="color: purple;">Age checker</h1>
        """
@app.route('/age/<name>/<int:year>')
def age_checker(name, year):
    current_year = datetime.now().year
    if year >= current_year:
        return f"""
        <html>
            <body>
                <h3>❌ Invalid year! Please enter a birth year less than {current_year}.</h3>
            </body>
        </html>
        """

    age = current_year - year
    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial;
                    background-color: #f4f8ff;
                    color: #333;
                    text-align: center;
                    margin-top: 50px;
                }}
                .box {{
                    background: #e0f7fa;
                    border: 2px solid #00acc1;
                    padding: 20px;
                    border-radius: 10px;
                    display: inline-block;
                }}
            </style>
        </head>
        <body>
            <div class="box">
                <h2>Hi {name.title()},</h2>
                <p>You are <strong>{age}</strong> years old.</p>
            </div>
        </body>
    </html>
    """
# Run the app
if __name__ == '__main__':
    print("🌐 Age Checker App running at http://127.0.0.1:5000")
    app.run(debug=True)