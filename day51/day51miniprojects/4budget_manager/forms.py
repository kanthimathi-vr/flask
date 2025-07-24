from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError
from models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    amt = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class LimitForm(FlaskForm):
    monthly_limit = FloatField('Set Monthly Limit', validators=[DataRequired(), NumberRange(min=0.01)])
    set_limit = SubmitField('Set Limit')
