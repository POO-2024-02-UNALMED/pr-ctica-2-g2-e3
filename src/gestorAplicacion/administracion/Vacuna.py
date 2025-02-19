from gestorAplicacion.servicios.CitaVacuna import CitaVacuna

class Vacuna:
    def __init__(self, tipo: str, nombre: str, tipo_eps: list, precio: float):
        self.tipo = tipo
        self.nombre = nombre
        self.tipo_eps = tipo_eps
        self.precio = precio
        self.agenda = [
            CitaVacuna("3 de Marzo, 8:00 am", None, self),
            CitaVacuna("3 de Marzo, 11:00 am", None, self),
            CitaVacuna("4 de Marzo, 3:00 pm", None, self),
            CitaVacuna("5 de Marzo, 10:00 am", None, self)
        ]
    
    def mostrar_agenda_disponible(self):
        # Se accede directamente al atributo 'paciente' en lugar de llamar a get_paciente()
        return [cita for cita in self.agenda if cita.paciente is None]
    
    def actualizar_agenda(self, paciente_asignado, numero_cita: int, agenda_disponible: list):
        cita_asignada = None
        for cita in self.agenda:
            if cita.get_fecha() == agenda_disponible[numero_cita - 1].get_fecha():
                cita.paciente = paciente_asignado
                cita_asignada = cita
        return cita_asignada
    
    @property
    def get_tipo(self):
        return self.tipo
    
    @property
    def get_tipo_eps(self):
        return self.tipo_eps
    
    @property
    def get_nombre(self):
        return self.nombre
    
    @property
    def get_precio(self):
        return self.precio
    
    @property
    def get_agenda(self):
        return self.agenda