import psycopg2 #importamos la librería necesaria para la comunicación con postgresql

conn = psycopg2.connect( #Aquí es donde se realiza la conexión con la base de datos
    host="127.0.0.1",
    database="twitter_app_db",
    user="postgres",
    password="admin123",
    port="8081")
