from datetime import datetime
from flask_mysqldb import MySQL

class User:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def register(self, nombres, apellidos, email, password):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (nombres, apellidos, email, password, join_date) VALUES (%s, %s, %s, %s, %s)",
                (nombres, apellidos, email, password, datetime.now().strftime('%Y-%m-%d'))
            )
            self.mysql.connection.commit()
            cur.close()
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            return False
        return True

    def get_by_email(self, email):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user

    def get_by_id(self, user_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return user
