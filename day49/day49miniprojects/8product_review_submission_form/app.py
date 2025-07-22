from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class ReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rating = IntegerField('Rating (1–5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Review Message', validators=[DataRequired()])
    submit = SubmitField('Submit Review')

@app.route('/review', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        flash("✅ Thank you for your review!", "success")
        return redirect(url_for('review'))
    return render_template('review.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
