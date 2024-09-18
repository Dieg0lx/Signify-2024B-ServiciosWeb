from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', active_section='mi-perfil')

@app.route('/mi-perfil')
def mi_perfil():
    return render_template('index.html', active_section='mi-perfil')

@app.route('/evaluaciones')
def evaluaciones():
    return render_template('index.html', active_section='evaluaciones')

@app.route('/cursos')
def cursos():
    return render_template('index.html', active_section='cursos')

if __name__ == '__main__':
    app.run(debug=True)
