from gestorAplicacion.administracion import Medicamento
from gestorAplicacion.servicios.Servicio import Servicio

class Formula(Servicio):
    def __init__(self, listaMedicamentos: list = None, doctor: 'Doctor' = None, paciente: 'Paciente' = None):
        super().__init__(paciente)
        self.listaMedicamentos = listaMedicamentos if listaMedicamentos is not None else []
        self.doctor = doctor

    def getListaMedicamentos(self) -> list:
        return self.listaMedicamentos

    # Implementar el método abstracto que faltaba
    def validarPago(self):
        # Aquí se puede implementar la lógica de validación. Por ejemplo, retornamos True.
        return True

    def __str__(self):
        med_str = ", ".join([med.nombre for med in self.listaMedicamentos]) if self.listaMedicamentos else "Sin medicamentos"
        paciente_nombre = self.paciente.nombre if self.paciente else "N/A"
        doctor_nombre = self.doctor.nombre if self.doctor else "N/A"
        return f"Fórmula para {paciente_nombre}, Doctor: {doctor_nombre}, Medicamentos: {med_str}"