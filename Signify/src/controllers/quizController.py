from flask import render_template, request, redirect, url_for
from Signify.src.app import app, db
from flask_login import current_user, login_required

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(100), nullable=False)
    option2 = db.Column(db.String(100), nullable=False)
    option3 = db.Column(db.String(100), nullable=False)
    option4 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

class UserQuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)

@app.route('/quiz')
@login_required
def quiz():
    questions = Quiz.query.all()
    return render_template('quiz.html', quiz=questions)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    correct_answers = {}
    questions = Quiz.query.all()
    
    for question in questions:
        correct_answers[f'question{question.id}'] = question.correct_option
    
    score = 0
    total_questions = len(questions)
    
    for i in range(total_questions):
        question_key = f'question{i + 1}'
        answer = request.form.get(question_key)
        if answer and int(answer) == correct_answers[question_key]:
            score += 1
    
    # Guardar el resultado del usuario
    result = UserQuizResult(user_id=current_user.id, score=score, total_questions=total_questions)
    db.session.add(result)
    db.session.commit()
    
    return render_template('result.html', score=score, total=total_questions)