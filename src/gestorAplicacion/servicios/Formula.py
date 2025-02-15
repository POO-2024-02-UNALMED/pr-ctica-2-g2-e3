from gestorAplicacion.administracion import Medicamento
from gestorAplicacion.servicios.Servicio import Servicio

class Formula(Servicio):
    def __init__(self, listaMedicamentos: list = None, doctor: 'Doctor' = None, paciente: 'Paciente' = None):  # String type hints
        super().__init__(paciente)
        self.listaMedicamentos = listaMedicamentos if listaMedicamentos is not None else []
        self.doctor = doctor

    def getListaMedicamentos(self) -> list:
        return self.listaMedicamentos