from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    course = StringField('Course', validators=[DataRequired()])
    rating = IntegerField('Rating (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    suggestion = TextAreaField('Suggestion (Optional)')
    submit = SubmitField('Submit Feedback')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        score = form.rating.data
        if score < 5:
            msg = "We'll improve!"
        elif 5 <= score <= 7:
            msg = "Thanks for your feedback!"
        else:
            msg = "Glad you liked the course!"
        flash(msg, "success")
        return redirect(url_for('feedback'))
    return render_template('feedback.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
