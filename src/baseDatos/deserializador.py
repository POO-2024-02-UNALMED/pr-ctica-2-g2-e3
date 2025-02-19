import pickle
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def cargar_pacientes():
    path = os.path.join(DATA_DIR, "pacientes.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return []

def cargar_doctores():
    path = os.path.join(DATA_DIR, "doctores.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return []

def cargar_medicamentos():
    path = os.path.join(DATA_DIR, "medicamentos.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return []

def cargar_vacunas():
    path = os.path.join(DATA_DIR, "vacunas.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return []

def cargar_habitaciones():
    path = os.path.join(DATA_DIR, "habitaciones.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return []

def cargar_todo(hospital):
    # Se asume que 'hospital' es una instancia que contiene los atributos:
    # lista_pacientes, lista_doctores, lista_medicamentos, lista_vacunas y habitaciones
    hospital.lista_pacientes = cargar_pacientes()
    hospital.lista_doctores = cargar_doctores()
    hospital.lista_medicamentos = cargar_medicamentos()
    hospital.lista_vacunas = cargar_vacunas()
    hospital.habitaciones = cargar_habitaciones()