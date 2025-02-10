class Enfermedad:
    enfermedades_registradas = []

    def __init__(self, especialidad, nombre, tipologia):
        self.especialidad = especialidad
        self.nombre = nombre
        self.tipologia = tipologia
        self.enfermos = 1
        Enfermedad.enfermedades_registradas.append(self)

    def nuevo_enfermo(self):
        self.enfermos += 1

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, value):
        self._especialidad = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def tipologia(self):
        return self._tipologia

    @tipologia.setter
    def tipologia(self, value):
        self._tipologia = value

    @property
    def enfermos(self):
        return self._enfermos

    @enfermos.setter
    def enfermos(self, value):
        self._enfermos = value

    @staticmethod
    def get_enfermedades_registradas():
        return Enfermedad.enfermedades_registradas