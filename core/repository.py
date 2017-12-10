import os

class Repository(object):

    def get_encuesta_activa(self, username):
        encuesta = self.buscar_encuesta_alumno(username)
        return encuesta.get_json_data()

    def guardar_encuesta_alumno(self, data):
        from models import db
        oferta_id = data['oferta']['id']
        username = data['alumno']['username']
        encuesta = self.buscar_encuesta_alumno(username)
        self.guardar_materias_aprobadas(encuesta, data['materias_aprobadas'])
        self.guardar_materias_cursables(encuesta, data['materias_cursables'])
        self.guardar_materias_preinscripcion(encuesta, data['materias_preinscripcion'])
        self.guardar_materias_imposibilitadas(encuesta, data['materias_cursaria'])
        encuesta.respondida = True
        db.session.commit()

    def buscar_encuesta_alumno(self, username):
        """
        * Buscar una encuesta del alumno y la oferta actual
            * Si existe, la traigo
            * Sino, la creo
        """
        from models import Encuesta, Usuario, Oferta
        #TODO: Catchear una posible excepcion
        alumno = Usuario.query.filter_by(username=username).first()
        oferta_activa = Oferta.query.filter_by(activa=True).first()
        encuesta = Encuesta.query.filter_by(oferta_id=oferta_activa.id, alumno_id=alumno.id).first()
        if not encuesta:
            encuesta = self.crear_encuesta(oferta_activa, alumno)
        return encuesta

    def crear_encuesta(self, oferta, alumno):
        from models import Encuesta, db
        #Creo una encuesta para el alumno actual
        encuesta = Encuesta(oferta.id, alumno.id)
        #Recorro las materias de la oferta y las pongo en cursables
        for materia in oferta.materias:
            encuesta.cursables.append(materia)
        db.session.add(encuesta)
        db.session.commit()
        return encuesta

    def guardar_materias_aprobadas(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias aprobadas y lo relaciono
        """
        from models import Materia
        for data_materia in materias:
            materia = Materia.query.filter(Materia.id == data_materia['id']).first()
            encuesta.aprobadas.append(materia)

    def guardar_materias_imposibilitadas(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias imposibilitadas y lo relaciono
        """
        from models import Materia
        for data_materia in materias:
            materia = Materia.query.filter(Materia.id == data_materia['id']).first()
            encuesta.imposibilitadas.append(materia)

    def guardar_materias_cursables(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias cursables y lo relaciono
        """
        from models import Materia
        encuesta.cursables = []
        for data_materia in materias:
            materia = Materia.query.filter(Materia.id == data_materia['id']).first()
            encuesta.cursables.append(materia)

    def guardar_materias_preinscripcion(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias preinscripcion y lo relaciono
        """
        from models import Comision
        for data_materia in materias:
            comision = Comision.query.filter(Comision.id == data_materia['comision_seleccionada']['id']).first()
            encuesta.preinscripcion.append(comision)


    def get_resultados(self, oferta_id):
        from models import Oferta
        oferta = Oferta.query.filter(Oferta.id == oferta_id).first()
        return oferta.get_resultados()
