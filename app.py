from flask import Flask
from flask import render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__,template_folder='Template')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='280603'
app.config['MYSQL_DB']='biblioteca'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

#Funcion de Login

@app.route('/acceso-login', methods= ["GET", "POST"])
def login():

    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword':
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account['id']

            return render_template("admin.html")
        else:

            return render_template('index.html', mensaje="Usuario o clave incorrecta")


#Funcion de Registro

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods= ["GET", "POST"])
def crear_registro():

    correo=request.form['txtCorreo']
    password = request.form['txtPassword']
    nombre = request.form['txtNombre']


    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)", (nombre, correo, password))
    mysql.connection.commit()

    return render_template("index.html", mensaje2="Usuario registrado exitosamente!")

if __name__ == '__main__':
    app.secret_key="Luis2863"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
