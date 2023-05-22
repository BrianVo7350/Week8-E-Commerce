from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUpForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name')
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Email',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField()

class LogInForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField()
    