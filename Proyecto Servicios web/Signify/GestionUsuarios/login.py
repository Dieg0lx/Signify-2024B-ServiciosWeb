from flask import Flask, request, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'database': 'GestionUsuarios'
}

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def login():
    username = request.form['usuario']
    password = request.form['contrasena']

    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Consulta SQL para verificar las credenciales
    query = "SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return redirect(url_for('welcome'))
    else:
        return "Credenciales incorrectas"

@app.route('/welcome')
def welcome():
    return "Bienvenido!"

if __name__ == '__main__':
    app.run(debug=True)
