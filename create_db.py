import psycopg2
sql = "CREATE DATABASE workshop;"
sql_u="""CREATE TABLE users(
id serial,
username varchar(255) unique,
hashed_password varchar(80),
PRIMARY KEY(id)
);
"""
sql_m="""CREATE TABLE messages(
id serial,
from_id integer REFERENCES users(id) ON DELETE CASCADE,
to_id integer REFERENCES users(id) ON DELETE CASCADE,
creation_date timestamp DEFAULT CURRENT_TIMESTAMP,
text varchar(255),
PRIMARY KEY(id)
);
"""
try:
    cnx = psycopg2.connect(user="postgres", password="coderslab", host="localhost")
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(sql)
    print("The database created.")
except psycopg2.errors.OperationalError:
    print("Error with connection to postgres!")
except psycopg2.errors.DuplicateDatabase:
    print("The database already exists!")
else:
    cursor.close()
    cnx.close()

try:
    cnx = psycopg2.connect(user="postgres", password="coderslab", host="localhost", database="workshop")
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(sql_u)
    print("Table users created.")
    cursor.execute(sql_m)
    print("Table messages created.")
except psycopg2.errors.OperationalError:
    print("Error with connection to postgres!")
except psycopg2.errors.DuplicateTable:
    print("Table(s) already esist(s)!")
else:
    cursor.close()
    cnx.close()