class Persona:
    def __init__(self, cedula: int, nombre: str, tipo_eps: str):
        # Asignar directamente al atributo interno para evitar usar el setter de la propiedad
        self._cedula = cedula
        self.nombre = nombre
        self.tipo_eps = tipo_eps

    def getCedula(self):
        return self._cedula

    def setCedula(self, value):
        self._cedula = value

    def getNombre(self):
        return self._nombre

    def setNnombre(self, value):
        self._nombre = value

    def getTipoEps(self):
        return self._tipo_eps

    def setTipoEps(self, value):
        self._tipo_eps = value