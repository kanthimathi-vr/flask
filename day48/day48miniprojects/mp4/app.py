from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/weather")
def weather():
    weather_data = {
        "city": "New York",
        "temperature": 32,  # Celsius
        "condition": "sunny",  # "sunny" or "rainy"
        "humidity": 60,
        "date": datetime.now().strftime("%B %d, %Y")
    }
    return render_template("weather.html", title="Daily Weather Report", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
