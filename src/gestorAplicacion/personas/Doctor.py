from persona import Persona
from servicios.cita import Cita

class Doctor(Persona):
    def __init__(self, cedula, nombre, tipo_eps, especialidad):
        super().__init__(cedula, nombre, tipo_eps)
        self.especialidad = especialidad
        self.agenda = [
            Cita(self, "3 de Abril, 8:00 am", None),
            Cita(self, "4 de Abril, 3:00 pm", None),
            Cita(self, "5 de Abril, 10:00 am", None)
        ]

    def actualizar_agenda(self, paciente_asignado, numero_cita, agenda_disponible):
        cita_asignada = None
        for i in range(1, len(self.agenda) + 1):
            if self.agenda[i-1].fecha == agenda_disponible[numero_cita-1].fecha:
                self.agenda[i-1].paciente = paciente_asignado
                cita_asignada = self.agenda[i-1]
        return cita_asignada

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, value):
        self._especialidad = value

    @property
    def agenda(self):
        return self._agenda

    @agenda.setter
    def agenda(self, value):
        self._agenda = value