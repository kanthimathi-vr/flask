from flask import Flask, render_template

app = Flask(__name__)

@app.route("/team")
def team():
    team_members = [
        {"name": "Alice Johnson", "role": "Team Lead", "photo": "images/alice.jpg"},
        {"name": "Bob Smith", "role": "Developer", "photo": "images/bob.jpg"},
        {"name": "Charlie Lee", "role": "Designer", "photo": "images/charlie.jpg"},
    ]
    return render_template("team.html", title="Our Team", team=team_members)

if __name__ == "__main__":
    app.run(debug=True)
