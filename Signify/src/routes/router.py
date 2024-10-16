from app import app
from controllers.userController import first, login, second
from controllers.quizController import quiz_page, submit

@app.route('/', methods=['GET'])
def index():
    return first()

@app.route('/login', methods=['POST'])
def verification():
    return login()

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return second()

# Rutas del cuestionario
@app.route('/quiz', methods=['GET'])
def quiz():
    return quiz_page()

@app.route('/submit', methods=['POST'])
def submit_quiz():
    return submit()
