# -*- coding: utf-8 -*-
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
    alu2 = Usuario('Nestor Muñoz', 'nestorgabriel2008', 'nestorgabriel2008@gmail.com', 'nestor')
    alu3 = Usuario('Nestor Muñoz 2', 'nestorgabriel2004', 'nestorgabriel2004@hotmail.com', 'nestor')
    alu4 = Usuario('Sin Encuesta', 'sinencuesta', 'sinencuesta@unq.edu.ar', 'sinencuesta')
    director = Usuario('Director', 'director', 'director@unq.edu.ar', 'director')

    rol_alu = Rol('alumno')
    rol_dir = Rol('director')
    alu.roles.append(rol_alu)
    alu2.roles.append(rol_alu)
    alu3.roles.append(rol_alu)
    alu4.roles.append(rol_alu)
    director.roles.append(rol_dir)

    #Materias y comisiones
    # c1 = Comision('De 18hs a 20hs', 20)
    # c2 = Comision('De 20hs a 22hs', 40)
    # m1 = Materia('Algoritmos', 4)
    # m1.comisiones.append(c1)
    # m1.comisiones.append(c2)

    # c3 = Comision('De 20hs a 22hs', 30)
    # m2 = Materia('Arquitectura de Computadoras', 8)
    # m2.comisiones.append(c3)

    # c4 = Comision('De 16hs a 18hs', 30)
    # c5 = Comision('De 18hs a 20hs', 40)
    # m3 = Materia('Matematica 1', 1)
    # m3.comisiones.append(c4)
    # m3.comisiones.append(c5)

    materias_c1 = ['Introduccion a la programacion','Matematica 1','Organizacion de computadoras']
    materias_c2 = ['Programacion con objetos 1','Estructuras de datos','Bases de datos']
    materias_c3 = ['Matematica 2','Programacion con objetos 2','Sistemas operativos','Redes de computadoras']
    materias_c4 = ['Estrategias de persistencia','Construccion de interfaces de usuario','Elementos de ingenieria de software','Programacion concurrente']
    materias_c5 = ['Desarrollo de aplicaciones','Programacion funcional','Laboratorio de sistemas operativos y redes']

    comisiones = []
    materias = []


    # TODO: ELIMINAR ESTA REPETICION DE CODIGO
    for m in materias_c1:
        c1 = Comision('Lunes de 18hs a 20hs', 20)
        db.session.add(c1)
        c2 = Comision('Martes de 20hs a 22hs', 40)
        db.session.add(c2)
        materia = Materia(m,1)
        materia.comisiones.append(c1)
        materia.comisiones.append(c2)
        db.session.add(materia)
        materias.append(materia)

    for m in materias_c2:
        c1 = Comision('Miercoles de 18hs a 20hs', 20)
        db.session.add(c1)
        c2 = Comision('Jueves de 20hs a 22hs', 40)
        db.session.add(c2)
        materia = Materia(m,2)
        materia.comisiones.append(c1)
        materia.comisiones.append(c2)
        db.session.add(materia)
        materias.append(materia)

    for m in materias_c3:
        c1 = Comision('Viernes de 18hs a 20hs', 20)
        db.session.add(c1)
        c2 = Comision('Sabados de 10hs a 12hs', 40)
        db.session.add(c2)
        materia = Materia(m,3)
        materia.comisiones.append(c1)
        materia.comisiones.append(c2)
        db.session.add(materia)
        materias.append(materia)

    for m in materias_c4:
        c1 = Comision('Lunes de 18hs a 20hs', 20)
        db.session.add(c1)
        c2 = Comision('Jueves de 20hs a 22hs', 40)
        db.session.add(c2)
        materia = Materia(m,4)
        materia.comisiones.append(c1)
        materia.comisiones.append(c2)
        db.session.add(materia)
        materias.append(materia)

    for m in materias_c5:
        c1 = Comision('Martes de 18hs a 20hs', 20)
        db.session.add(c1)
        c2 = Comision('Viernes de 20hs a 22hs', 40)
        db.session.add(c2)
        materia = Materia(m,5)
        materia.comisiones.append(c1)
        materia.comisiones.append(c2)
        db.session.add(materia)
        materias.append(materia)

    #Oferta
    oferta = Oferta("2017s2")
    oferta.activa = True
    # oferta.materias.append(m1)
    # oferta.materias.append(m2)
    # oferta.materias.append(m3)
    for materia in materias:
        oferta.materias.append(materia)

    db.session.add(oferta)

    db.session.add(rol_alu)
    db.session.add(rol_dir)
    db.session.add(alu)
    db.session.add(alu2)
    db.session.add(alu3)
    db.session.add(alu4)
    db.session.add(director)
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(m1)
    # db.session.add(c3)
    # db.session.add(c4)
    # db.session.add(c5)
    # db.session.add(m2)
    # db.session.add(m3)
    db.session.commit()

    #Encuesta contestada
    encuesta = Encuesta(oferta.id, alu.id)
    encuesta.aprobadas.append(materias[0])
    encuesta.aprobadas.append(materias[1])
    encuesta.aprobadas.append(materias[2])
    encuesta.respondida = True
    encuesta.preinscripcion.append(materias[3].comisiones[0])
    encuesta.preinscripcion.append(materias[4].comisiones[1])
    for i in range(5,17):
        encuesta.cursables.append(materias[i])

    # Encuesta nueva (todas las materias en cursables)
    encuesta2 = Encuesta(oferta.id, alu2.id)
    for m in materias:
        encuesta2.cursables.append(m)

    db.session.commit()

if __name__ == '__main__':
    clear_data(db)
    load_data(db)
