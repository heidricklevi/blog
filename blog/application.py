import datetime
from flask import Flask, session, render_template, request, flash, redirect, url_for, abort
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask.ext.moment import Moment
from dbhelper import DBHelper
import config
from user import User
import bcrypt
from forms import RegistrationForm, LoginForm
from flask_mail import Mail
from flask.ext.mail import Message
import smtplib

application = Flask(__name__)
application.secret_key = config.app_key_auth
login_manager = LoginManager(application)
DB = DBHelper()
moment = Moment(application)
mail = Mail(application)

ROLE_USER = 1
ROLE_MODERATOR = 2
ROLE_ADMINISTRATOR = 3



def send_email(user_fromaddress, pwd, recipient, subject, **kwargs ):

    gmail_user = user_fromaddress
    gmail_pwd = pwd
    FROM = user_fromaddress
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = render_template('mail.txt', **kwargs)

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")




@application.route('/')
def home():
    return render_template("index.html")

# @application.before_request
# def before_request():
#     if current_user.is_authenticated and not current_user.confirmed:
#         return redirect(url_for('unconfirmed'))
#
# @application.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect('home')
#     return render_template('unconfirmed.html')

@application.route('/confirm')
@login_required
def resend_confirmation():
    user = current_user._get_current_object()
    if user.confirmed:
        return render_template("index.html")
    token = user.generate_confirmation_token()

    send_email(config.from_address, config.mail_password, config.to_address, "Confirmation Email", user=user, token=token)
    return redirect(url_for('home'))

@application.route('/confirm/<token>')
@login_required
def confirm(token):
    user = current_user._get_current_object()
    if current_user.confirmed:
        print(user.confirmed)
        return redirect(url_for('home'))
    if current_user.confirm(token):
        print('successfully confirmed')
        flash("Thank you for confirming your account!")
        if user.role == ROLE_ADMINISTRATOR:
            return render_template('admin.html')
    else:
        flash("Confirmation link invalid or expired.")
    return redirect(url_for('login'))

@application.route('/register', methods=['GET'])
def register():
    return render_template("register.html", registrationform=RegistrationForm())

@application.route('/register/createaccount', methods=['POST'])
def create_user():
    form = RegistrationForm(request.form)
    stored_user = DB.get_user_login(form.email.data)
    if stored_user:
        form.email.errors = list()
        form.email.errors.append("Email Address Already Registered")
        return render_template("register.html", registrationform=form)

    hashed = bcrypt.hashpw(str(form.password.data).encode(), bcrypt.gensalt())
    DB.create_user(ROLE_USER, form.name.data, form.email.data, datetime.datetime.now(), hashed,
                       datetime.datetime.now(), False)
    user = User(form.email.data, hashed, False, ROLE_USER)

    token = User.generate_confirmation_token(user, expiration=3600)
    send_email(config.mail_username, config.mail_password, config.to_address, "test", user=user, token=token)

    return render_template("register.html", registrationform=form)

@application.route('/admin')
@login_required
def admin_panel():
    records = DB.get_all_users()
    user = current_user._get_current_object()
    if user.role != ROLE_ADMINISTRATOR:
        abort(403)
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
        hashed = str(stored_user[0]['password']).encode()
        if stored_user and bcrypt.hashpw(str(form.password.data).encode(), hashed) == hashed:
            user = User(form.email.data, hashed, stored_user[0]['confirmed'], stored_user[0]['roles_id'])
            login_user(user, remember=True)
            return render_template("login.html", loginform=form)

        form.email.errors.append("Email or Password is invalid")
    return render_template("login.html", loginform=form)

@login_manager.user_loader
def load_user(user_id):
    stored_user = DB.get_user_login(user_id)
    user_password = str(stored_user[0]['password'].encode())
    if user_password:

        return User(stored_user[0]['email'], user_password, stored_user[0]['confirmed'], stored_user[0]['roles_id'])


if __name__ == '__main__':
    application.debug = True
    application.run()
