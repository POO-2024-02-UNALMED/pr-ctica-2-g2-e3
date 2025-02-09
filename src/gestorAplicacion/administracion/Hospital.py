from typing import List

class Hospital:
    habitaciones: List[Habitacion] = []

    def __init__(self):
        self.lista_doctores: List[Doctor] = []
        self.lista_pacientes: List[Paciente] = []
        self.lista_medicamentos: List[Medicamento] = []
        self.lista_vacunas: List[Vacuna] = []
        Deserializador.deserializar(self)
    
    def buscar_tipo_doctor(self, especialidad: str) -> List[Doctor]:
        return [doctor for doctor in self.lista_doctores if doctor.get_especialidad() == especialidad]
    
    def buscar_paciente(self, cedula_paciente: int) -> Paciente:
        return next((paciente for paciente in self.lista_pacientes if paciente.get_cedula() == cedula_paciente), None)
    
    def buscar_doctor(self, cedula_doctor: int) -> Doctor:
        return next((doctor for doctor in self.lista_doctores if doctor.get_cedula() == cedula_doctor), None)
    
    def buscar_vacuna(self, nombre: str) -> Vacuna:
        return next((vacuna for vacuna in self.lista_vacunas if vacuna.get_nombre() == nombre), None)
    
    def medicamentos_disponibles(self) -> List[Medicamento]:
        return [medicamento for medicamento in self.lista_medicamentos if medicamento.get_cantidad() > 0]
    
    def buscar_tipo_vacuna(self, tipo: str) -> List[Vacuna]:
        return [vacuna for vacuna in self.lista_vacunas if vacuna.get_tipo() == tipo]
    
    @property
    def get_lista_doctores(self) -> List[Doctor]:
        return self.lista_doctores
    
    @get_lista_doctores.setter
    def set_lista_doctores(self, lista_doctores: List[Doctor]):
        self.lista_doctores = lista_doctores
    
    @property
    def get_lista_pacientes(self) -> List[Paciente]:
        return self.lista_pacientes
    
    @get_lista_pacientes.setter
    def set_lista_pacientes(self, lista_pacientes: List[Paciente]):
        self.lista_pacientes = lista_pacientes
    
    @property
    def get_lista_medicamentos(self) -> List[Medicamento]:
        return self.lista_medicamentos
    
    @get_lista_medicamentos.setter
    def set_lista_medicamentos(self, lista_medicamentos: List[Medicamento]):
        self.lista_medicamentos = lista_medicamentos
    
    @property
    def get_lista_vacunas(self) -> List[Vacuna]:
        return self.lista_vacunas
    
    @get_lista_vacunas.setter
    def set_lista_vacunas(self, lista_vacunas: List[Vacuna]):
        self.lista_vacunas = lista_vacunas
    
    @classmethod
    def get_habitaciones(cls) -> List[Habitacion]:
        return cls.habitaciones
    
    @classmethod
    def set_habitaciones(cls, habitaciones: List[Habitacion]):
        cls.habitaciones = habitaciones
