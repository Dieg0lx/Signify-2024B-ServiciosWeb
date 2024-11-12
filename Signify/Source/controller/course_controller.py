# course_controller.py
from flask import render_template, request, redirect, url_for, session, flash
from app import mysql
from datetime import datetime
from app import app

def calculate_level(points):
    return points // 100 + 1

def calculate_level_progress(points):
    return (points % 100)

@app.route('/courses')
def courses_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.cursor()
    courses = []  # Asegúrate de inicializar la lista
    current_course = None

    try:
        # Obtener cursos con sus preguntas y opciones
        cur.execute("""SELECT * FROM courses;""") 
        
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

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def start_course(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.cursor()
    try:
        # Primero verificar si el curso existe
        cur.execute("SELECT id, title FROM courses WHERE id = %s", (course_id,))
        course_data = cur.fetchone()
        
        if not course_data:
            flash('Curso no encontrado')
            return redirect(url_for('courses_page'))
            
        # Obtener preguntas del curso
        cur.execute("""
            SELECT q.id, q.question_text, q.correct_answer 
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
            
            course['questions'].append({
                'id': question[0],
                'question': question[1],
                'options': options,
                'correct': question[2]
            })
            
        return render_template('course.html', course=course)
        
    except Exception as e:
        print(f"Error loading course: {e}")
        flash('Error al cargar el curso')
        return redirect(url_for('courses_page'))
    finally:
        cur.close()

    return render_template('course.html', course=course)

@app.route('/course_result/<int:user_id>')
def course_result(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        cur = mysql.cursor()
        cur.execute("""SELECT course_results.score, courses.title FROM course_results JOIN courses ON course_results.course_id = courses.id WHERE course_results.user_id = %s""", (user_id)) 
            
        result = cur.fetchone()

        cr = {
            'score': result[0],
            'title': result[1],
        }

        return render_template('course_results.html', cr=cr)

    except Exception as e:
        print(f"Error loading result: {e}")
        flash('Error al cargar el resultado')
        return redirect(url_for('courses_page'))
    finally:
        cur.close()

@app.route('/submit_course/<int:course_id>', methods=['POST'])
def submit_course(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    cur = mysql.cursor()
    try:
        # Obtener respuestas del usuario
        answers = request.form.to_dict()
        correct_answers = 0
        total_questions = 0
        
        # Verificar respuestas
        for question_id, answer in answers.items():
            total_questions += 1
            q_id = int(question_id)
            cur.execute("SELECT correct_answer FROM questions WHERE id = %s", (q_id,))
            correct = cur.fetchone()[0]
            if answer == correct:
                correct_answers += 1
        
        # Calcular puntuación
        score = int((correct_answers / total_questions) * 100)
        
        # Guardar resultado
        cur.execute("""
            INSERT INTO course_results 
            (user_id, course_id, score) 
            VALUES (%s, %s, %s)
        """, (session['user_id'], course_id, score))
        
        # Actualizar progreso del usuario
        cur.execute("""
            UPDATE users 
            SET completed_courses = completed_courses + 1,
                total_points = total_points + %s 
            WHERE id = %s
        """, (score, session['user_id']))
        
        # Actualizar misiones
        cur.execute("""
            UPDATE missions 
            SET progress = progress + 1 
            WHERE title = 'Completa 3 lecciones'
        """)
        
        mysql.commit()
        flash(f'¡Curso completado! Puntuación: {score}%')
        print(session['user_id'])
        return redirect(url_for('course_result', user_id=(session['user_id'])))

    except Exception as e:
        print(f"Error submitting course: {e}")
        mysql.rollback()
        flash('Error al enviar resultados')
    finally:
        cur.close()
    
    return redirect(url_for('courses_page'))