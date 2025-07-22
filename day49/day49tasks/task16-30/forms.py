from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField, BooleanField, TextAreaField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional, Regexp, ValidationError

def block_test_domain(form, field):
    if field.data.lower().endswith('@test.com'):
        raise ValidationError("Emails from test.com are not allowed.")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=3, message="Name must be at least 3 characters."),
        Regexp(r'^[A-Za-z]+$', message="Name must contain only letters.")
    ])

    email = StringField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Enter a valid email."),
        block_test_domain
    ])

    username = StringField("Username", validators=[
        DataRequired(message="Username is required."),
        Length(min=6, message="Username must be at least 6 characters.")
    ])

    age = IntegerField("Age", validators=[
        DataRequired(message="Age is required."),
        NumberRange(min=18, max=60, message="Age must be between 18 and 60.")
    ])

    message = TextAreaField("Message (Optional)", validators=[
        Optional()
    ])

    gender = RadioField("Gender", choices=[('male', 'Male'), ('female', 'Female')], validators=[
        DataRequired(message="Please select your gender.")
    ])

    country = SelectField("Country", choices=[('us', 'USA'), ('ca', 'Canada'), ('uk', 'UK')], validators=[
        DataRequired(message="Please select a country.")
    ])

    terms = BooleanField("I accept the terms and conditions", validators=[
        DataRequired(message="You must accept the terms.")
    ])

    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required.")
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo("password", message="Passwords must match.")
    ])

    date = DateField("Date", format='%Y-%m-%d', validators=[
        DataRequired(message="Date is required.")
    ])

    number = IntegerField("Favorite Number", validators=[
        DataRequired(message="Please enter a number.")
    ])

    submit = SubmitField("Submit")
