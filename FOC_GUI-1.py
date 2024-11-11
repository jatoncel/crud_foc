from ElementosRed import *
from ConsultaSQL import *

import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Label, Button, Entry, Frame, Image, PhotoImage, LabelFrame, Text, Toplevel, messagebox
import sqlite3
from PIL import Image, ImageTk

nombreBD = ConsultaSQL.database

def ejecutar(consulta, parametros=()):
    with sqlite3.connect(nombreBD) as conexionBD:
        cursorBD = conexionBD.cursor()
        respuesta = cursorBD.execute(consulta, parametros)
        conexionBD.commit()
    return respuesta

""" def conectar ():
    conexionBD = sqlite3.connect(nombreBD)
    cursorBD = conexionBD.cursor()
    return conexionBD, cursorBD """

""" def copiar():
    ent_dir.delete(0, 'end')
    idEmpalme = ent_idEmpalme.get()
    ent_dir.insert(0,idEmpalme) """

def get_id_empalme():
    id_empalme = ent_idEmpalme.get()
    return id_empalme

def get_id_apoyo():
    id_apoyo = ent_idApoyo.get()
    return id_apoyo

def get_nombre_apoyo():
    nombre_apoyo = ent_nombreApoyo.get()
    return nombre_apoyo

def limpiar_tabla_empalmes():
    registros=tbl_empalmes.get_children()
    [tbl_empalmes.delete(elemento) for elemento in registros]
    # tbl_Empalmes.delete(*tbl_Empalmes.get_children())


def limpiar_tabla_cables():
    registros=tbl_cables.get_children()
    [tbl_cables.delete(elemento) for elemento in registros]
    # tbl_Cables.delete(*tbl_Cables.get_children())


def limpiar_tabla_fusiones():
    pass

# crear nuevo REGISTRO de PUNTO DE APOYO en la base de datos
def db_crear_apoyo(entradas):
    nuevos_valores = []         # se crea lista para almacenar los nuevos datos
    
    #nuevos_valores = [entrada.get() for entrada in entradas]
    for entrada in entradas:
        nuevos_valores.append(entrada.get())

    # Actualizar la base de datos
    ejecutar(ConsultaSQL.crear_registro_apoyo, (*nuevos_valores,))

# crear nuevo REGISTRO de CAJA DE EMPALME en la base de datos
def db_crear_empalme(entradas, id_apoyo):
    nuevos_valores = []         # se crea lista para almacenar los nuevos datos
    
    #nuevos_valores = [entrada.get() for entrada in entradas]
    for entrada in entradas:
        nuevos_valores.append(entrada.get())

    # Actualizar la base de datos
    ejecutar(ConsultaSQL.crear_registro_empalme, (*nuevos_valores, id_apoyo))


# crear nuevo REGISTRO de CABLE en la base de datos
def db_crear_cable(entradas, id_Empalme):
    nuevos_valores = []         # se crea lista para almacenar los nuevos datos
    
    # nuevos_valores = [entry.get() for entry in entradas]
    for entrada in entradas:
        nuevos_valores.append(entrada.get())

    """ # se pasa el primer dato de la lista (que corresponde al puerto_caja_empalme) al final
    dato_0 = nuevos_valores.pop(0)
    nuevos_valores.append(dato_0) """

    # Actualizar la base de datos
    ejecutar(ConsultaSQL.crear_registro_cable, (*nuevos_valores, id_Empalme))

    db_leer_Cables(id_Empalme)


# obtener desde la base de datos, listado de Empalmes ubicados en Punto de Apoyo determinado
def db_leer_empalmes(id_apoyo):
    limpiar_tabla_empalmes()
    empalmes = ejecutar(ConsultaSQL.leer_registro_empalme, (id_apoyo,))

    for empalme in empalmes:
        tbl_empalmes.insert("", 'end', text=empalme[0], values=empalme[1:])

# obtener desde la base de datos, listado de Cables en un Empalme dado
def db_leer_Cables(id_empalme):
    limpiar_tabla_cables()
    cables = ejecutar(ConsultaSQL.leer_registro_cable, (id_empalme,))
    
    for cable in cables:
        tbl_cables.insert("", 'end', text=cable[0], values=cable[1:])



# actualizar los cambios en la informacion del cable
def db_actualizar_cable(entradas, id_Empalme, id_Cable):

    nuevos_valores = []             # se crea una lista para almacenar los datos actualizados

    for entrada in entradas:
        nuevos_valores.append(entrada.get())

    # Actualizar informacion del cable en la base de datos
    ejecutar(ConsultaSQL.actualizar_registro_cable, (*nuevos_valores, id_Empalme, id_Cable))
    
    db_leer_Cables(id_Empalme)


# establecer estado de validacion para el widget
def set_validation_entry(widget, estado):
    widget.config(validate=estado)

# establecer estado del widget
def set_state_widget(widget, estado):
    widget.config(state=estado)

def deshab_btn_agregarEmpalme():
    set_state_widget(btn_agregarEmpalme, 'disabled')

def hab_btn_agregarEmpalme():
    set_state_widget(btn_agregarEmpalme, 'normal')

def deshab_btn_agregarCable():
    set_state_widget(btn_agregarCable, 'disabled')

def hab_btn_agregarCable():
    set_state_widget(btn_agregarCable, 'normal')

def deshab_ent_nombreApoyo():
    set_state_widget(ent_nombreApoyo, 'readonly')

def hab_ent_nombreApoyo():
    set_state_widget(ent_nombreApoyo, 'normal')

def deshab_ent_nombreEmpalme():
    set_state_widget(ent_nombreEmpalme, 'readonly')

def hab_ent_nombreEmpalme():
    set_state_widget(ent_nombreEmpalme, 'normal')

# limpiar widgets de entrada de datos
def limpiar_campos_todos():
    limpiar_campos_empalme()
    limpiar_campos_apoyo()

# limpiar datos ingresados del empalme
def limpiar_campos_empalme ():
    hab_ent_nombreEmpalme()        # Habilitar temporalmente el widget para poder modificarlo
    set_validation_entry(ent_idEmpalme, 'none')        # Desactivar la validación temporalmente

    for widget in [ent_idEmpalme, ent_nombreEmpalme, ent_ref, ent_descrEmpalme]:
        widget.delete(0, 'end')

    deshab_ent_nombreEmpalme()      # Restaurar el estado original del widget a 'readonly'
    set_validation_entry(ent_idEmpalme, 'key')         # Reactivar la validación

    deshab_btn_agregarCable()
    limpiar_tabla_cables()
    ent_idEmpalme.focus()

# limpiar datos ingresados del punto de apoyo
def limpiar_campos_apoyo ():
    hab_ent_nombreApoyo()
    set_validation_entry(ent_idApoyo, 'none')

    for widget in [ent_idApoyo, ent_nombreApoyo, ent_dir, ent_tipoApoyo, ent_coord]:
        widget.delete(0, 'end')

    deshab_ent_nombreApoyo()
    set_validation_entry(ent_idApoyo, 'key')

    deshab_btn_agregarEmpalme()

    limpiar_tabla_empalmes()
    ent_idApoyo.focus()


def validar_numero(texto, prefijo, entry_actualizar):
    # Permite solo números
    if texto.isdigit():
        valor_formateado = f"{prefijo}{int(texto):05d}"     # Obtener el valor ingresado y formatearlo
        set_state_widget(entry_actualizar,'normal')             # Habilitar temporalmente para modificar       
        entry_actualizar.delete(0, 'end')
        entry_actualizar.insert(0, valor_formateado)
        set_state_widget(entry_actualizar,'readonly')           # Volver a colocar en modo solo lectura
        return True
    elif texto=='':
        set_state_widget(entry_actualizar,'normal') 
        entry_actualizar.delete(0, 'end')
        set_state_widget(entry_actualizar,'readonly')
        return True
    else:
        return False

# Función para actualizar informacion del Cable
def editar_cable(event):
    item = tbl_cables.selection()[0]
    text_0 = tbl_cables.item(item, 'text')      # dato columna 0
    values = tbl_cables.item(item, 'values')    # datos demas columnas de la tabla

    # agrupar los valores actuales de la fila seleccionada, en una lista
    valores_actuales = [text_0,]
    valores_actuales.extend(values)

    # campos de la tabla (Tbl_Cables) suceptibles a modificacion
    cmp_idCable = 'Id Cable'
    cmp_etiqueta = 'Etiqueta'
    cmp_hilos = 'Hilos'
    cmp_tipoCable = 'Tipo Cable'
    cmp_fabricante = 'Fabricante'
    cmp_sangria = 'Sangria'
    cmp_puerto = 'Puerto'

    # Crear una ventana emergente para editar los valores
    vent_editar = Toplevel(vent_ppal)
    vent_editar.title(f"Editar Datos del Cable {text_0}")

    campos_cable = [cmp_idCable, cmp_etiqueta, cmp_hilos, cmp_tipoCable, cmp_fabricante, cmp_sangria, cmp_puerto]
    size_campos_cable = [10, 25, 10, 15, 20, 7, 15]
    
    entradas = []        # crear una lista para almacenar los widgets entry

    # Crear widgets Label y Entry para cada columna en la ventana emergente
    for campo in campos_cable:
        indice = campos_cable.index(campo)
        label = Label(vent_editar, text=campo)
        label.grid(row=0, column=indice, sticky="w", pady=5)
        
        name_entry = (campo.replace(' ','_').lower())
        entry = Entry(vent_editar, name=(name_entry), width=size_campos_cable[indice])
        entry.grid(row=1, column=indice, sticky="w")

        entradas.append(entry)
        
        # Prellenar los campos con los valores actuales
        dato = valores_actuales[indice]
        entry.insert(0, dato)

    # Función para guardar los cambios
    def guardar_cambios():

        idEmpalme = int(get_id_empalme())
        idCable = int(valores_actuales[0])
        
        db_actualizar_cable(entradas, idEmpalme, idCable)
        
        vent_editar.destroy()

    # Crear Botón para guardar los cambios
    guardar_boton = Button(vent_editar, text="Guardar", command=guardar_cambios)
    guardar_boton.grid(row=3, column=0, columnspan=6, pady=5)

# obtener informacion del Empalme seleccionado
def leer_empalme(event):
    items = tbl_empalmes.selection()[0]
    text1 = tbl_empalmes.item(items, 'text')       # dato columna 0
    values = tbl_empalmes.item(items, 'values')    # datos demas columnas de la tabla

    limpiar_campos_empalme()

    ent_idEmpalme.insert(0, text1)
    ent_nombreEmpalme.insert(0, values[0])
    ent_ref.insert(0, values[1])
    ent_descrEmpalme.insert(0, values[2])

    hab_btn_agregarCable()
    db_leer_Cables(text1)

# Función para agregar un nuevo Cable en caja de Empalme
def agregar_cable():

    id_empalme = get_id_empalme()
    name_empalme = ent_nombreEmpalme.get()

    # Crear una ventana emergente
    vent_agregar = Toplevel()
    vent_agregar.title(f"Agregar Nuevo Cable En La Caja De Empalme {name_empalme}")

    # campos de la tabla (Tbl_Cables)
    campos = ["Id Cable", "Etiqueta", "Hilos", "Tipo Cable", "Fabricante", "Sangria", "Puerto"]
    size_campos_cable = [10, 25, 10, 15, 20, 7, 15]
    entradas = []

    # Crear los widgets Label y Entry (campos de entrada)
    for campo in campos:
        indice = campos.index(campo)
        label = Label(vent_agregar, text=campo)
        label.grid(row=0, column=indice, sticky="w", pady=5)
        entry = Entry(vent_agregar, width=size_campos_cable[indice])
        entry.grid(row=1, column=indice)

        entradas.append(entry)
    
    # Función para guardar los datos y cerrar la ventana
    def guardar_cable():

        db_crear_cable(entradas,id_empalme)

        vent_agregar.destroy()          # cerrar la ventana emergente

    boton_guardar = Button(vent_agregar, text="Guardar", command=guardar_cable)
    boton_guardar.grid(row=3, column=0, columnspan=6, pady=5)

def crear_apoyo (id_apoyo='', nombre_apoyo=''):
    # Crear ventana emergente para registrar los datos del nuevo PUNTO DE APOYO
    vent_crear_apoyo = Toplevel(vent_ppal)
    vent_crear_apoyo.title(f"Crear Registro de Nuevo Punto De Apoyo")

    # frame informacion del punto de apoyo de ubicacion del empalme
    frm_PuntoApoyo = LabelFrame(vent_crear_apoyo, text="Punto de Apoyo", relief='solid', borderwidth=1,)
    frm_PuntoApoyo.grid(row=0, column=1, padx=[5, 10], pady=[5, 10], ipady=10, sticky="N" )

    # datos solicitados del Punto de Apoyo donde esta ubicado el Empalme
    campos_apoyo = ["Id Punto Apoyo", "Nombre", "Tipo Apoyo", "Direccion", "Coordenadas"]
    size_campos_ap = [15, 15, 10, 20, 25]
    datos_apoyo = []

    # Crear los widgets Label y Entry (campos de entrada)
    for campo in campos_apoyo:
        indice = campos_apoyo.index(campo)
        label = Label(frm_PuntoApoyo, text=campo)
        label.grid(row=0, column=indice, sticky="w", pady=5)

        name_entry = (campo.replace(' ','_').lower())
        entry = Entry(frm_PuntoApoyo, name=(name_entry), width=size_campos_ap[indice])
        entry.grid(row=1, column=indice, padx=2)

        datos_apoyo.append(entry)

    datos_apoyo[0].insert(0, id_apoyo)
    datos_apoyo[1].insert(0, nombre_apoyo)

    def guardar_apoyo():
        db_crear_apoyo(datos_apoyo)

        vent_crear_apoyo.destroy()          # cerrar la ventana emergente

    btn_guardar = Button(vent_crear_apoyo, text="Guardar")
    btn_guardar.grid(row=3, column=0, columnspan=6, pady=[0,10])
    btn_guardar.config(command=guardar_apoyo)

    # datos_apoyo[0].insert(0, id_apoyo)
    # datos_apoyo[0].configure(state="disabled")
    # datos_apoyo[1].insert(0, nombre_apoyo)
    # datos_apoyo[1].configure(state="disabled")

def crear_empalme ():
    # Crear una ventana emergente para editar los valores
    vent_crearEmpalme = Toplevel(vent_ppal)
    vent_crearEmpalme.title(f"Registrar Nueva Caja de Empalme")

    # frame informacion del empalme
    frm_empalme = LabelFrame(vent_crearEmpalme, text="Caja de Empalme", relief='solid', borderwidth=1, )
    frm_empalme.grid(row=0, column=0, padx=[10, 5], pady=[5, 10], ipady=10, sticky="N", )

    # frame informacion del punto de apoyo de ubicacion del empalme
    frm_PuntoApoyo = LabelFrame(vent_crearEmpalme, text="Punto de Apoyo", relief='solid', borderwidth=1,)
    frm_PuntoApoyo.grid(row=0, column=1, padx=[5, 10], pady=[5, 10], ipady=10, sticky="N" )

##---------------------------------------------------------------------------------
     # datos solicitados del Empalme a registrar
    campos_empalme = ["Id Empalme", "Nombre", "Cierre", "Descripcion"]
    size_campos_emp = [15, 15, 10, 30]
    datos_empalme = []

    # Crear los widgets Label & Entry (campos de entrada de datos)
    for campo in campos_empalme:
        indice = campos_empalme.index(campo)
        label = Label(frm_empalme, text=campo)
        label.grid(row=0, column=indice, sticky="w", pady=5)
        entry = Entry(frm_empalme, width=size_campos_emp[indice])
        entry.grid(row=1, column=indice, padx=2)

        datos_empalme.append(entry)
##---------------------------------------------------------------------------------
##---------------------------------------------------------------------------------
    # datos solicitados del Punto de Apoyo donde esta ubicado el Empalme
    campos_apoyo = ["Id Punto Apoyo", "Nombre", "Tipo Apoyo", "Direccion", "Coordenadas"]
    size_campos_ap = [15, 15, 10, 20, 25]
    datos_apoyo = []

    # Crear los widgets Label y Entry (campos de entrada)
    for campo in campos_apoyo:
        indice = campos_apoyo.index(campo)
        label = Label(frm_PuntoApoyo, text=campo)
        label.grid(row=0, column=indice, sticky="w", pady=5)
        entry = Entry(frm_PuntoApoyo, width=size_campos_ap[indice])
        entry.grid(row=1, column=indice, padx=2)

        datos_apoyo.append(entry)
##---------------------------------------------------------------------------------

    btn_guardar = Button(vent_crearEmpalme, text="Guardar")
    btn_guardar.grid(row=3, column=0, columnspan=6, pady=[0,10])
    btn_guardar.config()

# Función para agregar un nuevo Empalme en Punto de Apoyo
def agregar_empalme():
    
    id_apoyo=get_id_apoyo()
    
    # Crear una ventana emergente
    vent_agregarEmpalme = Toplevel()
    vent_agregarEmpalme.title(f"Agregar Caja De Empalme En El Punto De Apoyo {id_apoyo}")

    # frame informacion del empalme
    frm_empalme = LabelFrame(vent_agregarEmpalme, text="Caja de Empalme", relief='solid', borderwidth=1, )
    frm_empalme.grid(row=0, column=0, padx=[10, 10], pady=[10, 10], ipady=10, sticky="N", )

    # campos para la tabla (Tbl_Empalmes)
    campos_empalme = ["Id Empalme", "Nombre", "Cierre", "Descripcion"]
    size_campos = [15, 15, 10, 30]
    entradas = []

    # Crear los widgets Label y Entry (de los campos para  entrada de datos)
    for campo in campos_empalme:
        indice = campos_empalme.index(campo)
        label = Label(frm_empalme, text=campo)
        label.grid(row=0, column=indice, sticky="w", pady=5)
        entry = Entry(frm_empalme, width=size_campos[indice])
        entry.grid(row=1, column=indice, padx=2)

        entradas.append(entry)

    def guardar_empalme():
        db_crear_empalme(entradas, id_apoyo)
        
        db_leer_empalmes(id_apoyo)
        vent_agregarEmpalme.destroy()          # cerrar la ventana emergente
    
    btn_guardar = Button(vent_agregarEmpalme, text="Guardar")
    btn_guardar.grid(row=3, column=0, columnspan=6, pady=[0,10])
    btn_guardar.config(command=guardar_empalme)



# Funcion Buscar Id Empalme
def buscar_empalme():
    id_empalme = get_id_empalme()

    consulta = ejecutar(ConsultaSQL.buscarEmpalme,(id_empalme,))


    # # Conectar a la base de datos
    # conn = sqlite3.connect(nombreBD)
    # cursor = conn.cursor()

    # # Consulta para buscar el empalme y obtener todos los datos relevantes
    # cursor.execute("""SELECT e.nombre, e.caja_empalme, e.descripcion, 
    #                pa.id_punto_apoyo, pa.nombre, pa.direccion, pa.coordenadas, pa.tipo_apoyo, 
    #                c.id_cable, c.etiqueta, c.hilos, c.tipo_cable, c.fabricante, c.sangria, c.puerto_caja_empalme
    #                FROM Empalmes e 
    #                JOIN PuntosDeApoyo pa ON e.id_punto_apoyo = pa.id_punto_apoyo 
    #                LEFT JOIN cables c ON e.id_empalme = c.id_empalme
    #                WHERE e.id_empalme = ?""", (id_empalme,))
    

    # conn.commit()

    # resultado = cursor.fetchone()       # devuelve una tupla
    resultados = consulta.fetchall()      # devuelve una lista de tuplas

    if resultados:
        # Actualizar los campos de texto        
        limpiar_campos_empalme()
        limpiar_campos_apoyo()

        ent_idEmpalme.insert(0, id_empalme)

        ent_ref.insert(0, resultados[0][1])
        ent_descrEmpalme.insert(0, resultados[0][2])
        ent_idApoyo.insert(0, resultados[0][3])
        ent_dir.insert(0, resultados[0][5])
        ent_coord.insert(0, resultados[0][6])
        ent_tipoApoyo.insert(0, resultados[0][7])

        hab_btn_agregarCable()
        hab_btn_agregarEmpalme()
        
        # Limpiar y poblar el Treeview de los cables en la caja de empalme
        limpiar_tabla_cables()

        db_leer_Cables(id_empalme)

        # for fila in resultados[0:]:  # comenzar desde el primer resultado aunque ya se usó para los campos
        #     tbl_cables.insert("", tk.END, text=fila[8], values=fila[9:])  # Insertar solo los datos de los cables

        # Limpiar y poblar el Treeview de los empalmes en el punto de apoyo
        limpiar_tabla_empalmes()

        # Obtener los empalmes asociados al punto de apoyo
        id_apoyo = get_id_apoyo()
        db_leer_empalmes(id_apoyo)

        # cursor.execute("SELECT id_empalme, nombre, caja_empalme, descripcion FROM empalmes WHERE id_punto_apoyo = ?", (resultados[0][3],))
        
        # empalmes = cursor.fetchall()        # empalmes en el punto de apoyo
        # for empalme in empalmes:
        #     tbl_empalmes.insert("", tk.END, text=empalme[0], values=empalme[1:])

    else:
        if id_empalme != '': 
            # Mostrar un mensaje indicando que no se encontró el empalme
            crearEmpalme = messagebox.askyesno("Búsqueda", f"""No se encontró el empalme {ent_nombreEmpalme.get()}. 
                                \n¿Desea crear un Nuevo Empalme con el ID {id_empalme}?""")

            if crearEmpalme:
                crear_empalme()

        else:
            # Mostrar un mensaje indicando que el campo esta vacio
            messagebox.showinfo("Búsqueda", "Favor ingresar numero de ID.")
        
        deshab_btn_agregarCable()

        # Limpiar los campos y Treeviews
        limpiar_campos_empalme()
        tbl_cables.delete(*tbl_cables.get_children())
        ent_idEmpalme.insert(0, id_empalme)



# Funcion Buscar Id Punto de Apoyo
def buscar_apoyo ():
    id_apoyo = get_id_apoyo()
    nombre_apoyo = ent_nombreApoyo.get()
    id_empalme = get_id_empalme()

    consulta = ejecutar(ConsultaSQL.buscarApoyo,(id_apoyo,))

    resultados = consulta.fetchall()      # devuelve una lista de tuplas

    if resultados:
               
        limpiar_campos_empalme()
        limpiar_campos_apoyo()

        # Actualizar los campos de texto 
        ent_idApoyo.insert(0, id_apoyo)
        ent_dir.insert(0, resultados[0][1])
        ent_coord.insert(0, resultados[0][2])
        ent_tipoApoyo.insert(0, resultados[0][3])

        hab_btn_agregarEmpalme()

        # Obtener los empalmes asociados al punto de apoyo
        db_leer_empalmes(id_apoyo)

    else:
        if id_apoyo != '': 
            # Mostrar un mensaje indicando que no se encontró el Punto de Apoyo
            crearPuntoApoyo = messagebox.askyesno("Búsqueda", f"""No se encontró el Punto De Apoyo {ent_nombreApoyo.get()}. 
                                \n¿Desea crear Nuevo Punto De Apoyo con el ID {id_apoyo}?""")

            if crearPuntoApoyo:
                crear_apoyo(id_apoyo, nombre_apoyo)

        else:
            # Mostrar un mensaje indicando que el campo esta vacio
            messagebox.showinfo("Búsqueda", "Favor ingresar numero de ID.")
        
        deshab_btn_agregarEmpalme()

        # Limpiar los campos y Treeviews
        limpiar_campos_apoyo()


# ventana principal
vent_ppal = Tk()
vent_ppal.title("Información Empalmes")
vent_ppal.geometry("1100x500")
vent_ppal.iconbitmap('imagenes/pyc.ico')

# imagen para boton buscar
img_boton = Image.open('imagenes/_buscar.png')
img_boton = img_boton.resize((20, 20), Image.LANCZOS) # Redimension (Alto, Ancho)
img_boton = ImageTk.PhotoImage(img_boton)

# frame informacion del empalme
frm_infoEmp = LabelFrame(vent_ppal, text="Empalme", relief='solid', borderwidth=1, )
frm_infoEmp.grid(row=0, column=0, padx=[10,10], pady=[15, 10], ipady=10, sticky="N", )

# label and entry Id del empalme
lbl_idemp = Label(frm_infoEmp, text="ID EMPALME:").grid(row=0, column=0, padx=[10,0], sticky="w")
ent_idEmpalme = Entry(frm_infoEmp, justify='left')
ent_idEmpalme.grid(row=0, column=1, padx=[0, 10], sticky="w" )
ent_idEmpalme.configure(width=10)
ent_idEmpalme.focus()

# Crear Validador para el widget Entry de ID de empalme
registro_idEmp = (vent_ppal.register(lambda texto: validar_numero(texto, prefEmpalme, ent_nombreEmpalme)), '%P') # %P representa el nuevo valor
ent_idEmpalme.config(validate='key', validatecommand=registro_idEmp)    # Configurar el Entry de ID con el validador

ent_idEmpalme.bind("<KeyRelease>", lambda e: deshab_btn_agregarCable())

# label and entry Nombre del empalme
lbl_nombreEmpalme = Label(frm_infoEmp, text="NOMBRE:", anchor='w' ).grid(row=0, column=2, padx=[10, 5], sticky="e")
ent_nombreEmpalme = Entry(frm_infoEmp, justify='left')
ent_nombreEmpalme.grid(row=0, column=3, padx=[5, 10], sticky="w" )
ent_nombreEmpalme.configure(width=15, state='readonly')

# boton buscar empalme
btn_buscarEmpalme = Button(frm_infoEmp, text="Buscar", image=img_boton, )
btn_buscarEmpalme.grid(row=0, column=4, padx=[10,10], sticky='e' )
btn_buscarEmpalme.config(command=buscar_empalme)            # Asociar la función al botón

# Referencia caja de empalme
lbl_ref = Label(frm_infoEmp, text="CIERRE:", anchor='e', ).grid(row=1, column=0, padx=[10,0], sticky="w" )
ent_ref = Entry(frm_infoEmp, justify='left')
ent_ref.grid(row=1, column=1, padx=[0, 10], sticky="w")
ent_ref.configure(width=10)

# Descripcion del empalme
lbl_descrEmpalme = Label(frm_infoEmp, text="DESCRIPCION:", ).grid(row=1, column=2, padx=[10,5], sticky="e")
ent_descrEmpalme = Entry(frm_infoEmp, justify='left')
ent_descrEmpalme.grid(row=1, column=3, padx=[5, 10], columnspan=2, sticky="we" )
ent_descrEmpalme.configure(width=5)

# Botón para activar la función de agregar fila
btn_agregarCable = Button(frm_infoEmp, text="Agregar Cable", state='disabled')
btn_agregarCable.grid(row=2, column=0, padx=[10,0], pady=[10, 0], sticky='w' )
btn_agregarCable.configure(command=agregar_cable)

# Botón Limpiar campos de entrada
btn_borrarCamposEmpalme = Button(frm_infoEmp, text="Borrar Campos")
btn_borrarCamposEmpalme.grid(row=2, column=1, columnspan=2, padx=[10,10], pady=[10, 0] )
btn_borrarCamposEmpalme.configure(command=limpiar_campos_empalme)

# tabla listado de cables en caja de empalme
tbl_cables = ttk.Treeview(frm_infoEmp, columns=("etiqueta", "hilos", 
                                               "tipoCable", "fabricante", "sangria", "puerto"), )

tbl_cables.grid(row=4, column=0, columnspan=5, padx=10, pady=[10, 0], sticky='we')

tbl_cables.column("#0", width=70, minwidth=60, stretch=False)
tbl_cables.column("etiqueta", width=120, minwidth=70)
tbl_cables.column("hilos", width=50, minwidth=30, stretch=False)
tbl_cables.column("tipoCable", width=70, minwidth=50, stretch=False)
tbl_cables.column("fabricante", width=70, minwidth=50, stretch=False)
tbl_cables.column("sangria", width=50, minwidth=30, stretch=False)
tbl_cables.column("puerto", width=100, minwidth=45, stretch=False,)

tbl_cables.heading("#0", text="Id Cable", anchor="w", )
tbl_cables.heading("etiqueta", text="Etiqueta", anchor="w", )
tbl_cables.heading("hilos", text="Hilos", anchor="w", )
tbl_cables.heading("tipoCable", text="Tipo Cable", anchor="w", )
tbl_cables.heading("fabricante", text="Fabricante", anchor="w", )
tbl_cables.heading("sangria", text="Sangria", anchor="w", )
tbl_cables.heading("puerto", text="Puerto", anchor='w', )

# Asociar la función al evento de selección
tbl_cables.bind("<Double-1>", editar_cable)


# frame informacion del punto de apoyo al empalme
frm_PuntoApoyo = LabelFrame(vent_ppal, text="Punto de Apoyo", relief='solid', borderwidth=1,)
frm_PuntoApoyo.grid(row=0, column=1, padx=[10, 10], pady=[15, 10], ipady=10, sticky="nsew",)

# Entrada para el ID PUNTO DE APOYO (camara, poste o cuarto tecnico)
Label(frm_PuntoApoyo, text="ID PUNTO APOYO:", ).grid(row=0, column=0, padx=10, sticky="w")
ent_idApoyo = Entry(frm_PuntoApoyo, justify='left')
ent_idApoyo.grid(row=0, column=1, padx=[5, 10], sticky="w")
ent_idApoyo.configure(width=10, )

# Validador para el Entry de ID de apoyo
registro_idApoyo = (vent_ppal.register(lambda texto: validar_numero(texto, prefCamara, ent_nombreApoyo)), '%P')   # %P representa el nuevo valor
ent_idApoyo.config(validate='key', validatecommand=registro_idApoyo)    # Configurar el Entry de ID con el validador

ent_idApoyo.bind("<KeyRelease>", lambda e: deshab_btn_agregarEmpalme())

# label and entry Nombre del Punto de Apoyo en OSP
lbl_nombreApoyo = Label(frm_PuntoApoyo, text="NOMBRE:", ).grid(row=0, column=2, sticky="e")
ent_nombreApoyo = Entry(frm_PuntoApoyo, justify='left')
ent_nombreApoyo.grid(row=0, column=3, padx=[5, 10], sticky="w" )
ent_nombreApoyo.configure(width=15, state='readonly')

# boton buscar punto de apoyo
btn_buscarPntApoyo = Button(frm_PuntoApoyo, text="Buscar", image=img_boton )
btn_buscarPntApoyo.grid(row=0, column=4, padx=[5,10], sticky='e')
btn_buscarPntApoyo.config(command=buscar_apoyo)

# Direccion de punto de apoyo (camara o poste)
lbl_dir = Label(frm_PuntoApoyo, text="DIRECCION:", ).grid(row=1, column=0, padx=10, sticky="w")
ent_dir = Entry(frm_PuntoApoyo, justify='left')
ent_dir.grid(row=1, column=1, padx=[5, 10])
ent_dir.configure(width=20)

# Tipo de punto de apoyo
lbl_tipoApoyo = Label(frm_PuntoApoyo, text="TIPO APOYO:", ).grid(row=1, column=2, sticky="e" )
ent_tipoApoyo = Entry(frm_PuntoApoyo, justify='left')
ent_tipoApoyo.grid(row=1, column=3, padx=[5, 10], sticky="w")
ent_tipoApoyo.configure(width=12)

# Coordenadas de punto de apoyo (camara o poste)
lbl_coord = Label(frm_PuntoApoyo, text="COORDENADAS:", ).grid(row=2, column=0, columnspan=2, padx=10, sticky="w")
ent_coord = Entry(frm_PuntoApoyo, justify='left')
ent_coord.grid(row=2, column=1, padx=[5, 10])
ent_coord.configure(width=20)

# Botón agregar Empalme en Punto de Apoyo
btn_agregarEmpalme = Button(frm_PuntoApoyo, text="Agregar Empalme", state='disabled')
btn_agregarEmpalme.grid(row=3, column=0, padx=[10,10], pady=[10, 0], sticky='w')
btn_agregarEmpalme.configure(command=agregar_empalme,)

# Botón Limpiar campos del Punto de Apoyo
btn_borrarCamposApoyo = Button(frm_PuntoApoyo, text="Borrar Campos")
btn_borrarCamposApoyo.grid(row=3, column=1, padx=[10,20], pady=[10, 0], sticky='we')
btn_borrarCamposApoyo.configure(command=limpiar_campos_apoyo)

# Botón agregar nuevo Punto de Apoyo
btn_crearApoyo = Button(frm_PuntoApoyo, text="Crear Punto De Apoyo")
btn_crearApoyo.grid(row=3, column=2, padx=[10,10], pady=[10, 0], columnspan=2, sticky='w')
btn_crearApoyo.config(command=crear_apoyo)

# tabla - Enumercion de cajas de Empalmes en Punto de Apoyo
tbl_empalmes = ttk.Treeview(frm_PuntoApoyo, columns=("nombreEmpalme", "cierre", "descripcion"),height=5)
tbl_empalmes.grid(row=4, column=0, columnspan=5, padx=10, pady=[10, 0], sticky="NSEW" )
tbl_empalmes.column("#0", width=75, minwidth=40, stretch=False)
tbl_empalmes.column("nombreEmpalme", width=75, minwidth=40, stretch=False)
tbl_empalmes.column("cierre", width=60, minwidth=40, stretch=False)
tbl_empalmes.column("descripcion", width=120, minwidth=70)

tbl_empalmes.heading("#0", text="Id Empalme", anchor="w", )
tbl_empalmes.heading("nombreEmpalme", text="Nombre", anchor="w", )
tbl_empalmes.heading("cierre", text="Cierre", anchor="w", )
tbl_empalmes.heading("descripcion", text="Descripcion", anchor="w", )

# Asociar la función al evento de selección
tbl_empalmes.bind("<Double-1>", leer_empalme)



vent_ppal.mainloop()