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

from baseDatos.deserializador import cargar_todo
from baseDatos.serializador import guardar_todo

import tkinter as tk
from GUI.GUI import Aplicacion

def mostrar_mensaje_bienvenida():
    print("Bienvenido al Sistema de registro hospitalario basado en objetos")

def mostrar_utilidad_programa():
    print("Utilidades del programa:")
    print("- Gestión de pacientes, doctores y medicamentos.")
    print("- Asignación de habitaciones en el hospital.")
    print("- Registro y manejo de citas médicas y de vacunación.")
    print("- Generación de facturas y control de pagos.")
    print("- Manejo de inventario de medicamentos y vacunas.")

def exit_program(hospital: Hospital):
    guardar_todo(hospital)
    sys.exit(0)

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
            exit_program(hospital)
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
            exit_program(hospital)
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
            exit_program(hospital)
        else:
            print("Opción inválida, intente de nuevo.")

def agendar_citas(hospital: Hospital, cedula: str = None):
    if not cedula:
        cedula = input("Ingrese su número de cédula: ")
    try:
        cedula = int(cedula)
    except ValueError:
        print("Entrada inválida.")
        return
    paciente = hospital.buscarPaciente(cedula)
    if not paciente:
        print("Paciente no encontrado. Por favor regístrese.")
        return
    print(paciente.bienvenida() if hasattr(paciente, "bienvenida") else "Bienvenido, paciente.")

    # Seleccionar el tipo de cita y filtrar doctores por especialidad...
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
            return

        especialidad = ""
        if tipo_cita == 1:
            especialidad = "General"
        elif tipo_cita == 2:
            especialidad = "Odontologia"
        elif tipo_cita == 3:
            especialidad = "Oftalmologia"
        
        # Filtrar doctores de la especialidad elegida.
        doctores_disponibles = [doc for doc in hospital.lista_doctores if doc.especialidad == especialidad]
        if not doctores_disponibles:
            print("No hay doctores disponibles para la especialidad seleccionada.")

    # Selección del doctor
    while True:
        print("\nDoctores disponibles:")
        for idx, doc in enumerate(doctores_disponibles, start=1):
            print(f"{idx}. {doc.nombre}")
        print(f"{len(doctores_disponibles)+1}. --Regresar al menú--")
        try:
            numero_doctor = int(input("Seleccione el doctor con el que quiere la cita: "))
        except ValueError:
            print("Opción inválida.")
            continue
        if numero_doctor == len(doctores_disponibles) + 1:
            return
        if numero_doctor < 1 or numero_doctor > len(doctores_disponibles):
            print("Opción inválida, intente de nuevo.")
            continue
        doctor_seleccionado = doctores_disponibles[numero_doctor - 1]
        # Si el doctor no tiene citas disponibles, se vuelve a pedir selección.
        agenda_disponible = [cita for cita in doctor_seleccionado.agenda if cita.paciente is None]
        if not agenda_disponible:
            print("El doctor seleccionado no tiene citas disponibles, intente otro.")
            continue
        break

    # Mostrar la agenda completa del doctor
    print("\nCitas del doctor:")
    for idx, cita in enumerate(doctor_seleccionado.agenda, start=1):
        estado = "Disponible" if cita.paciente is None else "Asignada"
        print(f"{idx}. {cita.fecha} - {estado}")

    try:
        numero_cita = int(input("Seleccione la cita de su preferencia: "))
    except ValueError:
        print("Entrada inválida.")
        return
    if numero_cita < 1 or numero_cita > len(doctor_seleccionado.agenda):
        print("Opción inválida, operación cancelada.")
        return
    cita_seleccionada = doctor_seleccionado.agenda[numero_cita - 1]
    if cita_seleccionada.paciente is not None:
        print("La cita seleccionada ya está asignada. Operación cancelada.")
        return

    # Asignar la cita al paciente y mostrar la agenda actualizada
    cita_seleccionada.paciente = paciente
    print(f"\nCita agendada con éxito para {cita_seleccionada.fecha} con {doctor_seleccionado.nombre}.")

    print("\nAgenda actualizada del doctor:")
    for idx, cita in enumerate(doctor_seleccionado.agenda, start=1):
        estado = "Disponible" if cita.paciente is None else "Asignada"
        print(f"{idx}. {cita.fecha} - {estado}")

def formula_medica(hospital: Hospital):
    # Solicitar y validar la cédula del paciente
    cedula = input("Ingrese la cédula del paciente: ")
    try:
        cedula = int(cedula)
    except ValueError:
        print("Error: La cédula debe ser un número entero.")
        return

    paciente = hospital.buscarPaciente(cedula)
    if not paciente:
        print("Paciente no encontrado. Por favor regístrese primero.")
        return

    # Verificar que el paciente tenga enfermedades registradas en su historia clínica
    if not paciente.historia_clinica.enfermedades:
        print("No hay enfermedades registradas. Diríjase a la opción de registrar enfermedad.")
        return

    # Listar las enfermedades registradas
    print("\nEnfermedades registradas:")
    for idx, enfermedad in enumerate(paciente.historia_clinica.enfermedades, start=1):
        print(f"{idx}. {enfermedad.nombre} - {enfermedad.tipologia}")

    opcion = input("Elija la enfermedad que desea tratar (ingrese el número correspondiente): ")
    try:
        opcion = int(opcion)
    except ValueError:
        print("Entrada inválida.")
        return
    if opcion < 1 or opcion > len(paciente.historia_clinica.enfermedades):
        print("Opción fuera de rango.")
        return

    # Seleccionar la enfermedad a tratar
    enfermedad_tratar = paciente.historia_clinica.enfermedades[opcion - 1]

    # Buscar doctores con la especialidad que corresponde a la enfermedad.
    # En lugar de hospital.buscar_tipo_doctor, se utiliza una lista por comprensión.
    doctores_cita = [doc for doc in hospital.lista_doctores if doc.especialidad == enfermedad_tratar.especialidad]
    if not doctores_cita:
        print("Ahora no contamos con doctores para tratar esta enfermedad. Lo sentimos mucho.")
        return

    print(f"\nDoctor(es) disponibles para formular {enfermedad_tratar.nombre} ({enfermedad_tratar.tipologia}):")
    for idx, doc in enumerate(doctores_cita, start=1):
        print(f"{idx}. {doc.nombre}")

    opcion_doc = input("Seleccione el doctor (ingrese el número correspondiente): ")
    try:
        opcion_doc = int(opcion_doc)
    except ValueError:
        print("Entrada inválida.")
        return
    if opcion_doc < 1 or opcion_doc > len(doctores_cita):
        print("Opción fuera de rango.")
        return
    doctor_escogido = doctores_cita[opcion_doc - 1]

    # Crear la fórmula asociada al paciente
    from gestorAplicacion.servicios.Formula import Formula
    formula_paciente = Formula(paciente)
    # Asignar el doctor seleccionado
    formula_paciente.doctor = doctor_escogido

    # Agregar medicamentos a la fórmula
    medicamentos_seleccionados = []
    while True:
        # Obtener medicamentos disponibles para la enfermedad a través del método 'med_enfermedad' del paciente
        disponibles = paciente.med_enfermedad(enfermedad_tratar, hospital)
        if not disponibles:
            print("No hay medicamentos disponibles para tratar esta enfermedad.")
            break

        print(f"\nMedicamentos disponibles para tratar {enfermedad_tratar.nombre}:")
        for idx, med in enumerate(disponibles, start=1):
            print(f"{idx}. {med.nombre}")

        opcion_med = input("Seleccione el medicamento a agregar (ingrese 0 para terminar): ")
        try:
            opcion_med = int(opcion_med)
        except ValueError:
            print("Entrada inválida.")
            continue

        if opcion_med == 0:
            break
        if opcion_med < 1 or opcion_med > len(disponibles):
            print("Opción fuera de rango.")
            continue

        medicamento_seleccionado = disponibles[opcion_med - 1]
        # Evitar agregar duplicados (opcional)
        if medicamento_seleccionado in medicamentos_seleccionados:
            print("Ya ha seleccionado este medicamento.")
        else:
            medicamentos_seleccionados.append(medicamento_seleccionado)
            print(f"Medicamento '{medicamento_seleccionado.nombre}' agregado.")

    if not medicamentos_seleccionados:
        print("No se agregaron medicamentos, la fórmula no se guardará.")
        return

    # Asignar la lista de medicamentos a la fórmula
    formula_paciente.lista_medicamentos = medicamentos_seleccionados
    # Agregar la fórmula a la historia clínica del paciente
    paciente.historia_clinica.lista_formulas.append(formula_paciente)

    # Calcular e imprimir el precio final de la fórmula
    precio_total = paciente.calcular_precio_formula(formula_paciente)
    print("\nFÓRMULA MÉDICA GENERADA:")
    print(formula_paciente)
    print(f"Precio total de la fórmula: {precio_total}")


def asignar_habitacion(hospital: Hospital):
    try:
        cedula = int(input("Ingrese el número de identificación del paciente: "))
    except ValueError:
        print("Cédula inválida.")
        return

    paciente = hospital.buscarPaciente(cedula)
    if not paciente:
        print("Paciente no encontrado. Por favor regístrese primero.")
        return

    # Usar la instancia hospital para obtener las habitaciones disponibles
    habitaciones_disponibles = [h for h in hospital.habitaciones if not h.ocupada]
    if not habitaciones_disponibles:
        print("No hay habitaciones disponibles en el momento.")
        return

    print("\nHabitaciones disponibles:")
    for idx, habitacion in enumerate(habitaciones_disponibles, start=1):
        categoria = habitacion.categoria.name
        print(f"{idx}. Número: {habitacion.numero}, Categoría: {categoria}")

    try:
        opcion = int(input("Seleccione el número de la habitación deseada: "))
    except ValueError:
        print("Opción inválida.")
        return

    if opcion < 1 or opcion > len(habitaciones_disponibles):
        print("Opción inválida, selección fuera de rango.")
        return

    habitacion_seleccionada = habitaciones_disponibles[opcion - 1]

    try:
        dias = int(input("Ingrese la cantidad de días de hospedaje: "))
    except ValueError:
        print("Número de días inválido.")
        return

    # Asignar la habitación al paciente y marcarla como ocupada
    habitacion_seleccionada.paciente = paciente
    habitacion_seleccionada.ocupada = True
    habitacion_seleccionada.dias = dias
    paciente.habitacion_asignada = habitacion_seleccionada

    # Calcular el costo: costo = días * valor de la categoría (definido en CategoriaHabitacion)
    costo_total = dias * habitacion_seleccionada.categoria.get_valor()
    print(f"\n¡Habitación asignada con éxito!")
    print(f"Paciente: {paciente.nombre}")
    print(f"Habitación número: {habitacion_seleccionada.numero}")
    print(f"Categoría: {habitacion_seleccionada.categoria.name}")
    print(f"Días de hospedaje: {dias}")
    print(f"Costo total: {costo_total}")


def vacunacion(hospital: Hospital):
    # Solicitar la cédula del paciente y buscarlo
    try:
        cedula = int(input("Ingrese la cédula del paciente: "))
    except ValueError:
        print("Cédula inválida.")
        return
    paciente = hospital.buscarPaciente(cedula)
    if paciente is None:
        print("Paciente no encontrado.")
        return

    # Mensaje de bienvenida (si el paciente tiene el método 'bienvenida')
    if hasattr(paciente, "bienvenida"):
        print(paciente.bienvenida())
    else:
        print(f"Bienvenido, {paciente.nombre}")

    # Solicitar el tipo de vacuna a aplicar
    print("\nSeleccione el tipo de vacuna que requiere:")
    print("1. Obligatoria")
    print("2. No obligatoria")
    try:
        tipo_vacuna = int(input("Ingrese una opción: "))
    except ValueError:
        print("Opción inválida.")
        return
    if tipo_vacuna not in [1, 2]:
        print("Opción fuera de rango.")
        return

    # Filtrar vacunas disponibles según el tipo (comparando en minúscula)
    vacunas_disponibles = []
    for vacuna in hospital.lista_vacunas:
        if tipo_vacuna == 1 and vacuna.tipo.lower() == "obligatoria":
            vacunas_disponibles.append(vacuna)
        elif tipo_vacuna == 2 and vacuna.tipo.lower() == "no obligatoria":
            vacunas_disponibles.append(vacuna)
    if not vacunas_disponibles:
        print("No hay vacunas disponibles para el tipo seleccionado.")
        return

    print("\nVacunas disponibles:")
    for idx, vacuna in enumerate(vacunas_disponibles, start=1):
        print(f"{idx}. {vacuna.nombre} (Tipo: {vacuna.tipo}, Precio: {vacuna.precio})")
    
    try:
        num_vacuna = int(input("Seleccione la vacuna que desea aplicar (ingrese el número): "))
    except ValueError:
        print("Opción inválida.")
        return
    if num_vacuna < 1 or num_vacuna > len(vacunas_disponibles):
        print("Selección fuera de rango.")
        return
    vacuna_seleccionada = vacunas_disponibles[num_vacuna - 1]

    # Mostrar la agenda disponible para la vacuna seleccionada
    agenda_disponible = vacuna_seleccionada.mostrar_agenda_disponible()
    if not agenda_disponible:
        print("No hay citas disponibles para esta vacuna.")
        return

    print("\nCitas disponibles para la vacuna:")
    for idx, cita in enumerate(agenda_disponible, start=1):
        print(f"{idx}. Fecha: {cita.get_fecha()}")

    try:
        num_cita = int(input("Seleccione la cita de su preferencia: "))
    except ValueError:
        print("Opción inválida.")
        return
    if num_cita < 1 or num_cita > len(agenda_disponible):
        print("Selección fuera de rango.")
        return

    # Actualizar la agenda: asignar la cita al paciente
    cita_asignada = vacuna_seleccionada.actualizar_agenda(paciente, num_cita, agenda_disponible)
    if cita_asignada is None:
        print("No se pudo asignar la cita.")
        return

    # Actualizar el historial de vacunas del paciente
    if hasattr(paciente, "actualizar_historial_vacunas"):
        paciente.actualizar_historial_vacunas(cita_asignada)
    else:
        # Si el paciente no tiene el método, asegurarse de tener un historial (simulación)
        if not hasattr(paciente, "historia_clinica"):
            paciente.historia_clinica = type("HistoriaClinica", (), {"historial_vacunas": []})()
        paciente.historia_clinica.historial_vacunas.append(cita_asignada)

    # Imprimir resumen de la cita asignada
    print("\nResumen de su cita de vacunación:")
    print(f"Fecha: {cita_asignada.get_fecha()}")
    print(f"Paciente: {cita_asignada.paciente.nombre}")
    print(f"Vacuna: {vacuna_seleccionada.nombre}")
    print("Asistente médico: Enfermera")
    
    # Mostrar historial de vacunas aplicadas (si existe)
    if hasattr(paciente, "historia_clinica") and hasattr(paciente.historia_clinica, "historial_vacunas"):
        print("\nHistorial de vacunas aplicadas:")
        for idx, cv in enumerate(paciente.historia_clinica.historial_vacunas, start=1):
            print(f"{idx}. Fecha: {cv.get_fecha()}, Vacuna: {cv.vacuna.nombre}")
    
def facturacion(hospital: Hospital):
    # Solicitar la cédula del paciente y buscarlo
    try:
        cedula = int(input("Ingrese la cédula del paciente para facturación: "))
    except ValueError:
        print("Cédula inválida.")
        return

    paciente = hospital.buscarPaciente(cedula)
    if paciente is None:
        print("Paciente no encontrado.")
        return

    print(f"\n--- Facturación para {paciente.nombre} ---")

    servicios = []  # Lista de tuplas (descripción, costo)
    total = 0.0

    # Agregar fórmulas médicas (si existen)
    if hasattr(paciente, "historia_clinica") and hasattr(paciente.historia_clinica, "lista_formulas"):
        for formula in paciente.historia_clinica.lista_formulas:
            costo_formula = paciente.calcular_precio_formula(formula)
            descripcion = f"FÓRMULA MÉDICA con Dr(a). {formula.doctor.nombre}"
            servicios.append((descripcion, costo_formula))
            total += costo_formula

    # Agregar citas de vacunación (si existen)
    if hasattr(paciente, "historia_clinica") and hasattr(paciente.historia_clinica, "historial_vacunas"):
        for cita in paciente.historia_clinica.historial_vacunas:
            costo_vacuna = paciente.calcular_precio_cita_vacuna(cita)
            descripcion = f"Vacunación - {cita.vacuna.nombre} en fecha {cita.get_fecha()}"
            servicios.append((descripcion, costo_vacuna))
            total += costo_vacuna

    # Agregar asignación de habitación (si existe)
    if hasattr(paciente, "habitacion_asignada") and paciente.habitacion_asignada is not None:
        costo_habitacion = paciente.calcular_precio_habitacion(paciente.habitacion_asignada)
        descripcion = (f"Habitación #{paciente.habitacion_asignada.numero} - "
                       f"{paciente.habitacion_asignada.categoria.name} "
                       f"por {paciente.habitacion_asignada.dias} día(s)")
        servicios.append((descripcion, costo_habitacion))
        total += costo_habitacion

    if not servicios:
        print("No se encontraron servicios facturables para este paciente.")
        return

    # Mostrar la factura detallada
    print("\nServicios facturados:")
    for idx, (desc, costo) in enumerate(servicios, start=1):
        print(f"{idx}. {desc} -- Costo: {costo}")

    print(f"\nTotal a pagar: {total}")

    # Opción para pagar
    opcion_pago = input("¿Desea proceder con el pago? (S/N): ").strip().lower()
    if opcion_pago == "s":
        print("Pago realizado con éxito.")
        # Opcional: Aquí podrías limpiar el historial o marcar la factura como pagada.
    else:
        print("Pago cancelado.")
        
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
            exit_program(hospital)
        else:
            print("Opción inválida, intente de nuevo.")

def registrar_doctor(hospital: Hospital):
    try:
        id_doc = int(input("Ingrese el número de cédula: "))
    except ValueError:
        print("\nError: La cédula debe ser un número entero.")
        return

    eps = input("Ingrese su tipo de EPS ('Subsidiado','Contributivo' o 'Particular'): ").capitalize()
    if eps not in ["Subsidiado", "Contributivo", "Particular"]:
        print("\nError: Tipo de EPS no válido.")
        return

    especialidad = input("Ingrese su especialidad ('General', 'Odontologia' o 'Oftalmologia'): ").capitalize()
    if especialidad not in ["General", "Odontologia", "Oftalmologia"]:
        print("\nError: Especialidad no válida.")
        return

    nombre = input("Ingrese el nombre del doctor: ").strip()
    
    if hospital.buscar_doctor(id_doc):
        print("\nError: Ya existe un doctor con esta cédula.")
        return
    
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
        id_doc = int(id_doc)
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
        print("Información del doctor:")
        print(f"Nombre: {doctor.nombre}")
        print(f"Cédula: {doctor.cedula}")
        print(f"Especialidad: {doctor.especialidad}")

        # Mostrar la agenda del doctor (citas disponibles y asignadas)
        print("\nAgenda del doctor:")
        if doctor.agenda:
            for idx, cita in enumerate(doctor.agenda, start=1):
                estado = "Disponible" if cita.paciente is None else "Asignada"
                print(f"{idx}. {cita.fecha} - {estado}")
        else:
            print("No tiene citas registradas.")

def agregar_citas(hospital: Hospital):
    try:
        id_doc = int(input("Ingrese la cédula del doctor: "))
    except ValueError:
        print("Cédula inválida.")
        return
    doctor = hospital.buscar_doctor(id_doc)
    if not doctor:
        print("Doctor no encontrado.")
        return
    fecha = input("Ingrese la fecha de la nueva cita (Ej: '10-10-2025 10:00'): ")
    # Importar Cita para crear la nueva cita
    from gestorAplicacion.servicios.Cita import Cita
    nueva_cita = Cita(doctor, fecha, None)
    doctor.agenda.append(nueva_cita)
    print("La cita ha sido agregada a la agenda del doctor.")
    print("Agenda actual:")
    for idx, cita in enumerate(doctor.agenda, start=1):
        estado = "Asignada" if cita.paciente else "Disponible"
        print(f"{idx}. Fecha: {cita.fecha} - {estado}")

def eliminar_citas(hospital: Hospital):
    try:
        id_doc = int(input("Ingrese la cédula del doctor para eliminar una cita: "))
    except ValueError:
        print("Cédula inválida.")
        return
    doctor = hospital.buscar_doctor(id_doc)
    if not doctor:
        print("Doctor no encontrado.")
        return
    # Mostrar solo las citas sin asignar (disponibles para eliminar)
    citas_disponibles = [cita for cita in doctor.agenda if cita.paciente is None]
    if not citas_disponibles:
        print("No hay citas disponibles para eliminar (todas están asignadas).")
        return
    print("Citas disponibles para eliminar:")
    for idx, cita in enumerate(citas_disponibles, start=1):
        print(f"{idx}. Fecha: {cita.fecha}")
    try:
        opcion = int(input("Seleccione la cita que desea eliminar: "))
    except ValueError:
        print("Opción inválida.")
        return
    if opcion < 1 or opcion > len(citas_disponibles):
        print("Opción fuera de rango.")
        return
    cita_a_eliminar = citas_disponibles[opcion - 1]
    doctor.agenda.remove(cita_a_eliminar)
    print("¡Cita eliminada con éxito!")
    print("Agenda actual:")
    for idx, cita in enumerate(doctor.agenda, start=1):
        estado = "Asignada" if cita.paciente else "Disponible"
        print(f"{idx}. Fecha: {cita.fecha} - {estado}")

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
            ver_habitacion(hospital)
        elif opcion == "3":
            destruir_habitacion(hospital)
        elif opcion == "4":
            agregar_medicamentos(hospital)
        elif opcion == "5":
            ver_medicamentos(hospital)
        elif opcion == "6":
            ver_personas_registradas(hospital)
        elif opcion == "7":
            ver_vacunas(hospital)
        elif opcion == "8":
            break
        elif opcion == "9":
            exit_program(hospital)
        else:
            print("Opción inválida, intente de nuevo.")

def construir_habitacion(hospital: Hospital):
    try:
        numero = int(input("Ingrese el número de la habitación: "))
    except ValueError:
        print("Número inválido.")
        return

    print("Elija el tipo de habitación que desea construir")
    print("1. CAMILLA")
    print("2. INDIVIDUAL")
    print("3. DOBLE")
    print("4. OBSERVACION")
    print("5. UCI")
    print("6. UCC")
    opcion = input("Ingrese una opción: ")

    opciones = {
        "1": "CAMILLA",
        "2": "INDIVIDUAL",
        "3": "DOBLE",
        "4": "OBSERVACION",
        "5": "UCI",
        "6": "UCC"
    }
    categoria_input = opciones.get(opcion)
    if categoria_input is None:
        print("Opción inválida.")
        return

    from gestorAplicacion.administracion.CategoriaHabitacion import CategoriaHabitacion
    try:
        # Usar la sintaxis de enum para obtener el miembro correspondiente
        categoria = CategoriaHabitacion[categoria_input]
    except KeyError:
        print(f"'{categoria_input}' no es una categoría válida.")
        return

    from gestorAplicacion.servicios.Habitacion import Habitacion
    nueva_habitacion = Habitacion(numero, categoria, False, None, 0)
    # Cambiar de Hospital.habitaciones a la instancia hospital.habitaciones
    hospital.habitaciones.append(nueva_habitacion)
    print(f"Habitación número {numero} con categoría {categoria_input} construida con éxito.")


def ver_habitacion(hospital: Hospital):
    habitaciones = Hospital.habitaciones
    if habitaciones:
        print("Listado de habitaciones creadas:")
        for habitacion in habitaciones:
            categoria = habitacion.categoria.nombre if hasattr(habitacion.categoria, "nombre") else habitacion.categoria
            print(f"- Número: {habitacion.numero}, Categoría: {categoria}, Ocupada: {habitacion.ocupada}")
    else:
        print("No se han creado habitaciones.")
        
def destruir_habitacion(hospital: Hospital):
    try:
        numero = int(input("Ingrese el número de la habitación a destruir: "))
    except ValueError:
        print("Número inválido.")
        return
    habitacion_a_destruir = None
    for habitacion in Hospital.habitaciones:
        if habitacion.numero == numero:
            habitacion_a_destruir = habitacion
            break
    if habitacion_a_destruir:
        Hospital.habitaciones.remove(habitacion_a_destruir)
        print(f"Habitación número {numero} destruida con éxito.")
    else:
        print("No se encontró la habitación.")

def agregar_medicamentos(hospital: Hospital):
    nombre = input("Ingrese el nombre del medicamento: ").strip()
    descripcion = input("Ingrese la descripción del medicamento: ").strip()
    try:
        cantidad = int(input("Ingrese la cantidad disponible: "))
        precio = float(input("Ingrese el precio del medicamento: "))
    except ValueError:
        print("Cantidad o precio inválido.")
        return

    enfermedad_nombre = input("Ingrese el nombre de la enfermedad asociada: ").strip()

    print("Seleccione la tipología de la enfermedad asociada:")
    print("1. General")
    print("2. Odontologia")
    print("3. Oftalmologia")
    opcion = input("Seleccione una opción: ").strip()
    tipologia_mapping = {
        "1": "General",
        "2": "Odontologia",
        "3": "Oftalmologia"
    }
    if opcion not in tipologia_mapping:
        print("Opción inválida, se asignará 'General' por defecto.")
        tipologia = "General"
    else:
        tipologia = tipologia_mapping[opcion]

    from gestorAplicacion.personas.Enfermedad import Enfermedad
    nueva_enfermedad = Enfermedad(tipologia, enfermedad_nombre, tipologia)

    from gestorAplicacion.administracion.Medicamento import Medicamento
    nuevo_medicamento = Medicamento(nombre, nueva_enfermedad, descripcion, cantidad, precio)
    hospital.lista_medicamentos.append(nuevo_medicamento)
    print("¡Medicamento agregado con éxito!")

def ver_medicamentos(hospital: Hospital):
    if hospital.lista_medicamentos:
        print("Inventario de medicamentos:")
        for medicamento in hospital.lista_medicamentos:
            print(medicamento)
    else:
        print("No hay medicamentos registrados.")

def ver_personas_registradas(hospital: Hospital):
    print("Listado de Doctores:")
    if hospital.lista_doctores:
        for doctor in hospital.lista_doctores:
            print(doctor)
    else:
        print("No hay doctores registrados.")
    print("\nListado de Pacientes:")
    if hospital.lista_pacientes:
        for paciente in hospital.lista_pacientes:
            print(paciente)
    else:
        print("No hay pacientes registrados.")

def ver_vacunas(hospital: Hospital):
    if hospital.lista_vacunas:
        print("Vacunas registradas:")
        for vacuna in hospital.lista_vacunas:
            print(f"- Nombre: {vacuna.nombre}, Tipo: {vacuna.tipo}, Precio: {vacuna.precio}")
            print("  EPS disponibles: " + ", ".join(vacuna.tipo_eps))
    else:
        print("No hay vacunas registradas.")

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
            exit_program(hospital)
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
    try:
        cedula = int(input("Ingrese la cédula del paciente para registrar nuevas enfermedades: "))
    except ValueError:
        print("Error: La cédula debe ser un número entero.")
        return

    paciente = hospital.buscarPaciente(cedula)
    if paciente is None:
        print("Error: Paciente no encontrado.")
        return

    enfermedad_nombre = input("Ingrese el nombre de la nueva enfermedad: ").strip()
    
    print("Seleccione la tipología de la enfermedad:")
    print("1. General")
    print("2. Odontologia")
    print("3. Oftalmologia")
    opcion = input("Seleccione una opción: ").strip()
    tipologia_mapping = {
        "1": "General",
        "2": "Odontologia",
        "3": "Oftalmologia"
    }
    if opcion not in tipologia_mapping:
        print("Opción inválida, operación cancelada.")
        return
    tipologia = tipologia_mapping[opcion]

    from gestorAplicacion.personas.Enfermedad import Enfermedad
    nueva_enfermedad = Enfermedad(tipologia, enfermedad_nombre, tipologia)

    if not hasattr(paciente, "historia_clinica") or paciente.historia_clinica is None:
        from gestorAplicacion.administracion.HistoriaClinica import HistoriaClinica
        paciente.historia_clinica = HistoriaClinica(paciente)

    if not hasattr(paciente.historia_clinica, "enfermedades") or paciente.historia_clinica.enfermedades is None:
        paciente.historia_clinica.enfermedades = []

    paciente.historia_clinica.enfermedades.append(nueva_enfermedad)
    print("Nueva enfermedad registrada exitosamente para el paciente.")

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
    while True:
        print("\nMENU Gestión Vacunas")
        print("1. Registrar vacuna")
        print("2. Eliminar vacuna")
        print("3. Ver información de una vacuna")
        print("4. Agregar cita a una vacuna")
        print("5. Eliminar cita a una vacuna")
        print("6. Regresar al menú anterior")
        print("7. Salir")
        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            registrar_vacuna(hospital)
        elif opcion == "2":
            eliminar_vacuna(hospital)
        elif opcion == "3":
            ver_vacuna(hospital)
        elif opcion == "4":
            agregar_cita_vacuna(hospital)
        elif opcion == "5":
            eliminar_cita_vacuna(hospital)
        elif opcion == "6":
            break
        elif opcion == "7":
            exit_program(hospital)
        else:
            print("Opción inválida. Intente de nuevo.")

def registrar_vacuna(hospital: Hospital):
    print("\nRegistrar Vacuna")
    nombre = input("Ingrese el nombre de la vacuna (Inicia con mayúscula): ")
    if hospital.buscar_vacuna(nombre):
        print("Esta vacuna ya está registrada.")
        return
    tipo = input("Ingrese el tipo de vacuna (Obligatoria/No obligatoria): ")
    
    tipo_eps = []
    valid_eps = ["Subsidiado", "Contributivo", "Particular"]
    while True:
        print("Opciones EPS: " + ", ".join(valid_eps))
        eps = input("Ingrese su tipo de EPS ('Subsidiado','Contributivo' o 'Particular') (o 'fin' para terminar): ")
        if eps.lower() == 'fin':
            break
        if eps not in valid_eps:
            print("Opción EPS inválida. Por favor, ingrese una de las opciones: " + ", ".join(valid_eps))
            continue
        tipo_eps.append(eps)
    
    try:
        precio = float(input("Ingrese el precio de la vacuna: "))
    except ValueError:
        print("Precio inválido.")
        return
    
    vacuna_nueva = Vacuna(tipo, nombre, tipo_eps, precio)
    hospital.lista_vacunas.append(vacuna_nueva)
    
    print("\nInformación de la nueva vacuna registrada:")
    print(f"Vacuna: {vacuna_nueva.nombre}")
    print(f"Tipo: {vacuna_nueva.tipo}")
    print(f"Precio: {vacuna_nueva.precio}")
    print("EPS disponibles:")
    for eps in vacuna_nueva.tipo_eps:
        print(f"- {eps}")

def eliminar_vacuna(hospital: Hospital):
    print("\nEliminar Vacuna")
    nombre = input("Ingrese el nombre de la vacuna que desea eliminar: ")
    vacuna = hospital.buscar_vacuna(nombre)
    if vacuna is None:
        print("Esta vacuna no existe en el inventario del hospital.")
    else:
        hospital.lista_vacunas.remove(vacuna)
        print("¡Vacuna eliminada!")

def ver_vacuna(hospital: Hospital):
    print("\nVer Información de Vacuna")
    nombre = input("Ingrese el nombre de la vacuna: ")
    vacuna = hospital.buscar_vacuna(nombre)
    if vacuna is None:
        print("Esta vacuna no existe en el inventario del hospital.")
    else:
        print(f"\nNombre: {vacuna.nombre}")
        print(f"Tipo: {vacuna.tipo}")
        print(f"Precio: {vacuna.precio}")
        print("EPS disponibles:")
        for eps in vacuna.tipo_eps:
            print(f"- {eps}")
        print("Agenda de citas:")
        if vacuna.agenda:
            for cita in vacuna.agenda:
                estado = "(Disponible)" if cita.paciente is None else "(Asignada)"
                print(f"- {cita.get_fecha()} {estado}")
        else:
            print("No hay citas registradas.")

def agregar_cita_vacuna(hospital: Hospital):
    print("\nAgregar Cita a Vacuna")
    nombre = input("Ingrese el nombre de la vacuna: ")
    vacuna = hospital.buscar_vacuna(nombre)
    if vacuna is None:
        print("Esta vacuna no existe en el inventario del hospital.")
        return
    nueva_fecha = input("Ingrese la fecha para la nueva cita (Ej: '6 de Marzo, 9:00 am'): ")
    nueva_cita = CitaVacuna(nueva_fecha, None, vacuna)
    vacuna.agenda.append(nueva_cita)
    print("Nueva cita agregada con éxito a la vacuna.")

def eliminar_cita_vacuna(hospital: Hospital):
    print("\nEliminar Cita de Vacuna")
    nombre = input("Ingrese el nombre de la vacuna: ")
    vacuna = hospital.buscar_vacuna(nombre)
    if vacuna is None:
        print("Esta vacuna no existe en el inventario del hospital.")
        return
    citas_disponibles = vacuna.mostrar_agenda_disponible()
    if not citas_disponibles:
        print("No hay citas disponibles para eliminar en esta vacuna.")
        return
    print("Citas disponibles:")
    for idx, cita in enumerate(citas_disponibles, start=1):
        print(f"{idx}. {cita.get_fecha()}")
    try:
        opcion = int(input("Seleccione la cita que desea eliminar: "))
        if opcion < 1 or opcion > len(citas_disponibles):
            print("Opción inválida.")
            return
        cita_a_eliminar = citas_disponibles[opcion - 1]
        vacuna.agenda.remove(cita_a_eliminar)
        print("¡Cita eliminada con éxito!")
    except ValueError:
        print("Entrada inválida.")

def main():
    hospital = Hospital()  # Instanciar hospital
    cargar_todo(hospital)  # Cargar datos persistidos, si existen
    app = Aplicacion(hospital)
    app.mainloop()

if __name__ == "__main__":
    main()
