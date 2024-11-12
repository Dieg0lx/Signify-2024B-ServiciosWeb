# routes.py
from app import app
from controller.user_controller import register, login, logout, profile
from flask import redirect, url_for, session
from controller.course_controller import courses_page, start_course, results

# Rutas de la aplicación
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('courses_page'))