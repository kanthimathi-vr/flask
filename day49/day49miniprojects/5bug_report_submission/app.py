from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class BugReportForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    description = TextAreaField('Bug Description', validators=[DataRequired()])
    severity = RadioField('Severity', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit Report')

@app.route('/report', methods=['GET', 'POST'])
def report():
    form = BugReportForm()
    if form.validate_on_submit():
        severity = form.severity.data
        if severity == 'high':
            flash('🚨 High severity bug reported. Our team will investigate immediately!', 'danger')
        elif severity == 'medium':
            flash('⚠️ Medium severity bug received. We’ll take a look soon.', 'warning')
        else:
            flash('ℹ️ Low severity bug noted. Thank you for your feedback.', 'info')
        return redirect(url_for('report'))
    return render_template('bug_report.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
