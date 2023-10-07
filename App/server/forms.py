from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class SignupForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    

