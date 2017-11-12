from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

alumnos = [
    {
        'id': 1,
        'nombre': u'Juan Ignacio Yegro',
        'materias': [1, 3]
    },
    {
        'id': 2,
        'nombre': u'Nestor Munoz',
        'materias': [2, 3]
    }
]

materias = [
    {
        'id': 1,
        'nombre': u'Arquitectura de Software 1',
        'alumnos': [1]
    },
    {
        'id': 2,
        'nombre': u'Aspectos legales y sociales',
        'alumnos': [2]
    },
    {
        'id': 3,
        'nombre': u'Probabilidad y estadistica',
        'alumnos': [1, 2]
    },
]

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    return jsonify({'alumnos': alumnos})

@app.route('/materias', methods=['GET'])
def get_materias():
    return jsonify({'materias': materias})


@app.route('/oferta/<alumno_id>', methods=['GET'])
def get_encuesta(alumno_id):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "encuesta.json")
    return jsonify(json.load(open(json_url)))


@app.route('/preinscribir', methods=['POST'])
def post_preinscribir():
    return jsonify({
        'alumno': request.json['alumno'],
        'materias_aprobadas': request.json['materias_aprobadas'],
        'materias_preinscripcion': request.json['materias_preinscripcion']
        });


#LOGIN
@app.route('/login', methods=['POST'])
def post_login():
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
    userid = d['sub']
    #print 'USER ID ' + userid
    #TODO: con alguno de estos datos se deberia consultar la base para retornar la oferta del alumno
    #podria ser el email
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "encuesta.json")
    return jsonify(json.load(open(json_url)))





if __name__ == '__main__':
    app.run(debug=True)
