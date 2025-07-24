from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AppointmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description')
    appointment_date = DateTimeField('Appointment Date (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')
