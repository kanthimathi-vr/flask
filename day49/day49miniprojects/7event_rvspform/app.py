from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class RSVPForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    will_attend = BooleanField('I will attend')
    submit = SubmitField('Submit RSVP')

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    form = RSVPForm()
    if form.validate_on_submit():
        if not form.will_attend.data:
            flash("Sorry to miss you.", "warning")
        else:
            flash("Thank you for your RSVP! See you at the event.", "success")
        return redirect(url_for('rsvp'))
    return render_template('rsvp.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
