from re import L
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, widgets
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user != None:
            raise ValidationError('Username already exists! Try a different username')
    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email != None:
            raise ValidationError('Email address already exists! Try a different email address.')
            
    
    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=2, max=30), DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create account')

class LoginForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Log In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell this item')
