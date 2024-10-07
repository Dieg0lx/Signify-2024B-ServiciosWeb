from app import app
from controllers.userController import first, login, second

@app.route('/', methods=['GET'])
def index():
    return first()

@app.route('/login', methods=['POST'])
def verification():
    return login()

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return second()