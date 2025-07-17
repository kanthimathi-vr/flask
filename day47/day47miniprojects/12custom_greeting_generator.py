# 12. Custom Greeting Generator
# Requirements:
# - /greet: GET query string like ?name=Arivu&time=morning
# - /custom-greet/<name>: Dynamic greeting
# - Show form to enter name and time, POST to /submit-greet
# - Redirect to /greet-result after submission
 

from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Greeting form HTML
greet_form_html = """
<h2>Custom Greeting Form</h2>
<form action="/submit-greet" method="post">
  Name: <input type="text" name="name" required><br><br>
  Time of Day:
  <select name="time" required>
    <option value="morning">Morning</option>
    <option value="afternoon">Afternoon</option>
    <option value="evening">Evening</option>
    <option value="night">Night</option>
  </select><br><br>
  <input type="submit" value="Generate Greeting">
</form>
"""

@app.route('/greet')
def greet():
    name = request.args.get('name')
    time = request.args.get('time')

    if name and time:
        return f"<h3>Good {time.capitalize()}, {name}!</h3><a href='/greet'>Try again</a>"
    else:
        return render_template_string(greet_form_html)

@app.route('/custom-greet/<name>')
def custom_greet(name):
    return f"<h3>Hello, {name}! Have a great day!</h3>"

@app.route('/submit-greet', methods=['POST'])
def submit_greet():
    name = request.form['name']
    time = request.form['time']
    # Redirect with query string
    return redirect(url_for('greet', name=name, time=time))

@app.route('/greet-result')
def greet_result():
    name = request.args.get('name')
    time = request.args.get('time')
    if name and time:
        return f"<h3>Your greeting has been generated: Good {time}, {name}!</h3>"
    else:
        return "<h3>Missing greeting data.</h3>"

if __name__ == '__main__':
    app.run(debug=True)
