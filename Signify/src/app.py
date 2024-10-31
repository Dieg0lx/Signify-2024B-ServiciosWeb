from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signify.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    evaluations = db.relationship('Evaluation', backref='user', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    evaluations = db.relationship('Evaluation', backref='course', lazy=True)

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)
    completed = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        courses = Course.query.all()
        evaluations = {eval.course_id: eval.score for eval in current_user.evaluations}
        return render_template('index.html', courses=courses, evaluations=evaluations)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('usuario')
        password = request.form.get('contrasena')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('usuario')
        password = request.form.get('contrasena')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El nombre de usuario ya existe', 'error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/courses')
@login_required
def courses():
    courses = Course.query.all()
    evaluations = {eval.course_id: eval.score for eval in current_user.evaluations}
    return render_template('courses.html', courses=courses, evaluations=evaluations)

@app.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    evaluation = Evaluation.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not evaluation:
        evaluation = Evaluation(user_id=current_user.id, course_id=course_id, score=0)
        db.session.add(evaluation)
        db.session.commit()
    return render_template('course_detail.html', course=course, evaluation=evaluation)

@app.route('/quiz/<int:course_id>')
@login_required
def quiz(course_id):
    course = Course.query.get_or_404(course_id)
    # Aquí deberías cargar las preguntas del cuestionario para este curso
    questions = [
        {"id": 1, "question": "¿Cuál es el signo para 'Hola'?", "options": ["A", "B", "C", "D"]},
        {"id": 2, "question": "¿Qué significa el signo 'pulgar arriba'?", "options": ["Bien", "Mal", "Quizás", "No sé"]},
        # Agrega más preguntas aquí
    ]
    return render_template('quiz.html', course=course, questions=questions)

@app.route('/submit_quiz/<int:course_id>', methods=['POST'])
@login_required
def submit_quiz(course_id):
    evaluation = Evaluation.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not evaluation:
        evaluation = Evaluation(user_id=current_user.id, course_id=course_id)
        db.session.add(evaluation)
    
    # Aquí deberías procesar las respuestas y calcular la puntuación
    # Por ahora, simplemente estableceremos una puntuación aleatoria
    import random
    score = random.randint(0, 100)
    
    evaluation.score = score
    evaluation.completed = True
    db.session.commit()
    
    return redirect(url_for('course_detail', course_id=course_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Crear cursos si no existen
        if not Course.query.first():
            courses = [
                Course(name="Lenguaje de Señas Básico", description="Aprende el abecedario y conceptos básicos"),
                Course(name="Lenguaje de Señas Intermedio", description="Aprende comunicación intermedia con otras personas"),
                Course(name="Lenguaje de Señas Avanzado", description="Comunicación clara y confianza")
            ]
            db.session.add_all(courses)
            db.session.commit()
    app.run(debug=True)