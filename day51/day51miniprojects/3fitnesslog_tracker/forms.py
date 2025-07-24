from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class WorkoutForm(FlaskForm):
    type = StringField('Workout Type', validators=[DataRequired()])
    steps = IntegerField('Steps', validators=[NumberRange(min=0)], default=0)
    hours = FloatField('Hours', validators=[NumberRange(min=0)], default=0.0)
    submit = SubmitField('Log Workout')

class ProfileForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[])
    confirm = PasswordField('Confirm New Password',
                            validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update Profile')
