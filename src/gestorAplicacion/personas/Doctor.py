from gestorAplicacion.personas.Persona import Persona  # Correct import for Persona

class Doctor(Persona):
    def __init__(self, cedula: int, nombre: str, tipo_eps: str, especialidad: str):
        super().__init__(cedula, nombre, tipo_eps)
        self.especialidad = especialidad
        self.agenda = [
            self._crear_cita("3 de Abril, 8:00 am", None),  # Use a helper method
            self._crear_cita("4 de Abril, 3:00 pm", None),
            self._crear_cita("5 de Abril, 10:00 am", None)
        ]

    def _crear_cita(self, fecha: str, paciente):
        # Import Cita locally to avoid circular dependency
        from gestorAplicacion.servicios.Cita import Cita
        return Cita(self, fecha, paciente)

    def actualizar_agenda(self, paciente_asignado, numero_cita, agenda_disponible):
        cita_asignada = None
        for i in range(1, len(self.agenda) + 1):
            if self.agenda[i-1].fecha == agenda_disponible[numero_cita-1].fecha:
                self.agenda[i-1].paciente = paciente_asignado
                cita_asignada = self.agenda[i-1]
        return cita_asignada

    # Python properties don't need "get_" prefixes. Rename for consistency:

    @property
    def cedula(self):
        return self._cedula

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, value: str):
        self._especialidad = value

    @property
    def agenda(self) -> list:
        return self._agenda

    @agenda.setter
    def agenda(self, value: list):
        self._agenda = value