import requests
import json

'''
FUNCIONES QUE LLAMAN A LOS DISTINTOS METODOS DE LA API REST
'''

# main api url
url_base = 'http://localhost:5000/'

# put your username/password here
auth = ('nestorgabriel2008', 'nestor')

def get_usuarios(username = None):
	params = None
	if username:
		params = {'username': username}
	response = requests.get(url_base + 'usuarios',
                        auth=auth, params=params, verify=False).json()
	# response contains the geoJSON object,
	# pretty print it to the console
	print json.dumps(response, indent=4)

def get_usuario(id):
	response = requests.get(url_base + 'usuarios/' + str(id),
                    auth=auth, verify=False).json()
	print json.dumps(response, indent=4)

def get_materias(nombre = None):
	params = None
	if nombre:
		params = {'nombre': nombre}
	response = requests.get(url_base + 'materias',
                        auth=auth, params=params, verify=False).json()
	print json.dumps(response, indent=4)

def get_materia(id):
	response = requests.get(url_base + 'materias/' + str(id),
                    auth=auth, verify=False).json()
	print json.dumps(response, indent=4)

def get_oferta(id):
	response = requests.get(url_base + 'oferta/' + str(id),
                    auth=auth, verify=False).json()
	print json.dumps(response, indent=4)

def get_encuesta(username):
	params = {'username': username}
	response = requests.get(url_base + 'encuesta',
                    auth=auth, params=params, verify=False).json()
	print json.dumps(response, indent=4)
	return json.dumps(response)

def get_resultados():
	response = requests.get(url_base + 'resultados',
                        auth=auth, verify=False).json()
	print json.dumps(response, indent=4)

def post_encuesta(username):
	encuesta = get_encuesta(username)

	response = requests.post(url_base + 'encuesta',
                    auth=auth, data=encuesta, verify=False,
                    headers = {'content-type': 'application/json'}).json()
	print json.dumps(response, indent=4)

if __name__ == '__main__':
    post_encuesta('nestorgabriel2008')