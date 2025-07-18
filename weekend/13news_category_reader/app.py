from flask import Flask, render_template, abort

app = Flask(__name__)

# Hardcoded news data
news_data = {
    "sports": [
        "Team A wins the national championship!",
        "Local player scores hat-trick in derby."
    ],
    "technology": [
        "New AI model surpasses expectations.",
        "Tech giant releases foldable tablet."
    ],
    "entertainment": [
        "Blockbuster movie breaks box office records.",
        "Famous singer announces world tour."
    ]
}

@app.route("/news/<category>")
def news_category(category):
    category_news = news_data.get(category.lower())
    if not category_news:
        abort(404)
    return render_template("news.html", category=category.capitalize(), articles=category_news)

if __name__ == "__main__":
    app.run(debug=True)
