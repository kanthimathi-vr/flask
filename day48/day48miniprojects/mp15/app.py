from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/achievements")
def achievements():
    data = {
        "2025": [
            {"title": "Launched AI Module", "icon": "trophy.png"},
            {"title": "Won Hackathon", "icon": "star.png"}
        ],
        "2024": [
            {"title": "Expanded to 3 cities", "icon": "trophy.png"}
        ],
        "2023": [
            {"title": "Reached 10,000 users", "icon": "star.png"}
        ]
    }

    current_year = str(datetime.now().year)
    return render_template("achievements.html", title="Achievements", data=data, current_year=current_year)

if __name__ == "__main__":
    app.run(debug=True)
