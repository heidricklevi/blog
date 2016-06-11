import hashlib
import base64
import os

class PasswordHelper():
    def get_hash(self, plain):
        return hashlib.sha512(str(plain).encode('utf-8')).hexdigest()

    def get_salt(self):
        return str(base64.b64encode(os.urandom(20)))

    def validate_password(self, plain, salt, expected):
        return self.get_hash(plain + str(salt)) == expected

