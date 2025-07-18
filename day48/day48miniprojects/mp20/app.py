from flask import Flask, render_template

app = Flask(__name__)

@app.route("/leaderboard")
def leaderboard():
    leaderboard_data = [
        {"name": "Alice", "score": 98},
        {"name": "Bob", "score": 87},
        {"name": "Charlie", "score": 75}
    ]
    return render_template("leaderboard.html", title="Leaderboard", leaderboard=leaderboard_data)

if __name__ == "__main__":
    app.run(debug=True)
