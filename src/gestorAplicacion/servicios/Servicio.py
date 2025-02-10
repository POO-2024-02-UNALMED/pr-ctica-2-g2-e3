from abc import ABC, abstractmethod
from gestorAplicacion.personas import Paciente

# Clase Abstracta destinada a herencia de servicios del hospital
class Servicio(ABC):
    generadorID = 1000

    # Constructor
    def __init__(self, paciente: Paciente):
        self.idServicio = Servicio.generadorID
        Servicio.generadorID += 1
        self.paciente = paciente
        self.estadoPago = False

    # Método abstracto que debe implementarse en las clases hijas para validar el pago
    @abstractmethod
    def validarPago(self, paciente: Paciente, idServicio: int):
        pass