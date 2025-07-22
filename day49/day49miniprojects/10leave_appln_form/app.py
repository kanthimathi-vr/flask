from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class LeaveForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    reason = TextAreaField('Reason for Leave', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Apply for Leave')

@app.route('/leave', methods=['GET', 'POST'])
def leave():
    form = LeaveForm()
    if form.validate_on_submit():
        start = form.start_date.data
        end = form.end_date.data
        if end < start:
            form.end_date.errors.append("End date cannot be before start date.")
        else:
            duration = (end - start).days + 1
            flash(f"✅ Leave applied for {duration} day(s).", "success")
            return redirect(url_for('leave'))
    return render_template('leave.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
