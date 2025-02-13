
#autores: Samuel Botero Rivera, Santiago Sanchez Ruiz, Samuel Gutierrez Betancur, Samuel Garcia Rojas

from gestorAplicacion.personas.Doctor import Doctor  # Correct Doctor import
from gestorAplicacion.personas.Paciente import Paciente  # Correct Paciente import
from gestorAplicacion.servicios.Servicio import Servicio  # Correct Servicio import

class Cita(Servicio):
    def __init__(self, doctor: Doctor, fecha: str, paciente: Paciente):
        super().__init__(paciente)
        self.doctor = doctor
        self.fecha = fecha

    # Fix method signature to match Servicio's abstract method
    def validarPago(self):  # Remove redundant parameters
        # Example implementation:
        if self.paciente.eps == "Subsidiado":
            self.estadoPago = True
        return self.estadoPago