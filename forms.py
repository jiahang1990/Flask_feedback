from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, IntegerField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    """Form for register user"""
    username = StringField("Username", validators = [InputRequired(), Length(min=1, max=20)])
    passward = PasswordField("Password", validators = [InputRequired(), Length(min=6, max=55)])
    email = StringField("Email", validators = [InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First name", validators = [InputRequired(), Length(max=30)])
    last_name = StringField("Last name", validators = [InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """Form for login user"""
    username = StringField("Username", validators = [InputRequired(), Length(min=1, max=20)])
    passward = PasswordField("Password", validators = [InputRequired(), Length(min=6, max=55)])

class FeedbackForm(FlaskForm):
    """Form for add new feedback"""
    title = StringField("Title", validators = [InputRequired(), Length(max=100)])
    content = TextAreaField("Content", validators = [InputRequired()])