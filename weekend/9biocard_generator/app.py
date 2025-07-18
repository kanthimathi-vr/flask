from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        hobbies = request.form["hobbies"].split(",")
        hobbies = [h.strip() for h in hobbies if h.strip()]
        return render_template("card.html", name=name, age=age, hobbies=hobbies)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
