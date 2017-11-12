from flask import Flask, jsonify, request
from flask_cors import CORS
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

@app.route('/inscribir', methods=['POST'])
def post_inscribir():
    return jsonify({'alumno': request.json['alumno'], 'materias': request.json['materias']})

if __name__ == '__main__':
    app.run(debug=True)
