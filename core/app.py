from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os
import json
import requests
from flask_cli import FlaskCLI
from flask_sqlalchemy import SQLAlchemy

from repository import Repository
from models import Materia, Usuario

from config import app

from flask_httpauth import HTTPBasicAuth
from flask_restful import reqparse, Api, Resource
from flask_restful_swagger import swagger

from log import set_log


DEBUG = False

###################################
# wrapeo la app para swagger
api = swagger.docs(Api(app), apiVersion='0.1',
                   basePath='http://localhost:5000',
                   resourcePath='/',
                   produces=["application/json", "text/html"],
                   api_spec_url='/api/spec',
                   description='API de encuesta de preinscripcion')
###################################

cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)
db.init_app(app)


FlaskCLI(app)
@app.shell_context_processor
def ctx():
    return {'a':'b'}

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


################################################
### LOGIN ###
################################################

@app.route('/login', methods=['POST'])
def post_login():
    email = request.json['email']
    password = request.json['password']
    repo = Repository()
    usuario = Usuario.query.filter_by(email=email).first()
    #Esto hay que sacarlo
    if usuario and usuario.password == password:
        success = True
        rol = usuario.roles[0].name
    else:
        success = False
        rol = ''
    return json.dumps({'success':success, 'rol': rol }), 200, {'ContentType':'application/json'}



#LOGIN GOOGLE
@app.route('/google-login', methods=['POST'])
def post_google_login():
    #valido el token con un servicio de google
    j = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+request.json['token']).content
    """
    me devuelve un string con estos campos
    {
     // These six fields are included in all Google ID Tokens.
     "iss": "https://accounts.google.com",
     "sub": "110169484474386276334",
     "azp": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
     "aud": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
     "iat": "1433978353",
     "exp": "1433981953",

     // These seven fields are only included when the user has granted the "profile" and
     // "email" OAuth scopes to the application.
     "email": "testuser@gmail.com",
     "email_verified": "true",
     "name" : "Test User",
     "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
     "given_name": "Test",
     "family_name": "User",
     "locale": "en"
    }
    """
    d = json.loads(j)
    email = d['email']
    repo = Repository()
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        success = True
        rol = usuario.roles[0].name
    else:
        success = False
        rol = ''
    return json.dumps({'success':success, 'rol': rol }), 200, {'ContentType':'application/json'}


#LOGIN FACEBOOK
@app.route('/facebook-login', methods=['POST'])
def post_facebook_login():
    #valido el token con un servicio de facebook
    j = requests.get('https://graph.facebook.com/me?access_token='+request.json['token']).content
    """
    me devuelve un string con estos campos
    {
       "name": "Nestor Gabriel Munoz",
       "id": "10215016199027875"
    }
    """
    d = json.loads(j)
    #chequeo que no haya devuelto error
    if "name" in d and "id" in d:
        #el email me llega en el request
        email = request.json['email']
        repo = Repository()
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            success = True
            rol = usuario.roles[0].name
        else:
            success = False
            rol = ''
        return json.dumps({'success':success, 'rol': rol }), 200, {'ContentType':'application/json'}
    else:
        raise Exception('No se pudo validar el token')


################################################
### API REST ###
################################################

# HTTP AUTHENTICATION
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

auth = HTTPBasicAuth()
parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('nombre', type=str)

@auth.get_password
def get_password(username):
    # la password retornada debe coincidir con la que me llega en el request
    usuario = Usuario.query.filter_by(username=username).first()
    if usuario:
        return usuario.password
    else:
        return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

class UsuarioResource(Resource):
  "API DE USUARIOS"

  @swagger.operation(
    notes='Retorna un usuario registrado',
    nickname='get',
    parameters=[
      {
        "name": "id",
        "description": "ID del usuario",
        "required": True,
        "allowMultiple": False,
        "dataType": 'integer',
        "paramType": "path"
      }
    ])
  @auth.login_required
  def get(self,id):
    usuario = Usuario.query.filter_by(id=id).first()
    if usuario is None:
        return None
    else:
        return {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'username': usuario.username,
            'email': usuario.email,
            'roles': map(lambda r: r.name, usuario.roles)
        }, 200, {'Access-Control-Allow-Origin': '*'}

class UsuariosResource(Resource):

  @swagger.operation(
    notes='Retorna todos los usuarios registrados',
    parameters=[
      {
        "name": "username",
        "description": "Username",
        "required": False,
        "allowMultiple": False,
        "dataType": 'string',
        "paramType": 'query'
      }
    ])
  @auth.login_required
  def get(self):
    repo = Repository()
    argumentos = parser.parse_args()
    #Si viene 'username' y trae algun dato
    if 'username' in argumentos and argumentos['username']:
        return repo.get_usuario_por_username(argumentos['username']), 200, {'Access-Control-Allow-Origin': '*'}
    else:
        return repo.get_usuarios(), 200, {'Access-Control-Allow-Origin': '*'}


class MateriaResource(Resource):
  "API DE MATERIAS"

  @swagger.operation(
    notes='Retorna los datos de una materia',
    nickname='get',
    parameters=[
      {
        "name": "id",
        "description": "ID de la materia",
        "required": True,
        "allowMultiple": False,
        "dataType": 'string',
        "paramType": "path"
      }
    ])
  @auth.login_required
  def get(self,id):
    materia = Materia.query.filter_by(id=id).first()
    if materia is None:
        return None
    else:
        return {
            'id': materia.id,
            'nombre': materia.nombre,
            'cuatrimestre': materia.cuatrimestre,
            'oferta_id': materia.oferta_id,
        }, 200, {'Access-Control-Allow-Origin': '*'}

class MateriasResource(Resource):

  @swagger.operation(
    notes='Busca materias por nombre, si no se ingresa nombre retorna todas',
    parameters=[
      {
        "name": "nombre",
        "description": "Nombre",
        "required": False,
        "allowMultiple": False,
        "dataType": 'string',
        "paramType": 'query'
      }
    ])
  @auth.login_required
  def get(self):
    repo = Repository()
    args = parser.parse_args()
    #return args
    if 'nombre' in args and args['nombre']:
        return repo.get_materia_por_nombre(args['nombre']), 200, {'Access-Control-Allow-Origin': '*'}
    else:
        return repo.get_materias(), 200, {'Access-Control-Allow-Origin': '*'}


class OfertaResource(Resource):
  "API DE OFERTAS"

  @swagger.operation(
    notes='Retorna los datos de una oferta',
    nickname='get',
    parameters=[
      {
        "name": "id",
        "description": "ID de la oferta",
        "required": True,
        "allowMultiple": False,
        "dataType": 'string',
        "paramType": "path"
      }
    ])

  @auth.login_required
  def get(self,id):
    repo = Repository()
    oferta = repo.get_oferta(id)
    if oferta is None:
        return None
    else:
        return oferta, 200, {'Access-Control-Allow-Origin': '*'}

@swagger.model
class EncuestaModel:
  """Template que se muestra en la consola swagger para el POST de encuentas.
  Los parametros del __init__ son los campos del json q se envia en el body"""
  def __init__(self, alumno, materias_aprobadas, materias_preinscripcion,
    materias_cursaria, materias_cursables, oferta):
    pass

class EncuestasResource(Resource):
  "API DE ENCUESTAS"

  @swagger.operation(
    notes='Retorna la encuesta activa del usuario ingresado. Si no existe se crea',
    nickname='get',
    parameters=[
      {
        "name": "username",
        "description": "Usuario",
        "required": True,
        "allowMultiple": False,
        "dataType": 'string',
        "paramType": "query"
      }
    ])

  @auth.login_required
  def get(self):
    repo = Repository()
    try:
      return repo.get_encuesta_activa(parser.parse_args()['username']), 200, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        return {'error': str(e)},501

  @swagger.operation(
    notes='Crea o actualiza una encuesta',
    responseClass=EncuestaModel.__name__,
    nickname='post',
    parameters=[
      {
        "name": "Encuesta",
        "description": "Datos de la encuesta completada",
        "required": True,
        "allowMultiple": False,
        "dataType": EncuestaModel.__name__,
        "paramType": "body"
      }
    ])
  @auth.login_required
  def post(self):
    repo = Repository()
    repo.guardar_encuesta_alumno(request.json)
    return 'OK'


class ResultadosResource(Resource):

  @swagger.operation(
    notes='Retorna los resultados de la encuesta actual'
    )
  @auth.login_required
  def get(self):
    repo = Repository()
    return repo.get_resultados()


api.add_resource(UsuariosResource, '/usuarios')
api.add_resource(UsuarioResource, '/usuarios/<int:id>')
api.add_resource(MateriasResource, '/materias')
api.add_resource(MateriaResource, '/materias/<int:id>')
api.add_resource(OfertaResource, '/oferta/<int:id>')
api.add_resource(EncuestasResource, '/encuesta')
api.add_resource(ResultadosResource, '/resultados')

if __name__ == '__main__':
    if not DEBUG:
        set_log(app)
    app.run(host='0.0.0.0', debug=DEBUG)
