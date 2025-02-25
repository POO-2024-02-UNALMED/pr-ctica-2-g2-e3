# src/ErrorAplicacion.py

# src/ErrorAplicacion.py

class ErrorAplicacion(Exception):
    def __init__(self, mensaje: str):
        super().__init__(f"Manejo de errores de la Aplicación-> {mensaje}")




class ErrorPaciente(ErrorAplicacion):
    def __init__(self, mensaje: str):
        super().__init__(f"Error en la gestión de pacientes: {mensaje}")

class ErrorPacienteNoEncontrado(ErrorPaciente):
    def __init__(self, cedula: int):
        super().__init__(f"Paciente con cédula {cedula} no encontrado.")

class ErrorPacienteDatosInvalidos(ErrorPaciente):
    def __init__(self, campo: str):
        super().__init__(f"Datos inválidos para el paciente en el campo: {campo}.")

# Excepción sugerida:
class ValueErrorPaciente(ErrorPaciente):
    def __init__(self, mensaje: str):
        super().__init__(f"Valor incorrecto para paciente: {mensaje}")




# src/ErrorAplicacion.py

class ErrorCita(ErrorAplicacion):
    pass

class ErrorCitaNoDisponible(ErrorCita):
    def __init__(self, fecha: str):
        super().__init__(f"La cita para la fecha {fecha} no está disponible.")

class ErrorCitaYaAsignada(ErrorCita):
    def __init__(self, fecha: str):
        super().__init__(f"La cita para la fecha {fecha} ya ha sido asignada a otro paciente.")

# Excepción sugerida:
class IndexErrorCita(ErrorCita):
    def __init__(self, mensaje: str):
        super().__init__(f"Índice fuera de rango: {mensaje}")
