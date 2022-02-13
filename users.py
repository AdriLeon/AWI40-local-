import sqlite3 as sql
import hashlib

conn =  sql.connect('test.db')



print("Created and Opened database successfully!")

conn.execute("DROP TABLE IF EXISTS USUARIOS;")

conn.execute('''CREATE TABLE USUARIOS(
            ID  integer  PRIMARY KEY autoincrement,
            EMAIL   TEXT    NOT NULL,
            PASSWORD    TEXT    NOT NULL,
            LOCALID TEXT    NOT NULL);''')

print("Table created successfully")

email = "correo@dominio.com"
password = "123456789"

insertStat = f"INSERT INTO USUARIOS(EMAIL, PASSWORD) VALUES ('{email}', '{password}')"
emails = "correo@dominio.com"
passwords = "123456789"

cur = conn.cursor()
idu = conn.cursor()

cur.execute(insertStat)

statement = f"SELECT ID, PASSWORD FROM USUARIOS"
cur.execute(statement)
print(cur.fetchone()[0])

statement1 = f"SELECT * from USUARIOS WHERE EMAIL='{email}' AND PASSWORD='{password}';"
cur.execute(statement1)
idu.execute(statement)
if not cur.fetchone(): # An empty result evaluates to False.
    print("Login Failed")
else:
     print("Login successfully, correo:", email, "ID:",idu.fetchone()[0])

usu = "usuario@dominio.com"
result = hashlib.md5(usu.encode())
idl = result.hexdigest()
print(result.hexdigest())

id = f"insert into usuarios(id, email, password) values('{idl}', '{usu}', 'password')"
cur.execute(id)

statement = f"SELECT * FROM USUARIOS"

cur = conn.cursor()
cur.execute(statement)
print(cur.fetchall())