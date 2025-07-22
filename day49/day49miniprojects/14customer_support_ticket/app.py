import random
import string
from flask import Flask, render_template, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class SupportTicketForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    issue_category = SelectField(
        'Issue Category',
        choices=[('billing', 'Billing'), ('technical', 'Technical'), ('general', 'General Inquiry')],
        validators=[DataRequired()]
    )
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=25)])
    submit = SubmitField('Submit Ticket')

def generate_ticket_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/support', methods=['GET', 'POST'])
def support():
    form = SupportTicketForm()
    if form.validate_on_submit():
        ticket_id = generate_ticket_id()
        flash(f"🎫 Support ticket submitted successfully! Your ticket ID: {ticket_id}", "success")
        return redirect(url_for('support'))
    return render_template('support_ticket.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
