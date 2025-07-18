from flask import Flask, render_template

app = Flask(__name__)

@app.route("/blogs")
def blogs():
    blog_list = [
        {
            "title": "How to Master Flask",
            "author": "Alice",
            "snippet": "Flask is a lightweight WSGI web application framework...",
            "featured": True
        },
        {
            "title": "Understanding Jinja2",
            "author": "Bob",
            "snippet": "Templates are at the core of dynamic web pages...",
            "featured": False
        },
        {
            "title": "Python Tips and Tricks",
            "author": "Charlie",
            "snippet": "Boost your Python productivity with these tips...",
            "featured": True
        }
    ]
    return render_template("blogs.html", title="Blog Reader", blogs=blog_list)

if __name__ == "__main__":
    app.run(debug=True)
