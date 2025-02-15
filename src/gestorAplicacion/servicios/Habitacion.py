from gestorAplicacion.administracion import CategoriaHabitacion
from gestorAplicacion.servicios.Servicio import Servicio

class Habitacion(Servicio):
    def __init__(
        self, 
        numero: int, 
        categoria: CategoriaHabitacion, 
        ocupada: bool, 
        paciente: 'Paciente',  # Use string type hint
        dias: int
    ):
        super().__init__(paciente)
        self.numero = numero
        self.categoria = categoria
        self.ocupada = ocupada
        self.dias = dias

    @staticmethod
    def buscar_habitacion_disponible(categoria: CategoriaHabitacion):
        from gestorAplicacion.administracion.Hospital import Hospital  # Local import
        return [
            habitacion 
            for habitacion in Hospital.habitaciones 
            if habitacion.categoria == categoria and not habitacion.ocupada
        ]