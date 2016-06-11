import pymysql
import dbconfig

connection = pymysql.connect(host='localhost', port=3306, user=dbconfig.db_user, passwd=dbconfig.db_password)

try:
    with connection.cursor() as cursor:
        sql = "CREATE DATABASE IF NOT EXISTS blog"
        cursor.execute(sql)
        sql = """CREATE TABLE IF NOT EXISTS blog.users (

              id int NOT NULL AUTO_INCREMENT,
              name VARCHAR(1000),
              email VARCHAR(255),
              registration_date DATETIME,
              is_admin BOOLEAN,
              password VARCHAR(255),
              modified_at TIMESTAMP,
               PRIMARY KEY (id))"""

        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()
