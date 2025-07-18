from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", title="Home")

# Trigger error manually (optional test route)
@app.route("/cause-error")
def cause_error():
    raise Exception("This is a test for 500 error")

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html", title="Page Not Found", error=str(error)), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html", title="Server Error", error=str(error)), 500

if __name__ == "__main__":
    app.run(debug=True)
