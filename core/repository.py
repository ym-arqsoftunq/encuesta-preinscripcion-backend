import os
import json

class Repository(object):

    def get_oferta(self, oferta_id, username):
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "encuestas/oferta_%s.json" % (oferta_id))
        encuesta = json.load(open(json_url))
        encuesta['alumno'] = {'username': username}
        return encuesta

    def get_encuesta_alumno(self, oferta_id, alumno_id):
        encuesta = self.buscar_encuesta_alumno(oferta_id, alumno_id)
        return encuesta.get_json_data()

    def guardar_encuesta_alumno(self, encuesta):
        oferta_id = encuesta['oferta']['id']
        alumno_id = encuesta['alumno']['username']
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "encuestas/oferta_%s_alumno_%s.json" % (oferta_id, alumno_id))
        with open(json_url, 'w') as fp:
            json.dump(encuesta, fp)

    def buscar_encuesta_alumno(self, oferta_id, alumno_id):
        """
        * Buscar una encuesta del alumno y la oferta actual
            * Si existe, la piso
            * Sino, la creo
        """
        from models import Encuesta
        encuesta = Encuesta.query.filter(Encuesta.oferta_id==oferta_id and Encuesta.alumno_id==alumno_id).first()
        if not encuesta:
            encuesta = self.crear_encuesta(oferta_id, alumno_id)
        return encuesta

    def crear_encuesta(self, oferta_id, alumno_id):
        from models import Encuesta, db
        encuesta = Encuesta(oferta_id, alumno_id)
        db.session.add(encuesta)
        db.session.commit()
        return encuesta

    def guardar_materias_aprobadas(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias aprobadas y lo relaciono
        """

    def guardar_materias_cursables(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias cursables y lo relaciono
        """

    def guardar_materias_cursables(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias cursables y lo relaciono
        """

    def guardar_materias_cursables(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias cursables y lo relaciono
        """
