import pymysql
import dbconfig
import datetime


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTRATOR = 0x80

class DBHelper():

    def connect(self, database=dbconfig.db_name):
        return pymysql.connect(host=dbconfig.dev_host, user=dbconfig.db_user,
                               passwd=dbconfig.db_password, db=database,
                               cursorclass=pymysql.cursors.DictCursor)

    def get_user_data(self, id):
        connection = self.connect()
        try:
            query = "SELECT * FROM blog.users WHERE id = %s;"
            with connection.cursor() as cursor:
                cursor.execute(query, id)
            return cursor.fetchall()

        finally:
            connection.close()


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
            query = "SELECT email, password, confirmed, roles_id FROM blog.users WHERE email = %(email)s"
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

    def create_user(self, roles_id, name, email, registration_date, password, modified_at, confirmed):
        connection = self.connect()
        try:
            query = "INSERT INTO users (roles_id, name, email, registration_date, password, modified_at, confirmed) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (roles_id, name, email, registration_date, password, modified_at, confirmed))
                connection.commit()
        except Exception as e:
                print(e)
        finally:
            connection.close()

    def insert_roles(self, roles_id, permissions):
        conn = self.connect()

        try:
                query = "UPDATE blog.roles SET permissions = %s WHERE roles_id = %s"
                with conn.cursor() as cursor:
                    cursor.execute(query, (permissions, roles_id))
                    conn.commit()
        finally:
          conn.close()

    def update_user_permissions(self, roles, email):
        conn = self.connect()

        try:
            query = "UPDATE blog.users SET roles_id = %(roles)s WHERE email = %(email)s"
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
        finally:
            conn.close()

    def update_confirmed_state(self, user):
        conn = self.connect()
        try:
            query = "UPDATE blog.users SET confirmed = %s WHERE email = %s"
            with conn.cursor() as cursor:
                cursor.execute(query, (user.confirmed, user.email))
                conn.commit()
        finally:
            conn.close()

    def get_modified_date_time(self, email):
        conn = self.connect()
        try:
            query = "SELECT modified_at FROM blog.users WHERE email = %s"
            with conn.cursor() as cursor:
                cursor.execute(query, (email))
                conn.commit()
                return cursor.fetchall()
        except:
            conn.close()

    def get_registration_date(self, email):
        conn = self.connect()
        try:
            query = "SELECT registration_date FROM blog.users WHERE email = %s"
            with conn.cursor() as cursor:
                cursor.execute(query, (email))
                conn.commit()
                return cursor.fetchall()
        except:
            conn.close()

    def update_modified_time(self, modified_at, email):
        conn = self.connect()
        try:
            query = "UPDATE blog.users SET modified_at = %s WHERE email = %s"
            with conn.cursor() as cursor:
                cursor.execute(query, (modified_at, email))
                conn.commit()
        finally:
            conn.close()

class DBRole:
    def update_role_permissions(self, roles_id, permissions):
        conn = DBHelper.connect(DBHelper(), database=dbconfig.db_name)

        try:
                query = "UPDATE blog.roles SET permissions = %s WHERE roles_id = %s"
                with conn.cursor() as cursor:
                    cursor.execute(query, (permissions, roles_id))
                    conn.commit()
        finally:
          conn.close()


    def get_roles(self, name):
        conn = DBHelper.connect(DBHelper(), database=dbconfig.db_name)
        try:
            query = "SELECT * FROM blog.roles WHERE name = s(name)%"
            with conn.cursor() as cursor:
                cursor.execute(query, {'name': name})
                return cursor.fetchall()
        finally:
            conn.close()

# from user import User
# db = DBHelper()
# use = user.User("test1@testemail.com", "12434235234", False, 1)
# # db.create_user(use.role, use.email, use.email, datetime.datetime.now(), use.password, datetime.datetime.now(), use.confirmed)
# use.confirmed = True
# db.update_confirmed_state(use)