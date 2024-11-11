from typing import overload

prefEmpalme = 'FOC-'
prefCamara = 'AP-'
prefPoste = 'POL-'

class PuntoApoyo ():
    @overload
    def __init__(self, id, tipoApoyo, ubicacion, ) -> None:
        self.id=id
        self.tipoApoyo=tipoApoyo
        self.ubicacion=ubicacion
    @overload
    def __init__(self, tipoApoyo, ubicacion, ) -> None:
        self.tipoApoyo=tipoApoyo
        self.ubicacion=ubicacion

    def get_id (self):
        return self.id

class EmpalmeFO (PuntoApoyo):
    @overload
    def __init__(self, id, nombre, ref, descripcion,) -> None:
        self.id=id
        self.nombre=nombre
        self.ref=ref
        self.descripcion=descripcion
        self.ap=PuntoApoyo
        
    @overload
    def __init__(self, ref, ubicacion, ap, nCables:int, ) -> None:
        self.ref=ref
        self.ubicacion=ubicacion
        self.ap=ap
        self.nCables=nCables

    # campos de la tabla (Tbl_Empalmes)
    campos = ["Id Empalme", "Nombre", "Cierre", "Descripcion"]
    entradas = []

class CableFO ():
    @overload
    def __init__(self, id:int, name, hilos:int, sangria:bool, ) -> None:
        self.id=id
        self.name=name
        self.hilos=hilos
        self.sangria=sangria
    @overload
    def __init__(self, id:int, hilos:int, sangria:bool, ) -> None:
        self.id=id        
        self.hilos=hilos
        self.sangria=sangria
    @overload
    def __init__(self, name, hilos:int, sangria:bool, ) -> None:
        self.name=name
        self.hilos=hilos
        self.sangria=sangria

class FusionFO ():
    def __init__(self, idEmpalme, cableA, cableB, hiloA:int, hiloB:int, ) -> None:
        self.idEmpalme=idEmpalme
        self.cableA=cableA
        self.cableB=cableB
        self.hiloA=hiloA
        self.hiloB=hiloB


