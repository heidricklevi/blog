import datetime
from flask import Flask, render_template, request
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from dbhelper import DBHelper
from user import User
from bcrypt import hashpw
import bcrypt
from passwordhelper import PasswordHelper
from forms import RegistrationForm, LoginForm

application = Flask(__name__)
application.secret_key = "11231423513231231312536dkfjsajDhbasdgasdf"
login_manager = LoginManager(application)
DB = DBHelper()
PH = PasswordHelper()


@application.route('/')
def hello_world():
    return render_template("index.html")

@application.route('/register', methods=['GET'])
def register():
    return render_template("register.html", registrationform=RegistrationForm())

@application.route('/register/createaccount', methods=['POST'])
def create_user():
    form = RegistrationForm(request.form)
    stored_user = DB.get_user(form.email.data)
    if stored_user:
        form.email.errors.append("Email Address Already Registered")
        return render_template("register.html", registrationform=form)

    hashed = bcrypt.hashpw(str(form.password.data).encode(), bcrypt.gensalt())

    DB.create_user(form.name.data, form.email.data, datetime.datetime.now(), False, hashed,
                       datetime.datetime.now())
    return render_template("register.html", registrationform=form)

@application.route('/admin')
@login_required
@admin_required

@application.route('/login')
def login_page():
    return render_template('login.html', loginform=LoginForm())

@application.route('/login/verify', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user_login(form.email.data)
        hashed = str(stored_user[0][1]).encode()
        if stored_user and bcrypt.hashpw(str(form.password.data).encode(), hashed) == hashed:
            user = User(form.email.data)
            login_user(user, remember=True)
            return render_template("login.html", loginform=form)

        form.email.errors.append("Email or Password is invalid")
    return render_template("login.html", loginform=form)

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

if __name__ == '__main__':
    application.debug = True
    application.run()
