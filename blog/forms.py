from flask_wtf import Form
from wtforms import PasswordField, TextField, TextAreaField, BooleanField, IntegerField, HiddenField
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.validators import Length


class RegistrationForm(Form):
    name = TextField('name', validators=[validators.DataRequired()])
    username = TextField('username', validators=[validators.data_required()])
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=8, message="Password must be at least 8 chars")])
    password2 = PasswordField('password2', validators=[validators.DataRequired(), validators.EqualTo('password', message="passwords must match")])
    submit = SubmitField('submit', [validators.DataRequired()])


class LoginForm(Form):
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])

class EditProfileForm(Form):
    name = StringField('Real Name', validators=[Length(0, 64)])
    location = StringField("Location", validators=[Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

class User_EditForm(Form):
    name = HiddenField("name")
    location = HiddenField("Location", validators=[Length(0,64)])
    about_me = HiddenField('About Me')
    email = HiddenField('Email', validators=[validators.DataRequired(), Length(1, 64), EmailField()])
    confirmed = IntegerField("Confirmed")
    role = IntegerField('role')

class PostForm(Form):
    body = HiddenField("Type Blog content here.", validators=[validators.DataRequired()])
    title = TextField("Put your Blog post title here...", validators=[validators.DataRequired()])
    submit = SubmitField("Submit")