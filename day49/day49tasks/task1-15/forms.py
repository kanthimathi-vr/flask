from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, RadioField, SelectField, BooleanField, PasswordField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class UserForm(FlaskForm):
    # task 1
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    
    gender = RadioField("Gender", choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
    country = SelectField("Country", choices=[("us", "USA"), ("ca", "Canada"), ("uk", "UK")], validators=[DataRequired()])
    terms = BooleanField("I accept the terms", validators=[DataRequired()])
    
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    number = IntegerField("Favorite Number", validators=[DataRequired()])
    
    submit = SubmitField("Submit")
