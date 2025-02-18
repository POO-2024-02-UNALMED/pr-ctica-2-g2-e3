from typing import List
from gestorAplicacion.servicios.Habitacion import Habitacion  # Import Habitacion
from gestorAplicacion.personas.Doctor import Doctor  # Import Doctor
from gestorAplicacion.personas.Paciente import Paciente  # Import Paciente
from gestorAplicacion.administracion.Medicamento import Medicamento  # Import Medicamento
from gestorAplicacion.administracion.Vacuna import Vacuna  # Import Vacuna

class Hospital:
    habitaciones: List[Habitacion] = []  # Now Habitacion is defined

    def __init__(self):
        self.lista_doctores: List[Doctor] = []
        self.lista_pacientes: List[Paciente] = []
        self.lista_medicamentos: List[Medicamento] = []
        self.lista_vacunas: List[Vacuna] = []

    def agregar_doctor(self, doctor: Doctor):
        """Agrega un doctor a la lista de doctores del hospital"""
        self.lista_doctores.append(doctor)

    def buscar_doctor(self, cedula: int) -> Doctor:
        """Busca un doctor por cédula en la lista de doctores"""
        for doctor in self.lista_doctores:
            if doctor.cedula == cedula:
                return doctor

    def buscarPaciente(self, cedula: int) -> Paciente:
        """
        Busca un paciente en la lista de pacientes del hospital por su cédula.
        Retorna el paciente si lo encuentra, o None si no lo encuentra.
        """
        for paciente in self.lista_pacientes:
            if paciente.get_cedula() == cedula:
                return paciente
        return None

    # ... (rest of the class remains unchanged) ...
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