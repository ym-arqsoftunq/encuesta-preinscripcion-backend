from models import *

def clear_data(db):
    meta = db.metadata
    session = db.session
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()

def load_data(db):
    #Alumno
    alu = Usuario('Juan Ignacio Yegro', 'juan.yegro', 'juan.yegro@unq.edu.ar', 'alumno')
    director = Usuario('Director', 'director', 'director@unq.edu.ar', 'director')

    rol_alu = Rol('alumno')
    rol_dir = Rol('director')
    alu.roles.append(rol_alu)
    director.roles.append(rol_dir)

    #Materias y comisiones
    c1 = Comision('De 18hs a 20hs', 20)
    c2 = Comision('De 20hs a 22hs', 40)
    m1 = Materia('Algoritmos', 4)
    m1.comisiones.append(c1)
    m1.comisiones.append(c2)

    c3 = Comision('De 20hs a 22hs', 30)
    m2 = Materia('Arquitectura de Computadoras', 8)
    m2.comisiones.append(c3)

    c4 = Comision('De 16hs a 18hs', 30)
    c5 = Comision('De 18hs a 20hs', 40)
    m3 = Materia('Matematica 1', 1)
    m3.comisiones.append(c4)
    m3.comisiones.append(c5)

    #Oferta
    oferta = Oferta("2017s2")
    oferta.activa = True
    oferta.materias.append(m1)
    oferta.materias.append(m2)
    oferta.materias.append(m3)
    db.session.add(oferta)

    db.session.add(rol_alu)
    db.session.add(rol_dir)
    db.session.add(alu)
    db.session.add(director)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(m1)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.add(m2)
    db.session.add(m3)
    db.session.commit()

    #Encuesta
    encuesta = Encuesta(oferta.id, alu.id)
    encuesta.aprobadas.append(m1)
    encuesta.aprobadas.append(m2)
    encuesta.respondida = True
    encuesta.preinscripcion.append(c5)

    db.session.commit()

if __name__ == '__main__':
    clear_data(db)
    load_data(db)
