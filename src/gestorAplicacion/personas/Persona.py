class Persona:
    def __init__(self, cedula: int, nombre: str, tipo_eps: str):
        # Asignar directamente al atributo interno para evitar usar el setter de la propiedad
        self._cedula = cedula
        self.nombre = nombre
        self.tipo_eps = tipo_eps

    @property
    def cedula(self):
        return self._cedula

    @cedula.setter
    def cedula(self, value):
        self._cedula = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def tipo_eps(self):
        return self._tipo_eps

    @tipo_eps.setter
    def tipo_eps(self, value):
        self._tipo_eps = value