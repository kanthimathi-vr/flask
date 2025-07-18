#  3. Creating a base template with template inheritance  
# 1. Create a base.html with basic structure (html, head, body, and block tags). 
# 2. Add a {% block title %} and {% block content %} inside base.html. 
# 3. Modify index.html, about.html, and contact.html to {% extends "base.html" 
# %}. 
# 4. Add a common navigation bar in base.html. 
# 5. Add a footer section in base.html and include it across all pages. 
# 6. Create a custom 404 page that also extends base.html. 
# 7. Add a <head> block in base.html for setting dynamic page titles. 
# 8. Add custom <style> tags in the base.html for uniform styling. 
# 9. Use Bootstrap CDN in base.html to style all templates. 
# 10. Use nested block tags to customize child pages.


from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)





