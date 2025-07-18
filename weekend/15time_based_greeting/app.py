from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/greet")
def greet():
    hour = request.args.get("hour", type=int)
    greeting = None

    if hour is not None:
        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Night"
    return render_template("greet.html", hour=hour, greeting=greeting)

if __name__ == "__main__":
    app.run(debug=True)
