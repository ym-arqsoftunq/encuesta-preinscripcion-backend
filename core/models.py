from sqlalchemy import *
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

cursables = db.Table('cursables',
    db.Column('comision_id', db.Integer, db.ForeignKey('comisiones.id'), primary_key=True),
    db.Column('encuesta_id', db.Integer, db.ForeignKey('encuestas.id'), primary_key=True)
)

aprobadas = db.Table('aprobadas',
    db.Column('materia_id', db.Integer, ForeignKey('materias.id'), primary_key=True),
    db.Column('encuesta_id', db.Integer, ForeignKey('encuestas.id'), primary_key=True)
)

class Oferta(db.Model):
    __tablename__ = 'ofertas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=False)

    encuestas = relationship("Encuesta")

    def __init__(self, nombre):
        self.nombre = nombre



class Encuesta(db.Model):
    __tablename__ = 'encuestas'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'),
        nullable=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'),
        nullable=False)
    aprobadas = db.relationship('Materia', secondary=aprobadas, lazy='subquery',
        backref=db.backref('encuestas', lazy=True))
    cursables = db.relationship('Comision', secondary=cursables, lazy='subquery',
        backref=db.backref('encuestas', lazy=True))

    def __init__(self, oferta_id=None, alumno_id=None):
        self.oferta_id = oferta_id
        self.alumno_id = alumno_id

class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    encuestas = relationship("Encuesta")

    def __init__(self, nombre=None, username=None, email=None):
        self.nombre = nombre
        self.username = username
        self.email = email

    def __repr__(self):
        return "%d" % (self.nombre)

class Comision(db.Model):
    __tablename__ = 'comisiones'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))

    def __init__(self, descripcion=None):
        self.descripcion = descripcion

    def __repr__(self):
        return "Materia: %s comision: %s" % (self.materia, self.descripcion)

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=False)
    cuatrimestre = db.Column(db.Integer, nullable=False, unique=False)
    comisiones = relationship("Comision")

    def __init__(self, nombre=None, cuatrimestre=None):
        self.nombre = nombre
        self.cuatrimestre = cuatrimestre

    def __repr__(self):
        return "%d" % (self.nombre)
