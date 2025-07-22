from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date = DateField('Appointment Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Appointment Time', validators=[DataRequired()], format='%H:%M')
    purpose = TextAreaField('Purpose', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        flash(f"📅 Appointment booked for {form.date.data.strftime('%Y-%m-%d')} at {form.time.data.strftime('%H:%M')}", "success")
        return redirect(url_for('appointment'))
    return render_template('appointment.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
