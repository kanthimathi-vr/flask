from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/event")
def event():
    event_name = "Tech Conference 2025"
    event_date = datetime(2025, 12, 25, 10, 0, 0)  # yyyy, mm, dd, hh, mm, ss
    now = datetime.now()
    event_started = now >= event_date

    return render_template(
        "event.html",
        title="Event Countdown",
        event_name=event_name,
        event_date=event_date.strftime("%Y-%m-%dT%H:%M:%S"),  # ISO format for JS
        event_started=event_started
    )

if __name__ == "__main__":
    app.run(debug=True)
