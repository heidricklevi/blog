import datetime
from flask import Flask, session, render_template, request, flash, redirect, url_for, abort
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask.ext.moment import Moment
from dbhelper import DBHelper
import config
from flask.ext.moment import Moment
from user import User
import bcrypt
from forms import RegistrationForm, LoginForm, EditProfileForm
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

@application.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

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

@application.route('/account')
@login_required
def account():
    return render_template("account.html")

@application.route('/user/<name>')
def user(name):
    current = current_user._get_current_object()
    user = DB.get_user_data(current.email)
    if user is None:
        abort(404)
    return render_template("user.html", user=user)

@application.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        DB.update_user_profile(current_user)
        return redirect(url_for('.user', name=current_user.name))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)



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

    ROLE = ROLE_ADMINISTRATOR if form.email.data in config.administrators else ROLE_USER
    DB.create_user(ROLE, form.name.data, form.email.data, datetime.datetime.now(), hashed,
                       datetime.datetime.now(), False)
    user = User(form.email.data, hashed, False, ROLE)

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

@application.route('/admin/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    user = current_user._get_current_object()
    print(user.id)
    if user.role != ROLE_ADMINISTRATOR:  # Extra precautionary
        abort(403)
    if user.id == id:
        abort(403)  # current logged in admin cannot delete themselves

    DB.delete_user(id)
    return redirect(url_for('admin_panel'))


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
