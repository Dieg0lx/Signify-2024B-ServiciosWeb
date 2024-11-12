from flask_mysqldb import MySQL

class Course:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def get_all_courses(self):
        # Aquí usaríamos la conexión a la base de datos para obtener los cursos
        # En este caso, utilizaremos la variable courses como ejemplo
        courses = [
            {"id": 1, "title": "Lección 1", "questions": [
                {"id": 1, "question": "¿Cuál es la primera letra del alfabeto?", "options": ["A", "B", "C", "D"], "correct": "A"},
                {"id": 2, "question": "¿Qué letra sigue después de la A?", "options": ["B", "C", "D", "E"], "correct": "B"},
                {"id": 3, "question": "¿Cuál es la tercera letra del alfabeto?", "options": ["A", "B", "C", "D"], "correct": "C"},
            ]},
            {"id": 2, "title": "Lección 2", "questions": [
                {"id": 1, "question": "¿Qué letra viene después de la C?", "options": ["D", "E", "F", "G"], "correct": "D"},
                {"id": 2, "question": "¿Cuál es la quinta letra del alfabeto?", "options": ["D", "E", "F", "G"], "correct": "E"},
                {"id": 3, "question": "¿Qué letra sigue después de la E?", "options": ["D", "E", "F", "G"], "correct": "F"},
            ]},
        ]
        return courses
