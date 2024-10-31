from flask import Flask, request, jsonify
from Signify.src.app import db

# Definir el modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    contrasena = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'