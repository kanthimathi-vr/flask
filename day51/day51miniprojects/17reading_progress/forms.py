from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired(), Length(max=200)])
    total_pages = IntegerField('Total Pages', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add Book')

class UpdateProgressForm(FlaskForm):
    pages_read = IntegerField('Pages Read', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Update Progress')
