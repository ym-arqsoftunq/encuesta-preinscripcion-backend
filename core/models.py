from sqlalchemy import *
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from app import app
import json

db = SQLAlchemy(app)

preinscripcion = db.Table('preinscripcion',
    db.Column('comision_id', db.Integer, db.ForeignKey('comisiones.id'), primary_key=True),
    db.Column('encuesta_id', db.Integer, db.ForeignKey('encuestas.id'), primary_key=True)
)

aprobadas = db.Table('aprobadas',
    db.Column('materia_id', db.Integer, ForeignKey('materias.id'), primary_key=True),
    db.Column('encuesta_id', db.Integer, ForeignKey('encuestas.id'), primary_key=True)
)

cursables = db.Table('cursables',
    db.Column('materia_id', db.Integer, ForeignKey('materias.id'), primary_key=True),
    db.Column('encuesta_id', db.Integer, ForeignKey('encuestas.id'), primary_key=True)
)

class Oferta(db.Model):
    __tablename__ = 'ofertas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def asignar_datos(self, data):
        data['oferta'] = {}
        data['oferta']['id'] = self.id
        data['oferta']['nombre'] = self.nombre

class Encuesta(db.Model):
    __tablename__ = 'encuestas'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'),
        nullable=False)

    alumno = db.relationship('Alumno',
        backref=db.backref('encuestas', lazy=True))
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'),
        nullable=False)
    oferta = db.relationship('Oferta',
            backref=db.backref('encuestas', lazy=True))
    aprobadas = db.relationship('Materia', secondary=aprobadas, lazy='subquery',
        backref=db.backref('encuestas', lazy=True))
    cursables = db.relationship('Materia', secondary=cursables, lazy='subquery',
        backref=db.backref('encuestasc', lazy=True))
    preinscripcion = db.relationship('Comision', secondary=preinscripcion, lazy='subquery',
        backref=db.backref('encuestas', lazy=True))

    def __init__(self, oferta_id=None, alumno_id=None):
        self.oferta_id = oferta_id
        self.alumno_id = alumno_id

    def get_json_data(self):
        data = {'alumno': {},'materias_aprobadas':[],
                'materias_cursables':[],
                'materias_preinscripcion':[],
                'oferta':{}
                }
        self.asignar_cursables(data)
        self.asignar_aprobadas(data)
        self.asignar_preinscripcion(data)
        self.oferta.asignar_datos(data)
        self.alumno.asignar_datos(data)
        return json.dumps(data)

    def asignar_cursables(self, data):
        for cursable in self.cursables:
            data['materias_cursables'].append(cursable.get_json_data())

    def asignar_aprobadas(self, data):
        for aprobada in self.aprobadas:
            data['materias_aprobadas'].append(aprobada.get_json_data())

    def asignar_preinscripcion(self, data):
        for comision in self.preinscripcion:
            json_comision = comision.materia.get_json_data()
            json_comision['comision_seleccionada'] = comision.get_json_data()
            data['materias_preinscripcion'].append(json_comision)


class Alumno(db.Model):
    __tablename__ = 'alumnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre=None, username=None, email=None):
        self.nombre = nombre
        self.username = username
        self.email = email

    def __repr__(self):
        return "%d" % (self.nombre)

    def asignar_datos(self, data):
        data['alumno'] = {}
        data['alumno']['id'] = self.id
        data['alumno']['nombre'] = self.nombre
        data['alumno']['username'] = self.username

class Comision(db.Model):
    __tablename__ = 'comisiones'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))
    materia = db.relationship('Materia',
        backref=db.backref('comisiones', lazy=True))

    def __init__(self, descripcion=None):
        self.descripcion = descripcion

    def __repr__(self):
        return "Materia: %s comision: %s" % (self.materia, self.descripcion)

    def get_json_data(self):
        data = {}
        data['descripcion'] = self.descripcion
        data['id'] = self.id
        return data

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=False)
    cuatrimestre = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, nombre=None, cuatrimestre=None):
        self.nombre = nombre
        self.cuatrimestre = cuatrimestre

    def get_json_data(self):
        data = {'comisiones':[]}
        data['cuatrimestre'] = self.cuatrimestre
        data['id'] = self.id
        data['nombre'] = self.nombre
        for comision in self.comisiones:
            data['comisiones'].append(comision.get_json_data())
        return data

    def __repr__(self):
        return "%d" % (self.nombre)
