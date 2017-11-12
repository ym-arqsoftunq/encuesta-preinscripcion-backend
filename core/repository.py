import os
import json

class Repository(object):

    def get_oferta(self, oferta_id):
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "oferta_%s.json" % (oferta_id))
        return json.load(open(json_url))

    def get_encuesta_alumno(self, oferta_id, alumno_id):
        try:
            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
            json_url = os.path.join(SITE_ROOT, "oferta_%s_alumno_%s.json" % (oferta_id, alumno_id))
            data = json.load(open(json_url))
        except:
            data = self.get_oferta(oferta_id)
        return data
