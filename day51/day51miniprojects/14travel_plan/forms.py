from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TravelPlanForm(FlaskForm):
    place = StringField('Place', validators=[DataRequired(), Length(max=150)])
    travel_date = DateField('Travel Date (YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    reason = TextAreaField('Reason', validators=[Length(max=255)])
    submit = SubmitField('Add Plan')

class SearchForm(FlaskForm):
    country = StringField('Search by Country')
    submit = SubmitField('Search')
