# course_controller.py
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app import mysql
from datetime import datetime
from app import app
import base64

def calculate_level(points):
    return points // 100 + 1

def calculate_level_progress(points):
    return (points % 100)

@app.route('/courses')
def courses_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.cursor()
    courses = []
    current_course = None

    try:
        # Obtener cursos con sus preguntas y opciones
        cur.execute("SELECT * FROM courses;")
        rows = cur.fetchall()
        
        for row in rows:
            course_id, course_title = row
            if not current_course or current_course['id'] != course_id:
                current_course = {
                    'id': course_id,
                    'title': course_title,
                }
                courses.append(current_course)
        
        return render_template('courses.html',
                               section_title='Seccion 1',
                               section_subtitle='Abecedario Básico',
                               courses=courses)

    except Exception as e:
        print(f"Database error: {e}")
        return render_template('courses.html',
                               section_title='Seccion 1',
                               section_subtitle='Abecedario Básico',
                               courses=courses)
    finally:
        cur.close()

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cur.fetchone()
    user_data = {
        'completed_courses': user[6],
        'total_points': user[7],
        'level': calculate_level(user[7]),
        'level_progress': calculate_level_progress(user[7]),
        'achievements': [
            {'name': 'Primer Curso', 'icon': 'achievement1.png', 'unlocked': user[6] > 0},
            {'name': '100 Puntos', 'icon': 'achievement2.png', 'unlocked': user[7] >= 100},
            {'name': 'Racha de 3 Días', 'icon': 'achievement3.png', 'unlocked': False},  # Implement streak logic
        ]
    }
    cur.close()
    return render_template('results.html', user=user_data)

@app.route('/course/<int:course_id>', methods=['GET'])
def start_course(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.cursor()
    try:
        # Verificar si el curso existe
        cur.execute("SELECT id, title FROM courses WHERE id = %s", (course_id,))
        course_data = cur.fetchone()
        
        if not course_data:
            flash('Curso no encontrado')
            return redirect(url_for('courses_page'))
            
        # Obtener preguntas del curso, incluyendo la imagen en formato BLOB
        cur.execute("""
            SELECT q.id, q.question_text, q.correct_answer, q.image 
            FROM questions q 
            WHERE q.course_id = %s
        """, (course_id,))
        questions_data = cur.fetchall()
        
        # Estructurar los datos
        course = {
            'id': course_data[0],
            'title': course_data[1],
            'questions': []
        }
        
        # Obtener opciones para cada pregunta
        for question in questions_data:
            cur.execute("""
                SELECT option_text 
                FROM options 
                WHERE question_id = %s
            """, (question[0],))
            options = [opt[0] for opt in cur.fetchall()]
            
            # Convertir el BLOB de la imagen a base64 si existe
            image_base64 = None
            if question[3]:  # Verifica si hay una imagen
                image_base64 = base64.b64encode(question[3]).decode('utf-8')
            
            # Agregar cada pregunta con sus opciones y la imagen en base64
            course['questions'].append({
                'id': question[0],
                'question': question[1],
                'options': options,
                'correct': question[2],
                'image': image_base64
            })
            
        return render_template('course.html', course=course)
        
    except Exception as e:
        print(f"Error loading course: {e}")
        flash('Error al cargar el curso')
        return redirect(url_for('courses_page'))
    finally:
        cur.close()

@app.route('/submit_course/<int:course_id>', methods=['POST'])
def submit_course(course_id):
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
        
    cur = mysql.cursor()
    try:
        # Obtener respuestas del usuario
        answers = request.json
        correct_answers = 0
        total_questions = len(answers)
        
        # Verificar respuestas
        for question_id, answer in answers.items():
            cur.execute("SELECT correct_answer FROM questions WHERE id = %s", (question_id,))
            correct = cur.fetchone()[0]
            if answer == correct:
                correct_answers += 1
        
        # Calcular puntuación
        score = int((correct_answers / total_questions) * 100)
        
        # Guardar resultado
        cur.execute("""
            INSERT INTO course_results 
            (user_id, course_id, score, completed_at) 
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], course_id, score, datetime.now()))
        mysql.commit()
        
        # Actualizar progreso del usuario
        cur.execute("""
            UPDATE users 
            SET completed_courses = completed_courses + 1,
                total_points = total_points + %s 
            WHERE id = %s
        """, (score, session['user_id']))
        mysql.commit()
        
        return jsonify({
            'message': f'¡Curso completado! Puntuación: {score}%',
            'redirect': url_for('course_result', user_id=session['user_id'], course_id=course_id)
        })

    except Exception as e:
        print(f"Error submitting course: {e}")
        mysql.rollback()
        return jsonify({'error': 'Error al enviar resultados'}), 500
    finally:
        cur.close()

@app.route('/course_result/<int:user_id>/<int:course_id>')
def course_result(user_id, course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        cur = mysql.cursor()
        # Obtener el resultado específico del curso para el usuario
        cur.execute("""
            SELECT course_results.score, courses.title 
            FROM course_results 
            JOIN courses ON course_results.course_id = courses.id 
            WHERE course_results.user_id = %s AND course_results.course_id = %s
            ORDER BY course_results.completed_at DESC
            LIMIT 1
        """, (user_id, course_id))
        
        result = cur.fetchone()
        if result:
            cr = {
                'score': result[0],
                'title': result[1],
            }
            return render_template('course_results.html', cr=cr)
        else:
            flash("No se encontraron resultados para este curso.")
            return redirect(url_for('courses_page'))

    except Exception as e:
        print(f"Error loading result: {e}")
        flash('Error al cargar el resultado')
        return redirect(url_for('courses_page'))
    finally:
        cur.close()