from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class BookingForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    room_type = SelectField('Room Type', choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite')], validators=[DataRequired()])
    nights = IntegerField('Nights', validators=[DataRequired(), NumberRange(min=1, message="Nights must be at least 1")])
    submit = SubmitField('Book Now')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        flash(f"✅ Booking for {form.full_name.data} confirmed: {form.nights.data} night(s) in {form.room_type.data}", "success")
        return redirect(url_for('booking'))
    return render_template('booking.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
