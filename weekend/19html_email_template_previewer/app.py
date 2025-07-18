from flask import Flask, render_template, request, Markup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title_template = request.form.get("title", "")
        body_template = request.form.get("body", "")

        # Sample context for placeholders
        context = {
            "username": "John Doe",
            "date": "July 18, 2025",
            "company": "OpenAI",
        }

        # Render the email content safely using Jinja2 Template
        from jinja2 import Template, exceptions

        try:
            title_rendered = Template(title_template).render(context)
            body_rendered = Template(body_template).render(context)
        except exceptions.TemplateError as e:
            # Handle template errors gracefully
            title_rendered = f"Error rendering title: {e}"
            body_rendered = f"Error rendering body: {e}"

        # Mark safe for HTML rendering in preview
        return render_template("preview.html",
                               title=Markup(title_rendered),
                               body=Markup(body_rendered))
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
