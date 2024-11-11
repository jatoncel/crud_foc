from ConsultaSQL import *


nombreBD = ConsultaSQL.database

class Servicio ():

    def __init__(self):
        pass

    def ejecutar(consulta, parametros=()):
        with sqlite3.connect(nombreBD) as conexionBD:
            cursorBD = conexionBD.cursor()
            respuesta = cursorBD.execute(consulta, parametros)
            conexionBD.commit()
        return respuesta
    
    
    # Función para guardar los nuevos datos del Empalme
    def guardar_empalme(entradas, id_apoyo):
        nuevos_valores = []         # se crea lista para almacenar los nuevos datos
        
        """ nuevos_valores = [entry.get() for entry in entradas] """
        for entrada in entradas:
            nuevos_valores.append(entrada.get())

        print(nuevos_valores)

        # Actualizar la base de datos
        Servicio.ejecutar(ConsultaSQL.crear_registro_empalme, (*nuevos_valores, id_apoyo))
