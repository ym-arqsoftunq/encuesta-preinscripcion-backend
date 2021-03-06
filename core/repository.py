import os
from models import Usuario, Materia, Oferta, Encuesta, Comision, db

from pymemcache.client.base import Client


class Repository(object):

    def __init__(self):
        self.cache = Client(('memcached', 11211))

    def get_encuesta_activa(self, username):
        encuesta = self.buscar_encuesta_alumno(username)
        return encuesta.get_json_data()

    def guardar_encuesta_alumno(self, data):
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
        #TODO: Catchear una posible excepcion
        alumno = Usuario.query.filter_by(username=username).first()
        if alumno is None:
            raise Exception('El usuario ' + username + ' no existe')
        oferta_activa = Oferta.query.filter_by(activa=True).first()
        encuesta = Encuesta.query.filter_by(oferta_id=oferta_activa.id, alumno_id=alumno.id).first()
        if not encuesta:
            encuesta = self.crear_encuesta(oferta_activa, alumno)
        return encuesta

    def crear_encuesta(self, oferta, alumno):
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
        encuesta.aprobadas = []
        for data_materia in materias:
            materia = Materia.query.filter(Materia.id == data_materia['id']).first()
            encuesta.aprobadas.append(materia)

    def guardar_materias_imposibilitadas(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias imposibilitadas y lo relaciono
        """
        encuesta.imposibilitadas = []
        for data_materia in materias:
            materia = Materia.query.filter(Materia.id == data_materia['id']).first()
            encuesta.imposibilitadas.append(materia)

    def guardar_materias_cursables(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias cursables y lo relaciono
        """
        encuesta.cursables = []
        for data_materia in materias:
            materia = Materia.query.filter(Materia.id == data_materia['id']).first()
            encuesta.cursables.append(materia)

    def guardar_materias_preinscripcion(self, encuesta, materias):
        """
            * Con la encuesta ya traida de la BD, recorro el json de materias preinscripcion y lo relaciono
        """
        encuesta.preinscripcion = []
        for data_materia in materias:
            comision = Comision.query.filter(Comision.id == data_materia['comision_seleccionada']['id']).first()
            encuesta.preinscripcion.append(comision)


    def get_resultados(self):
        #En un principio se penso para ver resultados de muchas ofertas, pero se va a hacer solo para la activar
        oferta = Oferta.query.filter(Oferta.activa == True).first()
        #Deberia ser por oferta, pero para la muestra solo hay 1 oferta
        resultados = self.cache.get('resultados')
        if not resultados:
            resultados = oferta.get_resultados()
            self.cache.set('resultados', resultados)
        return resultados

    def get_materias(self):
        resultado = self.cache.get('materias')
        if not resultado:
            materias = Materia.query.all()
            resultado = []
            for m in materias:
                comisiones = Comision.query.filter_by(materia_id = m.id).all()
                cs = []
                for c in comisiones:
                    cs.append({'id': c.id, 'descripcion': c.descripcion, 'cupo': c.cupo})
                resultado.append({'id': m.id, 'nombre': m.nombre, 'cuatrimestre': m.cuatrimestre, 'oferta_id': m.oferta_id,
                    'comisiones': cs})
            self.cache.set('materias', resultado)
        return resultado

    def get_materia_por_nombre(self,nombre):
        m = Materia.query.filter_by(nombre=nombre).first()
        if m is None:
            return None
        else:
            comisiones = Comision.query.filter_by(materia_id = m.id).all()
            cs = []
            for c in comisiones:
                cs.append({'id': c.id, 'descripcion': c.descripcion, 'cupo': c.cupo})
            return {'id': m.id, 'nombre': m.nombre, 'cuatrimestre': m.cuatrimestre, 'oferta_id': m.oferta_id,
            'comisiones': cs}

    def get_materias_de_oferta(self,oferta_id):
        materias = Materia.query.filter_by(oferta_id=oferta_id).all()
        r = []
        for m in materias:
            r.append({'id': m.id, 'nombre': m.nombre, 'cuatrimestre': m.cuatrimestre, 'oferta_id': m.oferta_id})
        return r

    def get_usuarios(self):
        resultado = self.cache.get('usuarios')
        if not resultado:
            resultado = []
            usuarios = Usuario.query.all()
            for u in usuarios:
                roles = []
                for rol in u.roles:
                    roles.append({'id': rol.id, 'name': rol.name})
                resultado.append({'id': u.id, 'nombre': u.nombre, 'username': u.username, 'email': u.email,'roles': roles})
            self.cache.set('usuarios', resultado)
        return resultado

    def get_usuario_por_username(self,username):
        u = Usuario.query.filter_by(username=username).first()
        if u is None:
            return None
        else:
            roles = []
            for rol in u.roles:
                roles.append({'id': rol.id, 'name': rol.name})
            return {'id': u.id, 'nombre': u.nombre, 'username': u.username, 'email': u.email,'roles': roles}

    def get_oferta(self,id):
        oferta = Oferta.query.filter_by(id=id).first()
        if oferta is None:
            return None
        else:
            return {
                'id': oferta.id,
                'nombre': oferta.nombre,
                'activa': oferta.activa,
                'materias': self.get_materias_de_oferta(oferta.id)
            }
