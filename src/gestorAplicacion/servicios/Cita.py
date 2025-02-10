"""
Autores: Samuel Botero Rivera, Santiago Sanchez Ruiz, Samuel Gutierrez Betancur, Samuel Garcia Rojas
"""

from gestorAplicacion.personas import Doctor, Paciente
from gestorAplicacion.servicios.servicio import Servicio  # Suponiendo que la clase Servicio esté definida en este módulo

# Clase destinada a crear citas médicas
class Cita(Servicio):
    # Constructor
    def __init__(self, doctor: Doctor, fecha: str, paciente: Paciente):
        super().__init__(paciente)
        self.doctor = doctor
        self.fecha = fecha

    # Método que busca el estado de pago de una cita médica y lo cambia
    def validarPago(self, paciente: Paciente, idServicio: int):
        for cita in paciente.getHistoriaClinica().getHistorialCitas():
            if cita.getIdServicio() == idServicio:
                cita.setEstadoPago(True)