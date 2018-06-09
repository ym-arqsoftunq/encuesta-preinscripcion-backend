import random
import sys
from test_api_rest import get_usuarios, get_encuesta, get_materia, post_encuesta
import json

def simular_inscripcion(n=1):
	'''
	Realiza n inscripciones seleccionando en cada inscripcion un alumno al azar, entre 1 y 5 materias
	para pasar de cursables a aprobadas, cursaria o preinscripcion
	'''
	for i in range(n):
		# recupero usuarios
		usuarios = get_usuarios()
		# de los usuarios me quedo con los alumnos
		alumnos = filter(lambda u: u['roles'][0]['name'] == 'alumno', usuarios)

		# tomo un alumno al azar
		alumno = alumnos[random.randint(0,len(alumnos))]
		print 'username: ' + alumno['username']
		# recupero la encuesta. De no existir se crea una
		encuesta = get_encuesta(alumno['username'])	

		# muevo entre 1 y 5 materias de cursables a aprobadas, cursaria y preinscripcion al azar
		for ii in range(random.randint(1,5)):
			materia_seleccionada = encuesta['materias_cursables'].pop(random.randint(0,len(encuesta['materias_cursables'])-1))
			# elijo al azar si voy a marcar la materia como aprobada, cursaria o preinscripcion
			ubicacion = ['materias_aprobadas','materias_cursaria','materias_preinscripcion'][random.randint(0,2)]
			# para preinscripcion necesito especificar la comision
			if ubicacion == 'materias_preinscripcion':
				m = get_materia(materia_seleccionada['id'])
				# elijo la comision al azar
				c = m['comisiones'][random.randint(0,len(m['comisiones'])-1)]
				materia_seleccionada['comision_seleccionada'] = c

			encuesta[ubicacion].append(materia_seleccionada)

		response = post_encuesta(encuesta)
		print json.dumps(response, indent=4)


if __name__ == '__main__':
	# por parametro se puede pasar la cantidad de inscripciones que se desea simular
	# ej $ python simular_inscripcion.py 5
	if len(sys.argv) > 1:
		simular_inscripcion(int(sys.argv[1]))
	else:
		simular_inscripcion()