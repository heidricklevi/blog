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
                               cursorclass=pymysql.cursors.DictCursor)\

    def delete_user(self, id):
        conn = self.connect()
        try:
            query = "DELETE FROM blog.users WHERE id = %s;"
            with conn.cursor() as cursor:
                cursor.execute(query, id)
                conn.commit()
        finally:
            conn.close()

    def get_user_by_name(self, name):  # temp until unique username is added to db
        conn = self.connect()
        try:
            query = "SELECT * FROM blog.users WHERE name = %s;"
            with conn.cursor() as cursor:
                cursor.execute(query, name)
                return cursor.fetchall()
        finally:
            conn.close()


    def update_user(self, user):
        conn = self.connect()

        try:
            query = "UPDATE blog.users SET roles_id = %s, name = %s, email = %s," \
                    " registration_date = %s, password = %s, modified_at = %s, confirmed = %s, location = %s, about_me = %s WHERE id = %s"
            with conn.cursor() as cursor:
                cursor.execute(query, (user[0]["roles_id"], user[0]["name"], user[0]["email"],
                                       user[0]["registration_date"], user[0]["password"], user[0]["modified_at"], user[0]["confirmed"],
                                       user[0]["location"], user[0]["about_me"], user[0]["id"]))
                conn.commit()
        finally:
            conn.close()

    def insert_gravatar_hash(self, email, hash):
        conn = self.connect()
        try:
            query = "UPDATE blog.users SET gravatar_hash = %s WHERE email = %s; "
            with conn.cursor() as cursor:
                cursor.execute(query, (hash, email))
                conn.commit()
        finally:
            conn.close()


    def get_user_data(self, email):
        connection = self.connect()
        try:
            query = "SELECT * FROM blog.users WHERE email = %s;"
            with connection.cursor() as cursor:
                cursor.execute(query, email)
            return cursor.fetchall()

        finally:
            connection.close()

    def get_user_by_id(self, id):
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

    def create_blog_post(self, author_id, body, post_time):
        conn = self.connect()
        try:
            query = "INSERT INTO posts (author_id, body, post_time) VALUES (%s, %s, %s);"
            with conn.cursor() as cursor:
                cursor.execute(query, (author_id, body, post_time))
                conn.commit()
        finally:
            conn.close()


    def insert_roles(self, roles_id, permissions):
        conn = self.connect()

        try:
                query = "UPDATE blog.roles SET permissions = %s WHERE roles_id = %s"
                with conn.cursor() as cursor:
                    cursor.execute(query, (permissions, roles_id))
                    conn.commit()
        finally:
          conn.close()

    def get_all_posts(self):
        conn = self.connect()
        try:
            query = "select users.name, posts.author_id, posts.body, posts.post_time, posts.posts_id " \
                    "from blog.posts join users on posts.author_id = users.id ORDER BY post_time DESC;"
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
                return cursor.fetchall()
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


    def update_user_profile(self, user):
        conn = self.connect()
        try:
            query = "UPDATE blog.users SET name = %s, location = %s, about_me = %s WHERE email = %s"
            with conn.cursor() as cursor:
                cursor.execute(query, (user.name, user.location, user.about_me, user.email))
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