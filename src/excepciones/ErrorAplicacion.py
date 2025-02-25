# src/ErrorAplicacion.py

class ErrorAplicacion(Exception):
    def __init__(self, mensaje: str):
        super().__init__(f"Manejo de errores de la Aplicación-> {mensaje}")


class ErrorRegistro(ErrorAplicacion):
    def __init__(self, mensaje: str):
        super().__init__(f"Error en la gestión de registros: {mensaje}")


class ErrorRegistroNoEncontrado(ErrorRegistro):
    def __init__(self, cedula: int):
        super().__init__(f"Paciente con cédula {cedula} no encontrado.")


class ErrorNoServiciosFacturables(ErrorRegistro):
    def __init__(self, cedula: int):
        super().__init__(f"Paciente con cédula {cedula} no tiene servicios facturables para la facturación.")


class ErrorRegistroDatosInvalidos(ErrorRegistro):
    def __init__(self, campo: str):
        super().__init__(f"Datos inválidos para el paciente en el campo: {campo}.")


# Excepción sugerida:
class ValueErrorRegistro(ErrorRegistro):
    def __init__(self, mensaje: str):
        super().__init__(f"Valor incorrecto para paciente: {mensaje}")


class ErrorPacienteNoEncontrado(ErrorRegistro):
    def __init__(self, cedula):
        self.cedula = cedula
        self.message = f"Paciente con cédula {cedula} no encontrado."
        super().__init__(self.message)


# ERRORENTRADA

class ErrorEntrada(ErrorAplicacion):
    def __init__(self, mensaje: str):
        super().__init__(f"Error en la entrada por teclado: {mensaje}")


class ErrorCampoVacio(ErrorEntrada):
    def __init__(self, campo: str):
        super().__init__()
        self.message = f"El campo {campo} no puede estar vacío."
        super().__init__(self.message)