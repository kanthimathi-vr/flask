from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuizForm(FlaskForm):
    q1 = RadioField('What is 2 + 2?', choices=[('3','3'),('4','4'),('5','5')], validators=[DataRequired()])
    q2 = RadioField('Capital of France?', choices=[('London','London'),('Paris','Paris'),('Berlin','Berlin')], validators=[DataRequired()])
    submit = SubmitField('Submit Quiz')
