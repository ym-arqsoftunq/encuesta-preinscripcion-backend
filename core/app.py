from flask import Flask, jsonify
from flask_cors import CORS

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


if __name__ == '__main__':
    app.run(debug=True)
