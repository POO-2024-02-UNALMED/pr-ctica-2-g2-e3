from abc import ABC, abstractmethod
from gestorAplicacion.personas.Paciente import Paciente  # Correct Paciente import

class Servicio(ABC):
    generadorID = 1000

    def __init__(self, paciente: Paciente):
        self.idServicio = Servicio.generadorID
        Servicio.generadorID += 1
        self.paciente = paciente
        self.estadoPago = False

    @abstractmethod
    def validarPago(self):  # No parameters (matches subclasses)
        pass