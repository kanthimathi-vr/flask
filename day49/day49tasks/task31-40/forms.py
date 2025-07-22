from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField, BooleanField, TextAreaField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional, Regexp, ValidationError

def block_test_domain(form, field):
    if field.data.lower().endswith('@test.com'):
        raise ValidationError("Emails from test.com are not allowed.")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(), Length(min=3), Regexp(r'^[A-Za-z]+$', message="Letters only")
    ])
    email = StringField("Email", validators=[
        DataRequired(), Email(), block_test_domain
    ])
    username = StringField("Username", validators=[
        DataRequired(), Length(min=6)
    ])
    age = IntegerField("Age", validators=[
        DataRequired(), NumberRange(min=18, max=100)
    ])
    gender = RadioField("Gender", choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    country = SelectField("Country", choices=[('us', 'USA'), ('uk', 'UK'), ('ca', 'Canada')], validators=[DataRequired()])
    message = TextAreaField("Message (optional)", validators=[Optional()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match.")
    ])
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    number = IntegerField("Favorite Number", validators=[DataRequired()])
    terms = BooleanField("Accept Terms", validators=[DataRequired()])
    submit = SubmitField("Submit")
