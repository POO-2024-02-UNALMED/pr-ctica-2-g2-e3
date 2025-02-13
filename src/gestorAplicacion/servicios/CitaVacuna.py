from gestorAplicacion.servicios.Cita import Cita

class CitaVacuna(Cita):
    def __init__(self, fecha: str, paciente, vacuna):
        super().__init__(None, fecha, paciente)
        self.vacuna = vacuna

    def validar_pago(self, paciente, id_servicio: int):
        # Itera sobre el historial de vacunas del paciente y marca el pago como realizado si el id coincide.
        for cita_vacuna in paciente.get_historia_clinica().get_historial_vacunas():
            if cita_vacuna.get_id_servicio() == id_servicio:
                cita_vacuna.set_estado_pago(True)

    def descripcion_servicio(self) -> str:
        # Genera una descripción del servicio de vacuna.
        return f"{self.idServicio} - Vacuna {self.vacuna.get_nombre()} ({self.fecha})"

    def mensaje(self) -> str:
        return "del servicio de vacunas!"

    def get_vacuna(self):
        return self.vacuna

    def set_vacuna(self, vacuna):
        self.vacuna = vacuna