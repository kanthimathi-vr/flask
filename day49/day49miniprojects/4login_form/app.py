from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy credentials for authentication
DUMMY_EMAIL = 'admin@example.com'
DUMMY_PASSWORD = 'secret123'

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == DUMMY_EMAIL and form.password.data == DUMMY_PASSWORD:
            flash('Login successful!', 'success')
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)


# DUMMY_EMAIL = 'admin@example.com'
# DUMMY_PASSWORD = 'secret123'
