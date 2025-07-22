from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=3, message="Name must be at least 3 characters.")
    ])
    email = EmailField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required.")
    ])
    submit = SubmitField("Submit")
