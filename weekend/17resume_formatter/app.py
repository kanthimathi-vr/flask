from flask import Flask, render_template, request
from flask import Markup
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        experience = request.form.get("experience")
        return render_template("resume.html", name=name, email=email, experience=experience)
    return render_template("form.html")


@app.template_filter('nl2br')
def nl2br_filter(s):
    if s:
        return Markup(s.replace('\n', '<br>'))
    return ''

if __name__ == "__main__":
    app.run(debug=True)
