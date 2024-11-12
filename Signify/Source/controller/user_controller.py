# user_controller.py
from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
from app import mysql
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.cursor()
        error = None
        
        if not nombres or not apellidos or not email or not password:
            error = 'Todos los campos son requeridos.'
        elif len(password) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'
        else:
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone() is not None:
                error = 'El correo electrónico ya está registrado.'
        
        if error is None:
            try:
                cur.execute(
                    "INSERT INTO users (nombres, apellidos, email, password, join_date) VALUES (%s, %s, %s, %s, %s)",
                    (nombres, apellidos, email, generate_password_hash(password), datetime.now().strftime('%Y-%m-%d'))
                )
                mysql.commit()
                return redirect(url_for('login'))
            except Exception as e:
                error = 'Error al registrar el usuario.'
                print(e)  # For debugging
        
        flash(error)
        cur.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()  # Clear any existing session
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            
            if user and check_password_hash(user[4], password):
                session['user_id'] = user[0]
                session.permanent = False  # Session expires when browser closes
                return redirect(url_for('courses_page'))
            else:
                flash('Correo o contraseña incorrectos')
        finally:
            cur.close()
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        
        user_data = {
            'nombres': user[1],
            'apellidos': user[2],
            'email': user[3],
            'join_date': user[5].strftime('%d de %B de %Y') if user[5] else '',
            'completed_courses': user[6] or 0,
            'total_points': user[7] or 0,
            'profile_image': user[8] if user[8] else 'default.png'  # Asegurarse de que este índice es correcto
        }
        return render_template('profile.html', user=user_data)
    finally:
        cur.close()
        

@app.route('/delete-account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (session['user_id'],))
    mysql.commit()
    cur.close()
    session.clear()
    flash('Tu cuenta ha sido eliminada', 'info')
    return redirect(url_for('home'))

@app.route('/upload-profile-image', methods=['POST'])
def upload_profile_image():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'profile_image' not in request.files:
        flash('No file part')
        return redirect(url_for('profile'))
    
    file = request.files['profile_image']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('profile'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        new_filename = f"user_{session['user_id']}.{file_extension}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        
        cur = mysql.cursor()
        cur.execute("UPDATE users SET profile_image = %s WHERE id = %s", (new_filename, session['user_id']))
        mysql.commit()
        cur.close()
        
        flash('Profile image updated successfully')
    else:
        flash('Invalid file type')
    
    return redirect(url_for('profile'))

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        user_id = session.get('user_id')
        if not user_id:
            flash('Usuario no autenticado.')
            return redirect(url_for('login'))
        
        cur = mysql.cursor()
        cur.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        
        if not user:
            flash('Usuario no encontrado.')
            return redirect(url_for('change_password'))
        
        # Use check_password_hash to verify the current password
        if not check_password_hash(user[0], current_password):
            flash('Contraseña actual incorrecta.')
            return redirect(url_for('change_password'))
        
        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden.')
            return redirect(url_for('change_password'))
        
        if len(new_password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.')
            return redirect(url_for('change_password'))
        
        # Hash the new password before storing
        hashed_password = generate_password_hash(new_password)
        
        # Update the password in the database
        cur = mysql.cursor()
        cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))
        mysql.commit()
        cur.close()
        
        flash('Contraseña actualizada exitosamente.')
        return redirect(url_for('profile'))
    
    return render_template('change_password.html')