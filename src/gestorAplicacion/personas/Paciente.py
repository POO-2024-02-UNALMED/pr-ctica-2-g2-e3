from gestorAplicacion.personas.Persona import Persona
from gestorAplicacion.administracion.HistoriaClinica import HistoriaClinica
from gestorAplicacion.administracion.CategoriaHabitacion import CategoriaHabitacion
from gestorAplicacion.administracion.Medicamento import Medicamento
from gestorAplicacion.personas.Enfermedad import Enfermedad
from gestorAplicacion.personas.Doctor import Doctor
from gestorAplicacion.servicios.Habitacion import Habitacion
from gestorAplicacion.administracion.Vacuna import Vacuna

IVA = 0.19


class Paciente(Persona):
    def __init__(self, cedula: int, nombre: str, tipo_eps: str, categoria_habitacion: CategoriaHabitacion = None):
        super().__init__(cedula, nombre, tipo_eps)
        self.categoria_habitacion = categoria_habitacion
        self.habitacion_asignada = None
        self.historia_clinica = HistoriaClinica(self)
    
    def med_enfermedad(self, enfermedad, hospital) -> list:
        medicamentos = hospital.medicamentos_disponibles()
        med_enfermedades = []
        for med in medicamentos:
            if (enfermedad.get_nombre() == med.get_enfermedad().get_nombre() and
                enfermedad.get_tipologia() == med.get_enfermedad().get_tipologia()):
                med_enfermedades.append(med)
        return med_enfermedades

    def buscar_doctor_eps(self, especialidad: str, hospital) -> list:
        doctores_por_especialidad = hospital.buscar_tipo_doctor(especialidad)
        doctores_disponibles = []
        for doc in doctores_por_especialidad:
            if doc.get_tipo_eps() == self.get_tipo_eps():
                doctores_disponibles.append(doc)
        return doctores_disponibles

    def actualizar_historial_citas(self, cita_asignada):
        self.historia_clinica.get_historial_citas().append(cita_asignada)

    def calcular_precio_formula(self, formula) -> float:
        from gestorAplicacion.servicios.Formula import Formula  # Local import
        precio = 0
        for med in formula.get_lista_medicamentos():
            if formula.get_paciente().get_tipo_eps() == "Contributivo":
                precio += med.get_precio() * 0.8
            elif formula.get_paciente().get_tipo_eps() == "Subsidiado":
                precio += med.get_precio() * 0.7
            elif formula.get_paciente().get_tipo_eps() == "Particular":
                precio += med.get_precio()
        return precio * (1 + IVA)

    def calcular_precio_cita(self, cita_asignada) -> float:
        precio_total = 0
        especialidad = cita_asignada.get_doctor().get_especialidad()
        if especialidad == "General":
            precio_total += 5000
        elif especialidad == "Oftalmologia":
            precio_total += 7000
        elif especialidad == "Odontologia":
            precio_total += 10000

        tipo_eps = cita_asignada.get_paciente().get_tipo_eps()
        if tipo_eps == "Contributivo":
            precio_total += 2000
        elif tipo_eps == "Subsidiado":
            precio_total += 500
        elif tipo_eps == "Particular":
            precio_total += 10000

        return precio_total * (1 + IVA)

    def calcular_precio_cita_vacuna(self, cita_asignada) -> float:
        # Import CitaVacuna locally to avoid circular dependency
        from gestorAplicacion.servicios.CitaVacuna import CitaVacuna
        if isinstance(cita_asignada, CitaVacuna):
            precio_total = cita_asignada.get_vacuna().get_precio()
            vacuna_tipo = cita_asignada.get_vacuna().get_tipo()
            if vacuna_tipo == "Obligatoria":
                precio_total += 1000
            elif vacuna_tipo == "No obligatoria":
                precio_total += 3000

            tipo_eps = cita_asignada.get_paciente().get_tipo_eps()
            if tipo_eps == "Contributivo":
                precio_total += 2000
            elif tipo_eps == "Subsidiado":
                precio_total += 500
            elif tipo_eps == "Particular":
                precio_total += 10000

            return precio_total * (1 + IVA)
        return 0.0

    def calcular_precio_habitacion(self, habitacion_asignada) -> float:
        precio = 0
        if self.get_tipo_eps() == "Subsidiado":
            precio = habitacion_asignada.get_categoria().get_valor() * 0
        elif self.get_tipo_eps() == "Contributivo":
            precio = (habitacion_asignada.get_categoria().get_valor() / 2) * habitacion_asignada.get_dias()
        else:  # Particular
            precio = habitacion_asignada.get_categoria().get_valor() * habitacion_asignada.get_dias()
        return precio * (1 + IVA)

    def buscar_vacuna_por_eps(self, tipo: str, hospital) -> list:
        vacunas_por_tipo = hospital.buscar_tipo_vacuna(tipo)
        vacunas_disponibles = []
        for vacuna in vacunas_por_tipo:
            for eps in vacuna.get_tipo_eps():
                if eps == self.get_tipo_eps():
                    vacunas_disponibles.append(vacuna)
                    break
        return vacunas_disponibles

    def mensaje_doctor(self, doctor) -> str:
        return f"{doctor.bienvenida()}\nPor favor selecciona los medicamentos que vas a formularle a: {self.get_nombre()}"

    def actualizar_historial_vacunas(self, cita_asignada):
        # Import CitaVacuna locally to avoid circular dependency
        from gestorAplicacion.servicios.CitaVacuna import CitaVacuna
        if isinstance(cita_asignada, CitaVacuna):
            self.historia_clinica.get_historial_vacunas().append(cita_asignada)

    # Getters and setters
    def get_historia_clinica(self):
        return self.historia_clinica

    def get_categoria_habitacion(self):
        return self.categoria_habitacion

    def set_categoria_habitacion(self, categoria_habitacion: CategoriaHabitacion):
        self.categoria_habitacion = categoria_habitacion

    def get_habitacion_asignada(self):
        return self.habitacion_asignada

    def set_habitacion_asignada(self, habitacion_asignada):
        self.habitacion_asignada = habitacion_asignada

    def __str__(self):
        return (f"---------------------------\nNombre: {self.get_nombre()}\n"
                f"Cédula: {self.get_cedula()}\nTipo de EPS: {self.get_tipo_eps()}\n"
                "---------------------------")

    def despedida(self, cita_asignada) -> str:
        return f"¡Adiós {self.get_nombre()} {cita_asignada.mensaje()}"