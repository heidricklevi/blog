import pymysql
import datetime
import dbconfig
import bcrypt
from passwordhelper import PasswordHelper

class DBHelper():

    def connect(self, database='blog'):
        return pymysql.connect(host='localhost', user=dbconfig.db_user,
                               passwd=dbconfig.db_password, db=database)

    def get_all_users(self):
        connection = self.connect()
        try:
            query = "SELECT * FROM blog.users;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()

        finally:
            connection.close()

    def get_user_login(self, email):
        connection = self.connect()
        try:
            query = "SELECT email, password FROM blog.users WHERE email = %(email)s"
            with connection.cursor() as cursor:
                cursor.execute(query, {"email": email})
                return cursor.fetchall()

        finally:
            connection.close()

    def get_user(self, email):
        connection = self.connect()
        try:
            query = "SELECT email FROM blog.users WHERE email = %(email)s;"
            with connection.cursor() as cursor:
                cursor.execute(query, {"email": email})
            return cursor.fetchall()

        finally:
            connection.close()

    def create_user(self, name, email, registration_date, is_admin, password, modified_at):
        connection = self.connect()
        try:
            query = "INSERT INTO users (name, email, registration_date, is_admin, password, modified_at) VALUES (%s, %s, %s, %s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (name, email, registration_date, is_admin, password, modified_at))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()
    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()

    def get_all_crimes(self):
        connection = self.connect()
        try:
            query = "SELECT latitude, longitude, date, category, description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            named_crimes = []
            for crime in cursor:
                named_crime = {
                    "latitude": crime[0],
                    "longitude": crime[1],
                    "date": datetime.datetime.strftime(crime[2], '%Y-%m-%d'),
                    "category": crime[3],
                    "description": crime[4]
                }
                named_crimes.append(named_crime)
            return named_crimes
        finally:
            connection.close()
# DB = DBHelper()
# PH = PasswordHelper()
# hash = bcrypt.hashpw(b'akasis12', bcrypt.gensalt())
# DB.create_user("Test", "j@heidritech.com", datetime.datetime.now(), 0, hash, datetime.datetime.now())
# user = DB.get_user_login("j@heidritech.com")
# stored_pass = str(user[0][1]).encode()
# entered = b'akasis123'
# if bcrypt.hashpw(entered, stored_pass) == stored_pass:
#     print("True")
# else:
#     print("False")