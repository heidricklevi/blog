from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import dbhelper
import config
import os, shutil


class User(dbhelper.DBHelper):

    def __init__(self, email, password, confirmed, role):
        self.email = email
        self.password = password
        self.role = role
        self.confirmed = confirmed

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.email})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.email:
            return False
        self.confirmed = True
        dbhelper.DBHelper().update_confirmed_state(self.confirmed)
        return True

    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_email(self):
        return self.email








