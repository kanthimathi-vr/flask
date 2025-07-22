import random
from flask import Flask, render_template, redirect, flash, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class ComplaintForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    complaint = TextAreaField('Complaint', validators=[DataRequired(), Length(min=15, message="Complaint must be at least 15 characters")])
    category = SelectField('Category', choices=[('', 'Select Category'), ('product', 'Product'), ('service', 'Service'), ('billing', 'Billing'), ('other', 'Other')], validators=[DataRequired()])
    submit = SubmitField('Submit Complaint')

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint_id = random.randint(1000, 9999)
        flash(f"✅ Complaint registered successfully! Your complaint number is #{complaint_id}", "success")
        return redirect(url_for('complaint'))
    elif request.method == 'POST':
        # Collect all error messages to display at the top
        errors = []
        for field, error_list in form.errors.items():
            label = getattr(form, field).label.text
            for error in error_list:
                errors.append(f"{label}: {error}")
        flash(errors, "error-box")
    return render_template('complaint.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
