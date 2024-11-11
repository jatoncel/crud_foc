import sqlite3

class ConsultaSQL ():
	
	database = "database/Empalmes.db"

	# sentencias SQL
	CrearTabla = '''CREATE TABLE "Empalmes" (
		"id_empalme"	INTEGER NOT NULL UNIQUE,
		"nombre"	VARCHAR(20) NOT NULL,
		"descripcion"	VARCHAR(100),
		"caja_empalme"	VARCHAR(25) NOT NULL,
		"direccion"	VARCHAR(100),
		"id_punto_apoyo"	INTEGER NOT NULL,
		PRIMARY KEY("id_empalme"),
		CONSTRAINT "FK_Empalme.id_punto_apoyo" FOREIGN KEY("id_punto_apoyo") REFERENCES "PuntosDeApoyo"("id_punto_apoyo")
		);'''
	
	
	leer_registro_apoyo = "SELECT * FROM PuntoDeApoyos WHERE id_punto_apoyo = ?"

	leer_registro_cable = "SELECT * FROM Cables WHERE id_empalme = ? ORDER BY puerto_caja_empalme ASC"

	leer_registro_empalme = "SELECT * FROM Empalmes WHERE id_punto_apoyo = ?"

	actualizar_registro_cable = """ UPDATE Cables SET 
									id_Cable=?, etiqueta=?, 
									hilos=?, tipo_Cable=?, 
									fabricante=?, sangria=?, 
									puerto_caja_empalme=?, id_empalme=?
									WHERE id_Cable=? """
	
	actualizar_registro_empalme = """ UPDATE Cables SET 
									id_empalme=?, nombre=?, 
									descripcion=?, caja_empalme=?, 
									id_punto_apoyo=?
									WHERE id_empalme=? """

	crear_registro_fila = """ INSERT INTO CablesFO (item, id_Cable, 
								etiqueta, hilos, tipo_Cable, 
								fabricante, sangria) 
								VALUES (?, ?, ?, ?, ?, ?, ?) """

	crear_registro_cable = """ INSERT INTO Cables (id_cable, etiqueta, 
								hilos, tipo_Cable, fabricante, sangria, 
								puerto_caja_empalme, id_empalme) 
								VALUES (?, ?, ?, ?, ?, ?, ?, ?) """

	crear_registro_empalme = """ INSERT INTO Empalmes (id_empalme, 
								nombre, caja_empalme, descripcion, 
								id_punto_apoyo) 
								VALUES (?, ?, ?, ?, ?) """
	
	crear_registro_apoyo = """ INSERT INTO PuntosDeApoyo (id_punto_apoyo, 
								nombre, tipo_apoyo, 
								direccion, coordenadas) 
								VALUES (?, ?, ?, ?, ?) """

	buscarEnTabla = "SELECT nombre, id_punto_apoyo, tipo_apoyo, direccion FROM empalmes WHERE id = ?"

	buscarEmpalme = """ SELECT e.nombre, e.caja_empalme, e.descripcion, 
						pa.id_punto_apoyo, pa.nombre, pa.direccion, pa.coordenadas, pa.tipo_apoyo, 
						c.id_cable, c.etiqueta, c.hilos, c.tipo_cable, c.fabricante, c.sangria, c.puerto_caja_empalme
						FROM Empalmes e 
						JOIN PuntosDeApoyo pa ON e.id_punto_apoyo = pa.id_punto_apoyo 
						LEFT JOIN cables c ON e.id_empalme = c.id_empalme
						WHERE e.id_empalme = ? """
	
	buscarApoyo = """ SELECT pa.nombre, pa.direccion, pa.coordenadas, pa.tipo_apoyo, 
					e.id_empalme, e.nombre, e.caja_empalme, e.descripcion
					FROM PuntosDeApoyo pa 
					LEFT JOIN Empalmes e ON pa.id_punto_apoyo = e.id_punto_apoyo 
					WHERE pa.id_punto_apoyo = ? """

	