from abc import ABC, abstractmethod

class Pago(ABC):
    IVA = 0.19
    
    @abstractmethod
    def calcular_precio_cita(self, cita):
        pass
    
    @abstractmethod
    def calcular_precio_cita_vacuna(self, cita_vacuna):
        pass
    
    @abstractmethod
    def calcular_precio_formula(self, formula):
        pass
    
    @abstractmethod
    def calcular_precio_habitacion(self, habitacion):
        pass
