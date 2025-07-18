from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample user database
users = {
    "mahesh": {
        "name": "Mahesh Kumar",
        "bio": "Full-stack developer and trainer.",
        "joined": datetime(2025, 7, 15),
        "image": "mahesh.jpg"
    },
    "alice": {
        "name": "Alice Johnson",
        "bio": "Python enthusiast and blogger.",
        "joined": datetime(2025, 7, 1),
        "image": "alice.jpg"
    },
    "bob": {
        "name": "Bob Smith",
        "bio": "Student learning Flask.",
        "joined": datetime(2025, 6, 10),
        "image": "bob.jpg"
    }
}

@app.route("/profile/<username>")
def profile(username):
    user = users.get(username)
    if not user:
        return render_template("404.html", title="User Not Found"), 404

    days_since_joined = (datetime.now() - user["joined"]).days
    new_user = days_since_joined < 7

    return render_template(
        "profile.html",
        title=f"{user['name']}'s Profile",
        name=user["name"],
        bio=user["bio"],
        joined=user["joined"].strftime("%B %d, %Y"),
        image_file=user["image"],
        new_user=new_user
    )

if __name__ == "__main__":
    app.run(debug=True)
