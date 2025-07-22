from flask import Flask, render_template, redirect, flash, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class GymSignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=16, message="You must be at least 16 years old")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    plan = SelectField('Plan', choices=[('', 'Select Plan'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[DataRequired()])
    accept_terms = BooleanField('I accept the terms and conditions', validators=[DataRequired(message="You must accept the terms")])
    submit = SubmitField('Sign Up')

@app.route('/gym_signup', methods=['GET', 'POST'])
def gym_signup():
    form = GymSignupForm()
    if form.validate_on_submit():
        flash(f"🏋️‍♂️ Welcome to our gym, {form.name.data}!", "success")
        return redirect(url_for('gym_signup'))
    elif request.method == 'POST':
        errors = []
        for field, error_list in form.errors.items():
            label = getattr(form, field).label.text
            for error in error_list:
                errors.append(f"{label}: {error}")
        flash(errors, "error-box")
    return render_template('gym_signup.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
