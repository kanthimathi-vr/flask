# # day48 tasks
# # day 3 flask
#  1. Setting up HTML templates in the templates/ folder  
# 1. Create a templates/ folder and add a basic index.html file. 
# 2. Render the index.html from a Flask route using render_template(). 
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    username="admin"
    return render_template("index.html",title="home",username=username)

# 3. Add another file about.html and render it from /about route. 

@app.route('/about')
def about():
    return render_template("about.html",title="about")

# 4. Modify index.html to show a simple heading and a paragraph. 

# 5. Create contact.html and add form tags (no functionality yet). 

@app.route('/contact')
def contact():
    return render_template("contact.html",title = "contact")
# 6. Move all .html files into the templates/ folder and confirm Flask loads them 
# correctly. 
# 7. Create a 404 error page (404.html) and use @app.errorhandler(404) to 
# render it. 
# 8. Add a navigation bar in index.html linking to /about, /contact, and /. 

# 9. Pass a variable from Flask to index.html (e.g., username) and display it. 
# 10. Include a page title in each template using <title>{{ title }}</title>. 


if __name__ == '__main__':
    app.run(debug= True)







