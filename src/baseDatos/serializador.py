import pickle
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def guardar_pacientes(pacientes):
    with open(os.path.join(DATA_DIR, "pacientes.pkl"), "wb") as f:
        pickle.dump(pacientes, f)

def guardar_doctores(doctores):
    with open(os.path.join(DATA_DIR, "doctores.pkl"), "wb") as f:
        pickle.dump(doctores, f)

def guardar_medicamentos(medicamentos):
    with open(os.path.join(DATA_DIR, "medicamentos.pkl"), "wb") as f:
        pickle.dump(medicamentos, f)

def guardar_vacunas(vacunas):
    with open(os.path.join(DATA_DIR, "vacunas.pkl"), "wb") as f:
        pickle.dump(vacunas, f)

def guardar_habitaciones(habitaciones):
    with open(os.path.join(DATA_DIR, "habitaciones.pkl"), "wb") as f:
        pickle.dump(habitaciones, f)

def guardar_todo(hospital):
    # Se asume que 'hospital' tiene los siguientes atributos:
    # lista_pacientes, lista_doctores, lista_medicamentos, lista_vacunas y habitaciones
    guardar_pacientes(hospital.lista_pacientes)
    guardar_doctores(hospital.lista_doctores)
    guardar_medicamentos(hospital.lista_medicamentos)
    guardar_vacunas(hospital.lista_vacunas)
    guardar_habitaciones(hospital.habitaciones)