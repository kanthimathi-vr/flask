from flask import Flask, render_template

app = Flask(__name__)

# Common data
portfolio_data = {
    "name": "Jane Doe",
    "skills": ["Python", "Flask", "JavaScript", "CSS", "HTML"],
    "available_for_hire": True,
    "projects": [
        {"title": "Portfolio Website", "description": "My personal portfolio built with Flask."},
        {"title": "Blog App", "description": "A simple blog platform using Flask and SQLite."},
        {"title": "Task Manager", "description": "A task tracking app with user authentication."}
    ]
}

@app.route("/")
def home():
    return render_template("home.html", title="Home", **portfolio_data)

@app.route("/about")
def about():
    return render_template("about.html", title="About", **portfolio_data)

@app.route("/projects")
def projects():
    return render_template("projects.html", title="Projects", **portfolio_data)

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact", **portfolio_data)

if __name__ == "__main__":
    app.run(debug=True)
