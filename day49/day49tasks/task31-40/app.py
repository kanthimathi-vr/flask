from flask import Flask, render_template, request, flash, redirect, url_for
from forms import UserForm

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data

        flash("Form submitted successfully!", 'success')
        flash(f"Hello {name}, thank you for registering!", 'info')

        if age > 60:
            flash("You're above 60. Some features may vary.", 'warning')

        return redirect(url_for('result'))

    if request.method == 'POST':
        if 'email' in form.errors:
            flash("Invalid email address entered.", 'error')
        if 'terms' in form.errors:
            flash("You must accept the terms and conditions.", 'warning')

    return render_template('form.html', form=form)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            flash("Login successful!", 'success')
        else:
            flash("Invalid credentials!", 'error')

        return redirect(url_for("login"))

    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
