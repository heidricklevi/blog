from flask_wtf import Form
from wtforms import PasswordField, TextField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class RegistrationForm(Form):
    name = TextField('name', validators=[validators.DataRequired()])
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=8, message="Password must be at least 8 chars")])
    password2 = PasswordField('password2', validators=[validators.DataRequired(), validators.EqualTo('password', message="passwords must match")])
    submit = SubmitField('submit', [validators.DataRequired()])


class LoginForm(Form):
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])