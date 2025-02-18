import sys
import os

# 1. Add the project root to sys.path FIRST
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 2. Now import other modules
from typing import List
from gestorAplicacion.administracion.Hospital import Hospital
from gestorAplicacion.administracion.CategoriaHabitacion import CategoriaHabitacion
from gestorAplicacion.administracion.HistoriaClinica import HistoriaClinica
from gestorAplicacion.administracion.Medicamento import Medicamento
from gestorAplicacion.administracion.Vacuna import Vacuna
from gestorAplicacion.personas.Doctor import Doctor
from gestorAplicacion.personas.Enfermedad import Enfermedad
from gestorAplicacion.personas.Paciente import Paciente
from gestorAplicacion.servicios.Cita import Cita
from gestorAplicacion.servicios.CitaVacuna import CitaVacuna
from gestorAplicacion.servicios.Formula import Formula
from gestorAplicacion.servicios.Habitacion import Habitacion  # Moved here
from gestorAplicacion.servicios.Servicio import Servicio

# Rest of your code remains unchanged
def mostrar_mensaje_bienvenida():
    print("Bienvenido al Sistema de registro hospitalario basado en objetos")

# ... (rest of your functions and main logic) ...

def mostrar_utilidad_programa():
    print("Utilidades del programa:")
    print("- Gestión de pacientes, doctores y medicamentos.")
    print("- Asignación de habitaciones en el hospital.")
    print("- Registro y manejo de citas médicas y de vacunación.")
    print("- Generación de facturas y control de pagos.")
    print("- Manejo de inventario de medicamentos y vacunas.")

def menu_inicial(hospital: Hospital):
    while True:
        print("\nMENU INICIAL")
        print("1. Servicios para pacientes")
        print("2. Gestionar registros")
        print("3. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            menu_funcionalidades(hospital)
        elif opcion == "2":
            menu_gestion(hospital)
        elif opcion == "3":
            # Aquí se podría serializar el hospital antes de salir.
            sys.exit(0)
        else:
            print("Opción inválida, intente de nuevo.")

def menu_funcionalidades(hospital: Hospital):
    while True:
        print("\nMENU FUNCIONALIDADES")
        print("1. Agendar una cita medica")
        print("2. Generar fórmula médica")
        print("3. Asignar habitación a un paciente")
        print("4. Aplicarse una vacuna")
        print("5. Facturacion")
        print("6. Regresar al menu inicial")
        print("7. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            agendar_citas(hospital)
        elif opcion == "2":
            formula_medica(hospital)
        elif opcion == "3":
            asignar_habitacion(hospital)
        elif opcion == "4":
            vacunacion(hospital)
        elif opcion == "5":
            facturacion(hospital)
        elif opcion == "6":
            break
        elif opcion == "7":
            sys.exit(0)
        else:
            print("Opción inválida, intente de nuevo.")

def menu_gestion(hospital: Hospital):
    while True:
        print("\nMENU GESTION")
        print("1. Gestionar Pacientes")
        print("2. Gestionar Vacunas")
        print("3. Gestionar Doctores")
        print("4. Gestionar Hospital")
        print("5. Regresar al menu inicial")
        print("6. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            menu_gestion_paciente(hospital)
        elif opcion == "2":
            menu_gestion_vacunas(hospital)
        elif opcion == "3":
            menu_gestion_doctor(hospital)
        elif opcion == "4":
            menu_gestion_hospital(hospital)
        elif opcion == "5":
            break
        elif opcion == "6":
            sys.exit(0)
        else:
            print("Opción inválida, intente de nuevo.")

def agendar_citas(hospital: Hospital):
    cedula = input("Ingrese su número de cédula: ")
    try:
        cedula = int(cedula)
    except ValueError:
        print("Entrada inválida.")
        return
    paciente = hospital.buscarPaciente(cedula)  # Asume método similar a Java
    if not paciente:
        print("Paciente no encontrado. Por favor regístrese.")
        return
    print(paciente.bienvenida() if hasattr(paciente, "bienvenida") else "Bienvenido, paciente.")

    doctores_disponibles = []
    while not doctores_disponibles:
        print("\nSeleccione el tipo de cita que requiere:")
        print("1. General")
        print("2. Odontologia")
        print("3. Oftalmologia")
        print("4. --Regresar al menú--")
        try:
            tipo_cita = int(input("Ingrese una opción: "))
        except ValueError:
            print("Opción inválida.")
            continue
        if tipo_cita not in [1, 2, 3, 4]:
            print("Opción inválida, intente de nuevo.")
            continue
        if tipo_cita == 4:
            return  # Regresa al menú
        # Simulación: supongamos que solo en 'General' hay doctores disponibles
        if tipo_cita == 1:
            doctores_disponibles = ["Doctor A", "Doctor B"]
        else:
            print("No hay doctores disponibles para la especialidad seleccionada.")
    
    agenda_disponible = []
    while not agenda_disponible:
        print("\nDoctores disponibles:")
        for idx, doc in enumerate(doctores_disponibles, start=1):
            print(f"{idx}. {doc}")
        print(f"{len(doctores_disponibles)+1}. --Regresar al menú--")
        try:
            numero_doctor = int(input("Seleccione el doctor con el que quiere la cita: "))
        except ValueError:
            print("Opción inválida.")
            continue
        if numero_doctor == len(doctores_disponibles) + 1:
            return  # Regresa al menú
        if numero_doctor < 1 or numero_doctor > len(doctores_disponibles):
            print("Opción inválida, intente de nuevo.")
            continue
        doctor_seleccionado = doctores_disponibles[numero_doctor - 1]
        # Simulación: asignamos citas disponibles solo si se selecciona "Doctor A"
        if doctor_seleccionado == "Doctor A":
            agenda_disponible = ["2023-10-01 10:00", "2023-10-01 11:00"]
        else:
            print("El doctor seleccionado no tiene citas disponibles, intente otro.")
    
    print("\nCitas disponibles:")
    for idx, slot in enumerate(agenda_disponible, start=1):
        print(f"{idx}. {slot}")
    try:
        numero_cita = int(input("Seleccione la cita de su preferencia: "))
    except ValueError:
        print("Entrada inválida.")
        return
    if numero_cita < 1 or numero_cita > len(agenda_disponible):
        print("Opción inválida, operación cancelada.")
        return
    cita_seleccionada = agenda_disponible[numero_cita - 1]
    print(f"Cita agendada con éxito para {cita_seleccionada} con {doctor_seleccionado}.")

def formula_medica(hospital: Hospital):
    cedula = input("Ingrese la cédula del paciente: ")
    # paciente = hospital.buscarPaciente(int(cedula))
    print("Funcionalidad de fórmula médica no implementada.")

def asignar_habitacion(hospital: Hospital):
    cedula = input("Ingrese el número de identificación del paciente: ")
    print("Funcionalidad de asignar habitación no implementada.")

def vacunacion(hospital: Hospital):
    cedula = input("Ingrese la cédula del paciente: ")
    print("Funcionalidad de vacunación no implementada.")

def facturacion(hospital: Hospital):
    print("Funcionalidad de facturación no implementada.")

def menu_gestion_doctor(hospital: Hospital):
    while True:
        print("\nMENU GESTION DOCTOR")
        print("1. Registrar doctor")
        print("2. Eliminar doctor")
        print("3. Ver doctor")
        print("4. Agregar citas")
        print("5. Eliminar citas")
        print("6. Regresar")
        print("7. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            registrar_doctor(hospital)
        elif opcion == "2":
            eliminar_doctor(hospital)
        elif opcion == "3":
            ver_doctor(hospital)
        elif opcion == "4":
            agregar_citas(hospital)
        elif opcion == "5":
            eliminar_citas(hospital)
        elif opcion == "6":
            break
        elif opcion == "7":
            sys.exit(0)
        else:
            print("Opción inválida, intente de nuevo.")

def registrar_doctor(hospital: Hospital):
    try:
        # Validar cédula numérica
        id_doc = int(input("Ingrese el número de cédula: "))
    except ValueError:
        print("\nError: La cédula debe ser un número entero.")
        return

    # Validar EPS
    eps = input("Ingrese su tipo de EPS ('Subsidiado','Contributivo' o 'Particular'): ").capitalize()
    if eps not in ["Subsidiado", "Contributivo", "Particular"]:
        print("\nError: Tipo de EPS no válido.")
        return

    # Validar especialidad
    especialidad = input("Ingrese su especialidad ('General', 'Odontologia' o 'Oftalmologia'): ").capitalize()
    if especialidad not in ["General", "Odontologia", "Oftalmologia"]:
        print("\nError: Especialidad no válida.")
        return

    nombre = input("Ingrese el nombre del doctor: ").strip()
    
    # Verificar si el doctor ya existe
    if hospital.buscar_doctor(id_doc):
        print("\nError: Ya existe un doctor con esta cédula.")
        return
    
    # Crear y registrar el doctor
    nuevo_doctor = Doctor(
        cedula=id_doc,
        nombre=nombre,
        tipo_eps=eps,
        especialidad=especialidad
    )
    
    hospital.agregar_doctor(nuevo_doctor)
    print(f"\n¡Doctor {nombre} registrado exitosamente!")
    print(f"Especialidad: {especialidad} | EPS: {eps}")

    
def eliminar_doctor(hospital: Hospital):
    id_doc = input("Ingrese la cédula del doctor que se eliminará: ")
    try:
        id_doc = int(id_doc)  # Validar que sea un número
    except ValueError:
        print("\nError: La cédula debe ser un número entero.")
        return

    doctor = hospital.buscar_doctor(id_doc)
    if doctor:
        hospital.lista_doctores.remove(doctor)
        print(f"\n¡Doctor {doctor.nombre} (cédula: {id_doc}) eliminado exitosamente!")
    else:
        print("\nError: No existe un doctor con esa cédula.")

def ver_doctor(hospital: Hospital):
    try:
        id_doc = int(input("Ingrese la cédula del doctor: "))
    except ValueError:
        print("Error: La cédula debe ser un número entero.")
        return

    doctor = hospital.buscar_doctor(id_doc)
    if doctor is None:
        while True:
            print("El doctor no está registrado.\n¿Desea registrarlo?")
            print("1. Si")
            print("2. No")
            try:
                opcion = int(input("Seleccione una opción: "))
            except ValueError:
                print("Opción inválida.")
                continue

            if opcion == 1:
                registrar_doctor(hospital)
                return
            elif opcion == 2:
                print("Adios")
                return
            else:
                print("Opción Inválida, por favor intente de nuevo.")
    else:
        # Mostrar información del doctor
        print("Información del doctor:")
        print(f"Nombre: {doctor.nombre}")
        print(f"Cédula: {doctor.cedula}")
        print(f"Especialidad: {doctor.especialidad}")

def agregar_citas(hospital: Hospital):
    id_doc = input("Ingrese la cédula del doctor: ")
    fecha = input("Ingrese la fecha de la cita: ")
    print("La cita ha sido agregada a la agenda del doctor (simulación).")

def eliminar_citas(hospital: Hospital):
    id_doc = input("Ingrese la cédula del doctor para eliminar una cita: ")
    print("¡Cita eliminada con exito! (simulación)")

def menu_gestion_hospital(hospital: Hospital):
    while True:
        print("\nMENU GESTION HOSPITAL")
        print("1. Construir Habitación")
        print("2. Ver lista de Habitaciones")
        print("3. Destruir Habitación")
        print("4. Agregar Medicamentos")
        print("5. Ver Inventario de medicamentos")
        print("6. Ver personas registradas en el hospital")
        print("7. Ver vacunas registradas en el hospital")
        print("8. Regresar")
        print("9. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            construir_habitacion(hospital)
        elif opcion == "2":
            print("Mostrando lista de habitaciones (simulación).")
        elif opcion == "3":
            destruir_habitacion(hospital)
        elif opcion == "4":
            print("Agregando medicamentos (simulación).")
        elif opcion == "5":
            ver_medicamentos(hospital)
        elif opcion == "6":
            ver_personas_registradas(hospital)
        elif opcion == "7":
            ver_vacunas(hospital)
        elif opcion == "8":
            break
        elif opcion == "9":
            sys.exit(0)
        else:
            print("Opción inválida, intente de nuevo.")

def construir_habitacion(hospital: Hospital):
    numero = input("Ingrese el número de la habitación: ")
    print("Nueva habitación construida (simulación).")

def ver_habitacion(hospital: Hospital):
    categoria = input("Ingrese el tipo de habitacion que desea ver: ")
    print("Mostrando habitaciones (simulación).")

def destruir_habitacion(hospital: Hospital):
    numero = input("Ingrese el número de la habitación a destruir: ")
    print("Habitación destruida (simulación).")

def agregar_medicamentos(hospital: Hospital):
    print("¡Los medicamentos han sido actualizados/creados con éxito! (simulación).")

def ver_medicamentos(hospital: Hospital):
    print("Inventario de medicamentos (simulación).")

def ver_personas_registradas(hospital: Hospital):
    print("Mostrando listado de doctores y pacientes (simulación).")

def ver_vacunas(hospital: Hospital):
    print("Mostrando vacunas registradas (simulación).")

def menu_gestion_paciente(hospital: Hospital):
    while True:
        print("\nMENU GESTION PACIENTE")
        print("1. Registrar paciente")
        print("2. Registrar enfermedad")
        print("3. Eliminar paciente")
        print("4. Ver paciente")
        print("5. Regresar")
        print("6. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            registrar_paciente(hospital)
        elif opcion == "2":
            registrar_nueva_enfermedad(hospital)
        elif opcion == "3":
            eliminar_paciente(hospital)
        elif opcion == "4":
            ver_paciente(hospital)
        elif opcion == "5":
            break
        elif opcion == "6":
            sys.exit(0)
        else:
            print("Opción inválida, intente de nuevo.")

def registrar_paciente(hospital: Hospital):
    nombre = input("Ingrese el nombre del paciente: ")
    id_paciente = input("Ingrese el número de cédula: ")
    eps = input("Ingrese su tipo de EPS ('Subsidiado', 'Contributivo' o 'Particular'): ")
    try:
        paciente = Paciente(int(id_paciente), nombre, eps)
        hospital.lista_pacientes.append(paciente)
        print("Paciente registrado con éxito.")
    except ValueError:
        print("Error: El número de cédula debe ser un valor numérico.")

def registrar_nueva_enfermedad(hospital: Hospital):
    id_paciente = input("Ingrese la cédula del paciente para registrar nuevas enfermedades: ")
    print("Nueva enfermedad registrada (simulación).")

def eliminar_paciente(hospital: Hospital):
    id_paciente = input("Ingrese el número de cédula del paciente a eliminar: ")
    try:
        id_int = int(id_paciente)
        paciente = hospital.buscarPaciente(id_int)
        if paciente:
            hospital.lista_pacientes.remove(paciente)
            print("Paciente eliminado con éxito.")
        else:
            print("Paciente no encontrado.")
    except ValueError:
        print("Error: La cédula debe ser un valor numérico.")

def ver_paciente(hospital: Hospital):
    id_paciente = input("Ingrese el número de cédula del paciente a ver: ")
    try:
        id_int = int(id_paciente)
        paciente = hospital.buscarPaciente(id_int)
        if paciente:
            print("\nInformación del paciente:")
            print(paciente)
        else:
            print("Paciente no encontrado.")
    except ValueError:
        print("Error: La cédula debe ser un valor numérico.")





def menu_gestion_vacunas(hospital: Hospital):
    # Implementar las opciones para gestionar vacunas
    print("Gestión de vacunas no implementada en este esqueleto.")

def main():
    hospital = Hospital()  # Instanciar hospital
    mostrar_mensaje_bienvenida()
    mostrar_utilidad_programa()
    menu_inicial(hospital)

if __name__ == "__main__":
    main()