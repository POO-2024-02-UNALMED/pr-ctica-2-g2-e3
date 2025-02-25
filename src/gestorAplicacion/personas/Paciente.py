
from gestorAplicacion.personas.Persona import Persona
from gestorAplicacion.administracion.HistoriaClinica import HistoriaClinica
from gestorAplicacion.administracion.CategoriaHabitacion import CategoriaHabitacion
from gestorAplicacion.administracion.Medicamento import Medicamento
from gestorAplicacion.personas.Enfermedad import Enfermedad
from gestorAplicacion.personas.Doctor import Doctor
from gestorAplicacion.servicios.Habitacion import Habitacion

IVA = 0.19


class Paciente(Persona):
    def __init__(self, cedula: int, nombre: str, tipo_eps: str, categoria_habitacion: CategoriaHabitacion = None):
        super().__init__(cedula, nombre, tipo_eps)
        self.categoria_habitacion = categoria_habitacion
        self.habitacion_asignada = None
        self.historia_clinica = HistoriaClinica(self)
    
    def get_cedula(self):
        return self._cedula

    def med_enfermedad(self, enfermedad, hospital) -> list:
        """
        Retorna una lista de medicamentos disponibles para tratar la enfermedad dada.
        Se filtra la lista de medicamentos del hospital comparando el nombre (o tipología)
        de la enfermedad asociada al medicamento con la enfermedad proporcionada.
        """
        # Se filtra por medicamento que coincida con la enfermedad en nombre y tipología
        medicamentos = [
            med for med in hospital.lista_medicamentos
            if med.enfermedad.nombre == enfermedad.nombre and med.enfermedad.tipologia == enfermedad.tipologia
            and med.cantidad > 0  # opcional: solo los que hay en stock
        ]
        return medicamentos

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
        # Asegurarnos de que la fórmula tenga asignado el paciente
        if formula.paciente is None:
            formula.paciente = self

        # Si se asignó la lista de medicamentos usando un nombre erróneo,
        # se copia su valor a la propiedad correcta.
        if hasattr(formula, "lista_medicamentos"):
            formula.listaMedicamentos = formula.lista_medicamentos

        # Verificar que la lista de medicamentos sea del tipo list,
        # en caso contrario, inicializarla
        if not isinstance(formula.getListaMedicamentos(), list):
            formula.listaMedicamentos = []  # Re-inicializamos a lista vacía

        precio = 0
        for med in formula.getListaMedicamentos():
            if formula.paciente.tipo_eps == "Contributivo":
                precio += med.precio * 0.8
            elif formula.paciente.tipo_eps == "Subsidiado":
                precio += med.precio * 0.7
            elif formula.paciente.tipo_eps == "Particular":
                precio += med.precio
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
        # Nota: Se deben invocar correctamente los métodos get_vacuna para acceder a sus propiedades.
        # Es decir, usar paréntesis al llamar a get_vacuna().
        precio_total = cita_asignada.get_vacuna().get_precio  
        vacuna_tipo  = cita_asignada.get_vacuna().get_tipo  

        if vacuna_tipo.lower() == "obligatoria":
            precio_total += 1000
        elif vacuna_tipo.lower() == "no obligatoria":
            precio_total += 3000

        # Acceso directo al atributo 'paciente' de la cita
        tipo_eps = cita_asignada.paciente.tipo_eps  
        if tipo_eps == "Contributivo":
            precio_total += 2000
        elif tipo_eps == "Subsidiado":
            precio_total += 500
        elif tipo_eps == "Particular":
            precio_total += 10000

        IVA = 0.19
        return precio_total * (1 + IVA)

    def calcular_precio_habitacion(self, habitacion_asignada) -> float:
        # Se accede directamente al atributo 'tipo_eps' en lugar de llamar a un método inexistente.
        if self.tipo_eps == "Subsidiado":
            precio = habitacion_asignada.categoria.get_valor() * 0.3
        elif self.tipo_eps == "Contributivo":
            precio = (habitacion_asignada.categoria.get_valor() / 2) * habitacion_asignada.dias
        else:  # Particular
            precio = habitacion_asignada.categoria.get_valor() * habitacion_asignada.dias
        IVA = 0.19
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
        from gestorAplicacion.servicios.CitaVacuna import CitaVacuna
        if isinstance(cita_asignada, CitaVacuna):
            # Se utiliza el atributo 'historial_vacunas' directamente sin llamarlo como función.
            self.historia_clinica.historial_vacunas.append(cita_asignada)

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
        return (f"---------------------------\nNombre: {self.nombre}\n"
                f"Cédula: {self.cedula}\nTipo de EPS: {self.tipo_eps}\n"
                "---------------------------")

    def despedida(self, cita_asignada) -> str:
        return f"¡Adiós {self.get_nombre()} {cita_asignada.mensaje()}"