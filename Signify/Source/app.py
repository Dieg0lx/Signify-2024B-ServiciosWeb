from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename 
import os
from datetime import timedelta
import pymysql

app = Flask(__name__)

# Session configuration
app.secret_key = os.urandom(24)
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set a default value even if sessions aren't permanent
app.config['SESSION_TYPE'] = 'filesystem'

app.debug = True

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'source/static/images')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

mysql = None

try:
    mysql = pymysql.connect(
        host='localhost',
        user='root',
        password='cesar123',
        db='signify_db',
        ssl={"ssl": {"tls_version": "TLSv1.2"}}  # Esto es opcional si tu servidor requiere SSL
    )
    print("¡Conexión a la base de datos exitosa!")

except pymysql.MySQLError as e:
    print(f"Error de conexión: {e}")

from routes.router import *

print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule}")

if __name__ == '__main__':
    app.run(debug=True)