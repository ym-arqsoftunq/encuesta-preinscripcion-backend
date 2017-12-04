from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests
from repository import Repository

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    return jsonify({'alumnos': alumnos})

@app.route('/materias', methods=['GET'])
def get_materias():
    return jsonify({'materias': materias})

@app.route('/oferta/<oferta_id>/<alumno_id>', methods=['GET'])
def get_encuesta(oferta_id, alumno_id):
    repo = Repository()
    return jsonify(repo.get_encuesta_alumno(oferta_id, alumno_id))

@app.route('/resultados/<oferta_id>', methods=['GET'])
def get_resultados(oferta_id):
    repo = Repository()
    return jsonify(repo.get_resultados(oferta_id))

@app.route('/preinscribir', methods=['POST'])
def post_preinscribir():
    repo = Repository()
    repo.guardar_encuesta_alumno(request.json)
    return 'OK'

#LOGIN
@app.route('/login', methods=['POST'])
def post_login():
    #TODO: validar email y password
    email = request.json['email']
    password = request.json['password']
    username = email.split('@')[0]
    repo = Repository()
    return jsonify(repo.get_encuesta_alumno(1, username))

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
    return jsonify(repo.get_encuesta_alumno(1, username))

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
