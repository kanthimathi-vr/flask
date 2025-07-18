from flask import Flask, render_template

app = Flask(__name__)

@app.route("/faq")
def faq():
    faqs = [
        {"question": "What is Flask?", "answer": "Flask is a lightweight Python web framework."},
        {"question": "Is Flask suitable for beginners?", "answer": "Yes, it's simple and flexible."},
        {"question": "When was Flask released?", "answer": "April 2010."},
        {"question": "How to deploy a Flask app?", "answer": ""},
    ]
    return render_template("faq.html", title="FAQs", faqs=faqs)

if __name__ == "__main__":
    app.run(debug=True)
