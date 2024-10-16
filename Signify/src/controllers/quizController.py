from flask import render_template, request
from app import db
import mysql.connector

# Configuración de la conexión a la base de datos para el cuestionario
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='cesar123',
        database='signify'  # Base de datos para los cuestionarios
    )
    return connection

def quiz_page():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM quizzes')
    quiz = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('quiz.html', quiz=quiz)

def submit():
    correct_answers = {}
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT id, correct_option FROM quizzes')
    questions = cursor.fetchall()

    for question in questions:
        question_id = f'question{question["id"]}'
        correct_answers[question_id] = question['correct_option']

    score = 0
    total_questions = len(questions)

    for i in range(total_questions):
        question_key = f'question{i + 1}'
        answer = request.form.get(question_key)
        if answer and int(answer) == correct_answers[question_key]:
            score += 1

    cursor.close()
    connection.close()

    return render_template('result.html', score=score, total=total_questions)
