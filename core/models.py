from sqlalchemy import *
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from app import app
import json
from flask_user import UserMixin

db = SQLAlchemy(app)

preinscripcion = db.Table('preinscripcion',
    db.Column('comision_id', db.Integer, db.ForeignKey('comisiones.id'), primary_key=True),
    db.Column('encuesta_id', db.Integer, db.ForeignKey('encuestas.id'), primary_key=True)
)

aprobadas = db.Table('aprobadas',
    db.Column('materia_id', db.Integer, ForeignKey('materias.id'), primary_key=True),
    db.Column('encuesta_id', db.Integer, ForeignKey('encuestas.id'), primary_key=True)
)

imposibilitadas = db.Table('imposibilitadas',
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
    activa = db.Column(db.Boolean, default=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def activar_oferta(self):
        self.activa = True


    def asignar_datos(self, data):
        data['oferta'] = {}
        data['oferta']['id'] = self.id
        data['oferta']['nombre'] = self.nombre

    def get_resultados(self):
        resultados = {'materias': [], 'oferta': {}, 'encuestas': {}}
        self.asignar_datos(resultados)
        self.asignar_datos_encuestas(resultados)
        self.asignar_datos_materias(resultados)
        return resultados

    def asignar_datos_encuestas(self, resultados):
        resultados['encuestas']['respondidas'] = len(list(filter(lambda encuesta: encuesta.respondida, self.encuestas)))
        resultados['encuestas']['total'] = len(self.encuestas)

    def asignar_datos_materias(self, resultados):
        for materia in self.materias:
            resultados['materias'].append(materia.get_resultados())

class Encuesta(db.Model):
    __tablename__ = 'encuestas'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'),
        nullable=False)

    alumno = db.relationship('Usuario',
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
    imposibilitadas = db.relationship('Materia', secondary=imposibilitadas, lazy='subquery',
        backref=db.backref('encuestasi', lazy=True))
    respondida = db.Column(db.Boolean, default=False)
    modificable = db.Column(db.Boolean, default=True)


    def __init__(self, oferta_id=None, alumno_id=None):
        self.oferta_id = oferta_id
        self.alumno_id = alumno_id

    def get_json_data(self):
        data = {'alumno': {},'materias_aprobadas':[],
                'materias_cursables':[],
                'materias_preinscripcion':[],
                'materias_cursaria':[],
                'oferta':{}
                }
        self.asignar_cursables(data)
        self.asignar_aprobadas(data)
        self.asignar_preinscripcion(data)
        self.asignar_imposibilitadas(data)
        self.oferta.asignar_datos(data)
        self.alumno.asignar_datos(data)
        return json.dumps(data)

    def asignar_cursables(self, data):
        for cursable in self.cursables:
            data['materias_cursables'].append(cursable.get_json_data())

    def asignar_aprobadas(self, data):
        for aprobada in self.aprobadas:
            data['materias_aprobadas'].append(aprobada.get_json_data())

    def asignar_imposibilitadas(self, data):
        for materia in self.imposibilitadas:
            data['materias_cursaria'].append(materia.get_json_data())

    def asignar_preinscripcion(self, data):
        for comision in self.preinscripcion:
            json_comision = comision.materia.get_json_data()
            json_comision['comision_seleccionada'] = comision.get_json_data()
            data['materias_preinscripcion'].append(json_comision)


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False, default='')
    roles = db.relationship('Rol', secondary='rolesusuarios',
            backref=db.backref('usuarios', lazy='dynamic'))

    def __init__(self, nombre=None, username=None, email=None, password=None):
        self.nombre = nombre
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "%s" % (self.nombre)

    def get_id(self):
        return self.id

    def asignar_datos(self, data):
        data['alumno'] = {}
        data['alumno']['id'] = self.id
        data['alumno']['nombre'] = self.nombre
        data['alumno']['username'] = self.username

class Comision(db.Model):
    __tablename__ = 'comisiones'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    cupo = db.Column(db.Integer)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))
    materia = db.relationship('Materia',
        backref=db.backref('comisiones', lazy=True))

    def __init__(self, descripcion=None, cupo=0):
        self.descripcion = descripcion
        self.cupo = cupo

    def __repr__(self):
        return "Materia: %s comision: %s" % (self.materia, self.descripcion)

    def problema_de_cupo(self):
        #Si el cupo supera el 90%, entonces hay problema de cupo
        anotados = len(self.encuestas)
        return (anotados * 100 / self.cupo) >= 90

    def get_json_data(self):
        data = {}
        self.asignar_datos_basicos(data)
        return data

    def asignar_datos_basicos(self, data):
        data['descripcion'] = self.descripcion
        data['id'] = self.id
        data['cupo'] = self.cupo

    def get_resultados(self):
        resultados = {}
        self.asignar_datos_basicos(resultados)
        resultados['inscriptos'] = len(self.encuestas)
        return resultados

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=False)
    cuatrimestre = db.Column(db.Integer, nullable=False, unique=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'),
        nullable=False)
    oferta = db.relationship('Oferta',
            backref=db.backref('materias', lazy=True))

    def __init__(self, nombre=None, cuatrimestre=None):
        self.nombre = nombre
        self.cuatrimestre = cuatrimestre

    def get_json_data(self):
        data = {'comisiones':[]}
        self.asignar_datos_basicos(data)
        for comision in self.comisiones:
            data['comisiones'].append(comision.get_json_data())
        return data

    def asignar_datos_basicos(self, data):
        data['cuatrimestre'] = self.cuatrimestre
        data['id'] = self.id
        data['nombre'] = self.nombre

    def get_resultados(self):
        resultado = {'resultados': [], 'aprobados': len(self.encuestas), 'cursarian': len(self.encuestasi),
        'problema_de_cupo': False}
        self.asignar_datos_basicos(resultado)
        for comision in self.comisiones:
            resultado['problema_de_cupo'] = comision.problema_de_cupo() or resultado['problema_de_cupo']
            resultado['resultados'].append(comision.get_resultados())
        return resultado


    def __repr__(self):
        return "%s" % (self.nombre)

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name=None):
        self.name = name

# Define UserRoles model
class RolesUsuario(db.Model):
    __tablename__ = 'rolesusuarios'
    id = db.Column(db.Integer(), primary_key=True)
    usuario_id = db.Column(db.Integer(), db.ForeignKey('usuarios.id', ondelete='CASCADE'))
    rol_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
