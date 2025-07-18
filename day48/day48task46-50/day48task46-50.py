from flask import Flask, render_template

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html", title="Home")

# About route (displays static image)
@app.route("/about")
def about():
    return render_template("about.html", title="About Us")

# Contact route (can test JS and CSS here too)
@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")


if __name__ == "__main__":
    app.run(debug=True)
