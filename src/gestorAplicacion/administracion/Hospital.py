from typing import List
from gestorAplicacion.servicios.Habitacion import Habitacion  # Import Habitacion
from gestorAplicacion.personas.Doctor import Doctor  # Import Doctor
from gestorAplicacion.personas.Paciente import Paciente  # Import Paciente
from gestorAplicacion.administracion.Medicamento import Medicamento  # Import Medicamento
from gestorAplicacion.administracion.Vacuna import Vacuna  # Import Vacuna
from gestorAplicacion.administracion.Deserializador import Deserializador  # Import Deserializador

class Hospital:
    habitaciones: List[Habitacion] = []  # Now Habitacion is defined

    def __init__(self):
        self.lista_doctores: List[Doctor] = []
        self.lista_pacientes: List[Paciente] = []
        self.lista_medicamentos: List[Medicamento] = []
        self.lista_vacunas: List[Vacuna] = []
        Deserializador.deserializar(self)  # Deserializador is now imported

    # Methods remain unchanged (e.g., buscar_tipo_doctor, buscar_paciente, etc.)

    # Fix property names (remove "get_" prefix for Python conventions)
    @property
    def lista_doctores(self) -> List[Doctor]:
        return self._lista_doctores

    @lista_doctores.setter
    def lista_doctores(self, value: List[Doctor]):
        self._lista_doctores = value

    # Repeat for other properties (lista_pacientes, lista_medicamentos, lista_vacunas)
    # ...

    @classmethod
    def get_habitaciones(cls) -> List[Habitacion]:
        return cls.habitaciones

    @classmethod
    def set_habitaciones(cls, habitaciones: List[Habitacion]):
        cls.habitaciones = habitaciones