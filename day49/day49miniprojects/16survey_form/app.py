from flask import Flask, render_template, redirect, flash, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class SurveyForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=100, message="Age must be between 18 and 100")])
    gender = SelectField('Gender', choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    favorite_product = SelectField('Favorite Product', choices=[('', 'Select Product'), ('product1', 'Product 1'), ('product2', 'Product 2'), ('product3', 'Product 3')], validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit Survey')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        flash("🎉 Thanks for participating!", "success")
        return redirect(url_for('survey'))
    elif request.method == 'POST':
        # Collect all errors to display in a top error box
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                label = getattr(form, field).label.text
                error_messages.append(f"{label}: {error}")
        flash(error_messages, 'error-box')
    return render_template('survey.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
