import datetime
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask.ext.moment import Moment

import user
from dbhelper import DBHelper
import config
from user import User
import bcrypt
from forms import RegistrationForm, LoginForm
import email

application = Flask(__name__)
application.secret_key = config.app_key_auth
login_manager = LoginManager(application)
DB = DBHelper()
moment = Moment(application)

@application.route('/')
def home():
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

    DB.create_user(1, form.name.data, form.email.data, datetime.datetime.now(), hashed,
                       datetime.datetime.now(), True)


    return render_template("register.html", registrationform=form)

@application.route('/admin')
@login_required
def admin_panel():
    records = DB.get_all_users()
    return render_template("admin.html", records=records)

@application.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("home"))


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
            user = User(form.email.data, hashed, stored_user[0][2])
            login_user(user, remember=True)
            return render_template("login.html", loginform=form)

        form.email.errors.append("Email or Password is invalid")
    return render_template("login.html", loginform=form)

@login_manager.user_loader
def load_user(user_id):
    stored_user = DB.get_user_login(user_id)
    user_password = str(stored_user[0][1].encode())
    if user_password:
        return User(stored_user[0][0], user_password, stored_user[0][2])

if __name__ == '__main__':
    application.debug = True
    application.run()
