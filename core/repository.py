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
        try:
            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
            json_url = os.path.join(SITE_ROOT, "encuestas/oferta_%s_alumno_%s.json" % (oferta_id, alumno_id))
            data = json.load(open(json_url))
        except:
            data = self.get_oferta(oferta_id, alumno_id)
        return data

    def guardar_encuesta_alumno(self, encuesta):
        oferta_id = encuesta['oferta']['id']
        alumno_id = encuesta['alumno']['username']
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "encuestas/oferta_%s_alumno_%s.json" % (oferta_id, alumno_id))
        with open(json_url, 'w') as fp:
            json.dump(encuesta, fp)
