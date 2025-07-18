from flask import Flask, render_template

app = Flask(__name__)

@app.route("/testimonials")
def testimonials():
    feedbacks = [
        {
            "name": "Alice",
            "comment": "Great service and support!",
            "photo": "profiles/user1.jpg",
            "rating": 5
        },
        {
            "name": "Bob",
            "comment": "Good experience overall.",
            "photo": "profiles/user2.jpg",
            "rating": 4
        },
        {
            "name": "Charlie",
            "comment": "Decent, but room for improvement.",
            "photo": "profiles/user3.jpg",
            "rating": 3
        }
    ]
    return render_template("testimonials.html", title="Testimonials", feedbacks=feedbacks)

if __name__ == "__main__":
    app.run(debug=True)
