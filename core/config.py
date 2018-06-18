from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# POSTGRES EN HEROKU
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://ymcmweyxeguwhs:dd2a06f5714d5608fbff0781726067683e830e8bc9a8864c93ec6d865c7c5e8d@ec2-23-23-150-141.compute-1.amazonaws.com:5432/dd19u18l7o7psc'
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# POSTGRES LOCAL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://localhost/encuestas'

# POSTGRES EN DOCKER poner IP de la maquina luego de @, no localhost
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:postgres@192.168.1.34:5432/encuestas'


# POSTGRES EN DOCKER poner IP de la maquina luego de @, no localhost
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:postgres@db:5432/encuestas'

app.config['ADMINS'] = ['nachoyegro@gmail.com', 'nestorgabriel2008@gmail.com']

app.config['EMAIL_HOST'] = 'smtp.mailtrap.io'
app.config['EMAIL_HOST_USER'] = '2d222580e64237'
app.config['EMAIL_HOST_PASSWORD'] = 'c812b45ad4d1a3'
app.config['EMAIL_PORT'] = 2525
app.config['EMAIL_SUBJECT'] = '[encuesta-preinscripcion-backend] Application Error'
