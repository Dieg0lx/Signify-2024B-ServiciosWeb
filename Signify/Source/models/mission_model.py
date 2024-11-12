from flask_mysqldb import MySQL

class Mission:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def get_all_missions(self):
        missions = [
            {"id": 1, "title": "Completa 3 lecciones", "goal": 3, "progress": 0},
            {"id": 2, "title": "Obtén 100 puntos", "goal": 100, "progress": 0},
            {"id": 3, "title": "Practica 5 días seguidos", "goal": 5, "progress": 0},
        ]
        return missions

    def update_mission_progress(self, mission_id, progress):
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE missions SET progress = %s WHERE id = %s", (progress, mission_id))
        self.mysql.connection.commit()
        cur.close()
