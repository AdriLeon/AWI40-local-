import sqlite3 as sql
import web
import json
import hashlib

urls = (
    '/login', 'Login',
    '/signup', 'Signup',
    '/inicio', 'Inicio',
)

app =  web.application(urls, globals())
render = web.template.render('views')


class Login:
    def GET(self):
        return render.login() 
            
    def POST(self):
        formulario = web.input()
        email = formulario.email
        password = formulario.password
        conn =  sql.connect('test.db')
        cur = conn.cursor()
        statement = f"SELECT * from USUARIOS WHERE EMAIL='{email}' AND PASSWORD='{password}'" #crea una variable donde se almacenara la consulta a la base de datos con los datos que ingresamos en el formulario
        cur.execute(statement) #ejecuta la consulta
        if cur.fetchone():#se comprueba el retorno de datos
            result = cur.execute(f"SELECT LOCALID FROM USUARIOS")
            localID = result.fetchone()
            print("Login successfully, correo:", email, "ID:", localID) #imprimimos un mensaje de que fue correcta el ingreso, mostramos el correo y la ID
            web.setcookie('localID', localID, 3600) # se almacena en una cookie el localID
            print("localId: ",web.cookies().get('localID')) # se imprime la cookie para verificar que se almaceno correctamente
            return web.seeother("inicio")#redirecciona a otra pagina web
        else:
            return render.login("Correo/Contraseña incorrectos")#renderiza a login pero con un mensaje


class Signup:
    def GET(self):
        return render.signup() 
            
    def POST(self):
        formulario = web.input()
        email = formulario.email
        password = formulario.password
        print("el correo es ", email, " y la contraseña es ", password)
        conn =  sql.connect('test.db')
        cur = conn.cursor()
        result = hashlib.md5(email.encode())
        localID = result.hexdigest()
        print(result.hexdigest())
        insertStat = f"INSERT INTO USUARIOS(EMAIL, PASSWORD, LOCALID) VALUES ('{email}', '{password}', '{localID}')"#crea una variable donde se almacenara la operacion de insertar a la base de datos con los datos que ingresamos en el formulario
        cur.execute(insertStat)
        conn.commit()#guardamos los dato que hemos ingresado
        statement = f"SELECT * from USUARIOS WHERE EMAIL='{email}' AND PASSWORD='{password}'"#crea una variable donde se almacenara la consulta a la base de datos con los datos que ingresamos en el formulario
        cur.execute(statement) #ejecuta la consulta
        if cur.fetchone():#se comprueba el retorno de datos
            print("Sign Up successfully, correo:", email, "ID:", localID) #imprimimos un mensaje de que fue correcta el ingreso, mostramos el correo y la ID
            web.setcookie('localID', localID, 3600) # se almacena en una cookie el localID
            print("localId: ",web.cookies().get('localID')) # se imprime la cookie para verificar que se almaceno correctamente
            return web.seeother("login")#redirecciona a otra pagina web
        else:
            return render.signup("Error al registrarse")#renderiza a login pero con un mensaje


class Inicio:
    def GET(self):
        return render.inicio() # renderiza a inicio.html
        



if __name__ == "__main__":
    web.config.debug = False
    app.run()
