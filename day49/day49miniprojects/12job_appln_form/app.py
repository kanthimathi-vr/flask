from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, URL, NumberRange

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class JobApplicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    resume_url = StringField('Resume URL', validators=[DataRequired(), URL()])
    experience = IntegerField('Years of Experience', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Apply')

@app.route('/job', methods=['GET', 'POST'])
def job():
    form = JobApplicationForm()
    if form.validate_on_submit():
        flash(f"🎉 Thank you {form.name.data} for applying!", "success")
        return redirect(url_for('job'))
    return render_template('job_application.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
