from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

@app.route("/courses")
def courses():
    course_list = ["Python", "Flask", "HTML", "CSS"]
    return render_template("courses.html", courses=course_list)

@app.route("/login")
def login():
    is_logged_in = True  # Change to False to test both states
    return render_template("login.html", is_logged_in=is_logged_in)

@app.route("/profile")
def profile():
    user_profile = {
        "name": "mathi",
        "email": "mathi@example.com",
        "age": 28,
        "city": "Chennai"
    }
    return render_template("profile.html", profile=user_profile)

@app.route("/datetime")
def show_datetime():
    now = datetime.now()
    return render_template("datetime.html", current_time=now)

@app.route("/news")
def news():
    news_items = [
        "Flask 3.0 released!",
        "Python 3.12 improves performance",
        "Jinja2 supports new filters"
    ]
    return render_template("news.html", news_items=news_items)

@app.route("/profile_card")
def profile_card():
    return render_template("profile_card.html", name="Mahesh", age=28, city="Chennai")

@app.route("/products")
def products():
    product_list = [
        {"name": "Laptop", "price": 1000},
        {"name": "Phone", "price": 500},
        {"name": "Headphones", "price": 150}
    ]
    return render_template("products.html", title="Products", products=product_list)

@app.route("/tax")
def tax():
    price = 1000
    tax_rate = 0.18
    tax = price * tax_rate
    total = price + tax
    return render_template("tax.html", price=price, tax=tax, total=total)

if __name__ == "__main__":
    app.run(debug=True)
