from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class EnrollmentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    course = SelectField('Course', choices=[
        ('python', 'Python Programming'),
        ('data', 'Data Science'),
        ('web', 'Web Development'),
        ('ml', 'Machine Learning')
    ], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=60)])
    submit = SubmitField('Enroll Now')

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    form = EnrollmentForm()
    if form.validate_on_submit():
        name = form.name.data
        course_label = dict(form.course.choices)[form.course.data]
        flash(f"🎓 Hi {name}, you enrolled in {course_label}!", "success")
        return redirect(url_for('enroll'))
    return render_template('enroll.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
