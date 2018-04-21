from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://ymcmweyxeguwhs:dd2a06f5714d5608fbff0781726067683e830e8bc9a8864c93ec6d865c7c5e8d@ec2-23-23-150-141.compute-1.amazonaws.com:5432/dd19u18l7o7psc'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://localhost/encuestas'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:postgres@localhost:5432/encuestas'
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
