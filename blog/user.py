from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import dbhelper
import config
import os, shutil



#model for MySQL db is tuple -- ((name, email, registration_date, is_admin, password, modified_at, confirmed),) --> access by index

class User(dbhelper.DBHelper):

    def __init__(self, email, password, confirmed):
        self.email = email
        self.password = password
        self.confirmed = confirmed

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








