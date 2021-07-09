"""import psycopg2 #importamos la librería necesaria para la comunicación con postgresql

conn = psycopg2.connect( #Aquí es donde se realiza la conexión con la base de datos
    host="127.0.0.1",
    database="twitter_app_db",
    user="postgres",
    password="admin123",
    port="8081")
"""

import psycopg2
from psycopg2.pool import SimpleConnectionPool

dbConnection = "dbname='twitter_app_db' user='postgres' host='127.0.0.1' password='admin123' port='8081'"

class PostgresSQLPool(object):

    def __init__(self):             
        self.postgreSQL_pool = self.create_pool(pool_size=0)

    def create_pool(self, pool_size):

        postgreSQL_pool = SimpleConnectionPool(1,pool_size,dsn=dbConnection)
        return postgreSQL_pool

    def close(self, conn, cursor):
        
        cursor.close()
        conn.close()
        #self.postgreSQL_pool.putconn(conn)

    def execute(self, sql, args=None, commit=False):
        # get connection form connection pool instead of create one.
        conn = self.postgreSQL_pool.getconn()
        cursor = conn.cursor()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        if commit is True:
            conn.commit()
            res = cursor.fetchone()
            self.close(conn, cursor)
            return res
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res