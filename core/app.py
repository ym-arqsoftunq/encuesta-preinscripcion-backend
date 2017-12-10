from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests
from repository import Repository
from flask_cli import FlaskCLI
from flask_alembic import Alembic
from flask_migrate import Migrate
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_user import roles_required, SQLAlchemyAdapter, UserManager
from flask_login import login_user, LoginManager, login_required, logout_user


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
 app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://ymcmweyxeguwhs:dd2a06f5714d5608fbff0781726067683e830e8bc9a8864c93ec6d865c7c5e8d@ec2-23-23-150-141.compute-1.amazonaws.com:5432/dd19u18l7o7psc'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://localhost/encuestas'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:postgres@localhost:5432/encuestas'
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = SQLAlchemy(app)
db.init_app(app)


db_adapter = SQLAlchemyAdapter(db,  'models.Usuario')
user_manager = UserManager(db_adapter, app)

login_manager = LoginManager()
login_manager.init_app(app)

FlaskCLI(app)
@app.shell_context_processor
def ctx():
    return {'a':'b'}

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    return jsonify({'alumnos': alumnos})

@app.route('/materias', methods=['GET'])
def get_materias():
    return jsonify({'materias': materias})

@app.route('/oferta/<username>', methods=['GET'])
#@login_required
#@roles_required('alumno')
def get_encuesta(username):
    try:
        repo = Repository()
        return repo.get_encuesta_activa(username)
    except Exception as e:
        return jsonify({'error': str(e)}),501

@app.route('/resultados/<oferta_id>', methods=['GET'])
#@login_required
#@roles_required('director')
def get_resultados(oferta_id):
    repo = Repository()
    return json.dumps(repo.get_resultados(oferta_id))

@app.route('/preinscribir', methods=['POST'])
#@login_required
#@roles_required('alumno')
def post_preinscribir():
    repo = Repository()
    repo.guardar_encuesta_alumno(request.json)
    return 'OK'

@login_manager.user_loader
def load_user(user_id):
    from models import Usuario
    return Usuario.query.get(user_id)

#LOGIN
@app.route('/login', methods=['POST'])
def post_login():
    from models import Usuario
    email = request.json['email']
    password = request.json['password']
    repo = Repository()
    usuario = Usuario.query.filter_by(email=email).first()
    #Esto hay que sacarlo
    if usuario and usuario.password == password and login_user(usuario):
        success = True
        rol = usuario.roles[0].name
    else:
        success = False
        rol = ''
    return json.dumps({'success':success, 'rol': rol }), 200, {'ContentType':'application/json'}

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    success = logout_user()
    return json.dumps({'success':success}), 200, {'ContentType':'application/json'}


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
    username = d['email'].split('@')[0]
    repo = Repository()
    return repo.get_encuesta_alumno(1, username)

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
        username = request.json['email'].split('@')[0]
        repo = Repository()
        return jsonify(repo.get_encuesta_alumno(1, username))
    else:
        raise Exception('No se pudo validar el token')

if __name__ == '__main__':
    app.run(debug=True)
