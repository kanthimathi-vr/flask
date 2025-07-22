from flask import Flask, render_template, redirect, flash, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class DonationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=10, message="Amount must be at least 10")])
    cause = SelectField('Cause', choices=[
        ('', 'Select Cause'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('environment', 'Environment'),
        ('animal_welfare', 'Animal Welfare'),
    ], validators=[DataRequired()])
    submit = SubmitField('Donate')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    form = DonationForm()
    if form.validate_on_submit():
        flash(f"💖 Thank you {form.name.data} for donating ${form.amount.data} towards {dict(form.cause.choices).get(form.cause.data)}!", "success")
        return redirect(url_for('donate'))
    elif request.method == 'POST':
        errors = []
        for field, error_list in form.errors.items():
            label = getattr(form, field).label.text
            for error in error_list:
                errors.append(f"{label}: {error}")
        flash(errors, "error-box")
    return render_template('donation.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
