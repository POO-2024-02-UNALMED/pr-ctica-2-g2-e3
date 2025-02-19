from gestorAplicacion.servicios.Cita import Cita  # Import the base class Cita

class CitaVacuna(Cita):
    def __init__(self, fecha: str, paciente, vacuna):
        super().__init__(None, fecha, paciente)
        self.vacuna = vacuna

    def get_fecha(self):
        return self.fecha

    def validar_pago(self, paciente, id_servicio: int):
        for cita_vacuna in paciente.get_historia_clinica().get_historial_vacunas():
            if cita_vacuna.get_id_servicio() == id_servicio:
                cita_vacuna.set_estado_pago(True)

    def descripcion_servicio(self) -> str:
        return f"{self.idServicio} - Vacuna {self.vacuna.get_nombre()} ({self.fecha})"

    def mensaje(self) -> str:
        return "del servicio de vacunas!"

    def get_vacuna(self):
        return self.vacuna

    def set_vacuna(self, vacuna):
        self.vacuna = vacuna