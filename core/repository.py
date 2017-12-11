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
        from models import Encuesta, db, Usuario, Materia
        #Creo una encuesta para el alumno actual
        encuesta = Encuesta(oferta.id, alumno.id)
        #Recorro las materias de la oferta y las pongo en cursables
        for materia in oferta.materias:
            encuesta.cursables.append(materia)
        #Seteo las materias aprobadas de la ultima encuesta
        anterior = Encuesta.query.filter(Usuario.id == alumno.id).order_by(Encuesta.id.desc()).first()
        #Si hubo una encuesta anterior...
        if anterior:
            #Recorro las aprobadas y se la seteo a la encuesta actual
            for aprobada in anterior.aprobadas:
                #Busco la materia correspondiente a la oferta actual
                actual = Materia.query.filter_by(nombre=aprobada.nombre, oferta=oferta).first()
                if actual:
                    encuesta.aprobadas.append(actual)
        db.session.add(encuesta)
        db.session.commit()
        return encuesta

    def guardar_materias_aprobadas(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias aprobadas y lo relaciono
        """
        from models import Materia
        encuesta.aprobadas = []
        for data_materia in materias:
            materia = Materia.query.filter(Materia.id == data_materia['id']).first()
            encuesta.aprobadas.append(materia)

    def guardar_materias_imposibilitadas(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias imposibilitadas y lo relaciono
        """
        from models import Materia
        encuesta.imposibilitadas = []
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
        encuesta.preinscripcion = []
        for data_materia in materias:
            comision = Comision.query.filter(Comision.id == data_materia['comision_seleccionada']['id']).first()
            encuesta.preinscripcion.append(comision)


    def get_resultados(self):
        from models import Oferta
        #En un principio se penso para ver resultados de muchas ofertas, pero se va a hacer solo para la activar
        oferta = Oferta.query.filter(Oferta.activa == True).first()
        resultados = oferta.get_resultados()
        return resultados
