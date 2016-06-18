import pymysql
import datetime
import dbconfig
import bcrypt


class DBHelper():

    def connect(self, database=dbconfig.db_name):
        return pymysql.connect(host=dbconfig.dev_host, user=dbconfig.db_user,
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
            query = "SELECT email, password, confirmed FROM blog.users WHERE email = %(email)s"
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
                # query = "INSERT INTO roles (name, default_permission, permissions) VALUES (%s, %s, %s);"
                query = "UPDATE blog.roles SET permissions = %s WHERE roles_id = %s"
                with conn.cursor() as cursor:
                    cursor.execute(query, (permissions, roles_id))
                    conn.commit()
        finally:
          conn.close()

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTRATOR = 0x80

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

roles = {
            'User': (True, Permission.FOLLOW | Permission.COMMENT),
            'Moderator': (False, Permission.FOLLOW | Permission.COMMENT | Permission.MODERATE_COMMENTS),
            'Admin': (False, Permission.ADMINISTRATOR)
        }
db = DBHelper()
# db.insert_roles("User", True, Permission.FOLLOW | Permission.COMMENT)

# db.insert_roles("Administrator", False, Permission.ADMINISTRATOR)



