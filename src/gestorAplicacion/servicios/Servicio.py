from abc import ABC, abstractmethod

class Servicio(ABC):
    generadorID = 1000

    def __init__(self, paciente: 'Paciente'):  # Use string type hint for Paciente
        self.idServicio = Servicio.generadorID
        Servicio.generadorID += 1
        self.paciente = paciente
        self.estadoPago = False

    @abstractmethod
    def validarPago(self):
        pass