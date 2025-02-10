"""
Clase que crea las formulas que se han generado para un paciente.
Autores: Samuel Botero Rivera, Santiago Sanchez Ruiz, Samuel Gutierrez Betancur, Samuel Garcia Rojas
"""

from gestorAplicacion.administracion import Medicamento
from gestorAplicacion.personas import Doctor, Paciente
from gestorAplicacion.servicios.Servicio import Servicio

class Formula(Servicio):
    def __init__(self, listaMedicamentos: list = None, doctor: Doctor = None, paciente: Paciente = None):
        super().__init__(paciente)
        self.listaMedicamentos = listaMedicamentos if listaMedicamentos is not None else []
        self.doctor = doctor

    def getListaMedicamentos(self) -> list:
        return self.listaMedicamentos