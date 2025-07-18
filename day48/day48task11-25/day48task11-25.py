# 2. Using Jinja2: {{ variables }}, {% for %}, {% if %}  
# 1. Pass a variable username = "Mahesh" to home.html and display it. 
# 2. Pass a list of strings (["Python", "Flask", "Jinja"]) to a template and loop 
# through with {% for %}. 
# 3. Add an {% if %} block to display different greetings based on a logged_in 
# boolean. 
# 4. Create a route /scores and pass a list of numbers, display them in a list in 
# HTML. 
# 5. Inside {% for %}, use loop.index to show the serial number of each item. 
# 6. Use nested {% if %} inside {% for %} to mark certain values (e.g., highlight 
# scores > 80). 
# 7. Use {% else %} to display a message when a passed list is empty. 
# 8. Display the current date passed as a variable (datetime.now()). 
# 9. Use a dictionary in Jinja2 and loop through its keys and values. 
# 10. Show a dynamic message like “Welcome back, {{ name }}” if name is 
# passed. 
# 11. Add conditional HTML rendering (e.g., “Admin Panel” only for role = 
# "admin"). 
# 12. Render a Bootstrap-styled card for each product in a product list. 
# 13. Capitalize a name using {{ name.capitalize() }}. 
# 14. Limit characters in a description using {{ description[:50] }}. 
# 15. Use safe filter to render a variable with embedded HTML tags. 

from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    username = "Admin"
    logged_in = True
    skills = ["Python", "Flask", "Jinja"]
    current_date = datetime.now()
    user_role = "admin"
    description = "This is a detailed description that will be cut off after 50 characters."
    html_message = "<b>This is bold HTML inside a variable</b>"

    return render_template(
        "home.html",
        username=username,
        logged_in=logged_in,
        skills=skills,
        current_date=current_date,
        role=user_role,
        name="Mahesh",
        description=description,
        html_message=html_message,
        profile={"email": "mahesh@example.com", "age": 30}
    )

@app.route("/scores")
def scores():
    scores = [45, 78, 82, 91, 67]
    return render_template("scores.html", scores=scores)

@app.route("/products")
def products():
    product_list = [
        {"name": "Laptop", "price": "$999"},
        {"name": "Phone", "price": "$499"},
        {"name": "Tablet", "price": "$299"}
    ]
    return render_template("products.html", products=product_list)










if __name__ == '__main__':
    app.run(debug= True)
