#  day46 tasks
# 28. Add comments to each section of the app.py explaining what it does
#  task no  21. Create a new file named app.py
# created file app.py
#   22. Import Flask correctly in your script
from flask import Flask

# 23. Create a basic Flask application instance
app = Flask(__name__)  
# This line initializes the Flask app.

#  24. Add a basic home route / that returns "Hello, Flask!"
 
@app.route('/')
def home():
    return "Hello,Flask!"

#  26. Add another route /about returning "This is the about page"
@app.route('/about')
def about():
    # 35. Add a print() statement and observe console output on page refresh
    print("About page added with new print statement")
    return "This is my about page"
# 30. Try adding a wrong syntax and observe Flask's debug error page

@app.route('/error')
def error():
    return "error message"
# 41. Define a route /hello that returns a welcome message
# 43. Add multiple routes pointing to the same function
@app.route('/hello')
@app.route('/welcome')
def hello():
    return "<h1 >welcome to hello ,welcome page!</h1>"

#  47. Add inline CSS styling to the returned HTML
@app.route('/styled')
def styled():
    return """
        <html>
        <body>
        <h1 style = " color: red;">Styled heading</h1>
        </body>
        </html>

"""

#  49. Return an unordered list with 3 items from an HTML response
@app.route('/list')
def list_items():
    return """
    <html>
        <body>
            <h3>My Favorite Fruits:</h3>
            <ul>
                <li>Apple</li>
                <li>Banana</li>
                <li>Mango</li>
            </ul>
        </body>
    </html>
    """

#  50. Use basic HTML tags like <h1>, <p>, <br>, <hr> and explain their output

@app.route('/html-tags')
def html_tags():
    return """
    <html>
        <body>
            <h1>Main Heading</h1>        <!-- Large bold header -->
            <p>This is a paragraph.</p>  <!-- Normal text block -->
            Line 1<br>Line 2<br>         <!-- Line breaks -->
            <hr>                         <!-- Horizontal line -->
            <p>After the horizontal line</p>
        </body>
    </html>
    """

# 42. Add a route /user/<username> and return a dynamic message with the username
@app.route('/user/<username>')
def show_user(username):
    return f"Hello, {username}"

# 44. Add different HTTP methods (GET, POST) in a route and print the method used
# @app.route('/method',methods=['GET','POST'])
# def method_check():
#     # return f"HTTP method used : {request.method}"


#  25. Run the app using python app.py and open it in the browser
if __name__ == '__main__':
    print("starting server.....")
    app.run(debug=True)

#27. Print something in the console when the server starts


