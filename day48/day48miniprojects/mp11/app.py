from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/news")
def news():
    news_list = [
        {
            "headline": "Local elections results announced",
            "datetime": datetime(2025, 7, 18, 9, 30),
            "category": "Politics",
            "is_breaking": False
        },
        {
            "headline": "Massive tech outage hits global networks",
            "datetime": datetime(2025, 7, 18, 11, 15),
            "category": "Technology",
            "is_breaking": True
        },
        {
            "headline": "New species discovered in Amazon rainforest",
            "datetime": datetime(2025, 7, 17, 16, 45),
            "category": "Science",
            "is_breaking": False
        }
    ]
    return render_template("news.html", title="Latest News", news_list=news_list)

if __name__ == "__main__":
    app.run(debug=True)
