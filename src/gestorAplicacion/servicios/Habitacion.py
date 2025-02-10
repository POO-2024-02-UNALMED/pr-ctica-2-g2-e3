from gestorAplicacion.administracion import CategoriaHabitacion, Hospital
from gestorAplicacion.personas import Paciente
from gestorAplicacion.servicios.Servicio import Servicio

class Habitacion(Servicio):
    def __init__(self, numero: int, categoria: CategoriaHabitacion, ocupada: bool, paciente: Paciente, dias: int):
        super().__init__(paciente)
        self.numero = numero
        self.categoria = categoria
        self.ocupada = ocupada
        self.dias = dias

    @staticmethod
    def BuscarHabitacionDisponible(categoria: CategoriaHabitacion):
        # Filtra y retorna una lista de habitaciones vacías de la categoría seleccionada
        habitaciones_disponibles = []
        for habitacion in Hospital.habitaciones:
            if habitacion.categoria == categoria and not habitacion.ocupada:
                habitaciones_disponibles.append(habitacion)
        return habitaciones_disponibles