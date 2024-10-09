from flask import render_template, request, redirect, url_for
from app import db
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from model.usuario import Usuario

def first():
    try:
        # Intentar ejecutar una consulta simple para verificar la conexión
        # db.session.execute(text('SELECT 1'))
        return render_template('login.html')
    except OperationalError:
        return "Vlio verga: Error de conexión a la base de datos"
    
def login():
    if request.method == 'POST':
        username = request.form.get('usuario')  # Nombre del campo en el formulario
        password = request.form.get('contrasena')  # Nombre del campo en el formulario
        print(username, password)
        try:
            user = Usuario.query.filter_by(nombre=username, contrasena=password).first()
            if user:
                render_template('index.html')
            else:
                return "Usuario no encontrado"
        except Exception as e:
            print(e)
    return "Error de conexion"

def second():
    try:
        # Intentar ejecutar una consulta simple para verificar la conexión
        # db.session.execute(text('SELECT 1'))
        return render_template('index.html')
    except OperationalError:
        return "Vlio verga: Error de renderizacion"