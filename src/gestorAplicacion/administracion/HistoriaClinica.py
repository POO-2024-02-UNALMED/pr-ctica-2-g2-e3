from typing import List

class HistoriaClinica:
    def __init__(self, paciente):
        self.paciente = paciente
        self.lista_formulas: List[Formula] = []
        self.historial_citas: List[Cita] = []
        self.enfermedades: List[Enfermedad] = []
        self.historial_vacunas: List[CitaVacuna] = []
    
    def buscar_cita_doc(self, especialidad, hospital):
        doctores_disp = hospital.buscar_tipo_doctor(especialidad)
        doc_cita = [doc for doc in doctores_disp if any(doc.get_cedula() == cita.get_doctor().get_cedula() for cita in self.historial_citas)]
        return doc_cita
    
    def agregar_formula(self, formula_paciente):
        self.lista_formulas.append(formula_paciente)
    
    @property
    def get_paciente(self):
        return self.paciente
    
    @property
    def get_lista_formulas(self):
        return self.lista_formulas
    
    @get_lista_formulas.setter
    def set_lista_formulas(self, lista_formulas):
        self.lista_formulas = lista_formulas
    
    @property
    def get_historial_citas(self):
        return self.historial_citas
    
    @get_historial_citas.setter
    def set_historial_citas(self, historial_citas):
        self.historial_citas = historial_citas
    
    @property
    def get_enfermedades(self):
        return self.enfermedades
    
    @get_enfermedades.setter
    def set_enfermedades(self, enfermedades):
        self.enfermedades = enfermedades
    
    @property
    def get_historial_vacunas(self):
        return self.historial_vacunas
    
    @get_historial_vacunas.setter
    def set_historial_vacunas(self, historial_vacunas):
        self.historial_vacunas = historial_vacunas
