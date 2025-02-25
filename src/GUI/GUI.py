import os
import sys
# Agregar la raíz del proyecto a sys.path (por ejemplo, d:/uni/POO/proyecto/pr-ctica-2-g2-e3/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk, Menu, messagebox
from tkinter import PhotoImage
from tkinter import simpledialog
import os
from PIL import Image, ImageTk  # Importar Pillow
from gestorAplicacion.administracion.Hospital import Hospital
from gestorAplicacion.servicios.CitaVacuna import CitaVacuna
from gestorAplicacion.servicios.Cita import Cita
from gestorAplicacion.personas.Paciente import Paciente
from gestorAplicacion.personas.Doctor import Doctor
from gestorAplicacion.personas.Enfermedad import Enfermedad
from gestorAplicacion.administracion.HistoriaClinica import HistoriaClinica

from excepciones.ErrorAplicacion import ErrorPacienteNoEncontrado
from excepciones.ErrorAplicacion import ErrorNoServiciosFacturables
from excepciones.ErrorAplicacion import ErrorCampoVacio


class Inicio(ttk.Frame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Crear el menú
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)
        
        menu_inicio = Menu(self.menu_bar, tearoff=0)
        menu_inicio.add_command(label="Descripción del Sistema", command=self.mostrar_descripcion)
        menu_inicio.add_command(label="Salir", command=parent.quit)
        
        self.menu_bar.add_cascade(label="Inicio", menu=menu_inicio)
        
        # Contenedores principales
        self.p1 = ttk.Frame(self.container)
        self.p2 = ttk.Frame(self.container)
        
        self.p1.grid(row=0, column=0, sticky="nsew")
        self.p2.grid(row=0, column=1, sticky="nsew")
        
        # Subcontenedores
        self.p3 = ttk.Frame(self.p1, borderwidth=2, relief="ridge")
        self.p4 = ttk.Frame(self.p1, borderwidth=2, relief="ridge")
        self.p5 = ttk.Frame(self.p2, borderwidth=2, relief="ridge")
        self.p6 = ttk.Frame(self.p2, borderwidth=2, relief="ridge")
        
        self.p3.pack(fill=tk.BOTH, expand=True)
        self.p4.pack(fill=tk.BOTH, expand=True)
        self.p5.pack(fill=tk.BOTH, expand=True)
        self.p6.pack(fill=tk.BOTH, expand=True)
        
        # Zona P3 - Saludo de bienvenida
        ttk.Label(self.p3, text="Bienvenido al Sistema de Gestión Hospitalaria", font=("Arial", 14)).pack(pady=10)
        
        # Zona P4 - Imagen y botón de ingreso
        self.image_folder = os.path.join(os.path.dirname(__file__), "archivos")
        self.image_index = 0
        self.images = [self.load_image(os.path.join(self.image_folder, f"image{i}.png")) for i in range(1, 6)]
        self.label_image = ttk.Label(self.p4, image=self.images[self.image_index])
        self.label_image.pack(pady=10)
        self.label_image.bind("<Enter>", self.change_image)
        
        ttk.Button(self.p4, text="Ingresar", command=switch_callback).pack(pady=10)
        
        # Zona P5 - Hoja de vida
        self.desarrolladores = [
            "Samuel Gutierrez Betancur (19 años)\nIng. sistemas e informatica\nAficionado de la electronica y la guitarra",
            "Samuel Botero Rivera (25 años)\nIng.  fisica\nMi tiempo libre me gusta dedicarlo a la fotografia y a leer",
            "Samuel Garcia Rojas (19 años)\nIng. sistemas e informatica\nAficionado al futbol ",
        ]
        self.hoja_vida_index = 0
        self.label_hoja_vida = ttk.Label(self.p5, text=self.desarrolladores[self.hoja_vida_index], wraplength=200)
        self.label_hoja_vida.pack(pady=10)
        self.label_hoja_vida.bind("<Button-1>", self.change_hoja_vida)
        
        # Zona P6 - Fotos de los desarrolladores
        self.dev_images = [[self.load_image(os.path.join(self.image_folder, f"dev{i}_{j}.png")) for j in range(1, 5)] for i in range(1, 4)]
        self.frame_dev_images = ttk.Frame(self.p6)
        self.frame_dev_images.pack()
        self.update_dev_images()
        
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.rowconfigure(0, weight=1)
    
    def load_image(self, path, size=(100, 100)):
        """Carga y redimensiona una imagen."""
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
    def change_image(self, event):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.label_image.configure(image=self.images[self.image_index])
    
    def change_hoja_vida(self, event):
        self.hoja_vida_index = (self.hoja_vida_index + 1) % len(self.desarrolladores)
        self.label_hoja_vida.configure(text=self.desarrolladores[self.hoja_vida_index])
        self.update_dev_images()
    
    def update_dev_images(self):
        for widget in self.frame_dev_images.winfo_children():
            widget.destroy()
        for i in range(2):
            for j in range(2):
                label = ttk.Label(self.frame_dev_images, image=self.dev_images[self.hoja_vida_index][i * 2 + j])
                label.grid(row=i, column=j, padx=5, pady=5)
    
    def mostrar_descripcion(self):
        messagebox.showinfo("Descripción del Sistema", "Sistema de Gestión Hospitalaria: Gestión de pacientes, doctores y servicios médicos.")

class Aplicacion(tk.Tk):
    def __init__(self, hospital):
        super().__init__()
        self.geometry("800x500")
        self.title("Sistema de Gestión Hospitalaria")
        
        self.hospital = hospital
        self.ventana_inicio = Inicio(self, self.mostrar_ventana_principal)
    
    def mostrar_ventana_principal(self):
        self.ventana_inicio.destroy()
        self.ventana_principal = VentanaPrincipal(self, self.hospital)

class VentanaPrincipal(ttk.Frame):
    def __init__(self, parent, hospital):
        super().__init__(parent)
        self.hospital = hospital
        self.pack(fill=tk.BOTH, expand=True)
        
        self.label_titulo = ttk.Label(self, text="Sistema de Gestión Hospitalaria", font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=10)
        
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)
        
        menu_archivo = Menu(self.menu_bar, tearoff=0)
        menu_archivo.add_command(label="Aplicación", command=self.mostrar_info_app)
        menu_archivo.add_command(label="Salir", command=parent.quit)
        
        menu_procesos = Menu(self.menu_bar, tearoff=0)
        menu_procesos.add_command(label="Agendar Citas", command=self.mostrar_agendar_citas)
        menu_procesos.add_command(label="Generar Fórmulas Médicas", command=self.mostrar_generar_formulas_medicas)
        menu_procesos.add_command(label="Asignar Habitaciones", command=self.mostrar_asignar_habitaciones)
        menu_procesos.add_command(label="Aplicación de Vacunas", command=self.mostrar_aplicar_vacunas)
        menu_procesos.add_command(label="Facturación", command=self.mostrar_facturacion)
        
        menu_gestion = Menu(self.menu_bar, tearoff=0)
        menu_gestion.add_command(label="Gestionar Pacientes", command=self.mostrar_gestion_pacientes)
        menu_gestion.add_command(label="Gestionar Doctores", command=self.mostrar_gestion_doctores)
        menu_gestion.add_command(label="Gestionar Vacunas", command=self.mostrar_gestion_vacunas)
        menu_gestion.add_command(label="Gestionar Hospital", command=self.mostrar_gestion_hospital)
        
        menu_ayuda = Menu(self.menu_bar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_autores)
        
        self.menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
        self.menu_bar.add_cascade(menu=menu_procesos, label="Procesos y Consultas")
        self.menu_bar.add_cascade(label="Gestión", menu=menu_gestion)
        self.menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
        
        self.frame_contenido = ttk.Frame(self, borderwidth=2, relief="ridge")
        self.frame_contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(self.frame_contenido, text="Seleccione una opción del menú", font=("Arial", 12, "bold")).pack(pady=5)
    
    def mostrar_info_app(self):
        messagebox.showinfo("Aplicación", "Sistema de Gestión Hospitalaria: Gestión de pacientes, doctores y servicios médicos.")
    
    def mostrar_autores(self):
        messagebox.showinfo("Acerca de", "Autores: Samuel Gutierrez, Samuel Garcia, Samuel Botero")

    def mostrar_agendar_citas(self):
        self.actualizar_frame_contenido("Agendar Citas", "Ingrese el número de cédula del paciente:", [])
        
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.obtener_cedula("Agendar Citas")).pack(pady=5)

    def mostrar_generar_formulas_medicas(self):
        self.actualizar_frame_contenido("Generar Fórmulas Médicas", "Ingrese el número de cédula del paciente:", [])
        
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.obtener_cedula("Generar Fórmulas Médicas")).pack(pady=5)

    def mostrar_asignar_habitaciones(self):
        self.actualizar_frame_contenido("Asignar Habitaciones", "Ingrese el número de cédula del paciente:", [])
        
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.obtener_cedula("Asignar Habitaciones")).pack(pady=5)

    def mostrar_aplicar_vacunas(self):
        self.actualizar_frame_contenido("Aplicación de Vacunas", "Ingrese el número de cédula del paciente:", [])
        
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.obtener_cedula("Aplicación de Vacunas")).pack(pady=5)

    def mostrar_facturacion(self):
        self.actualizar_frame_contenido("Facturación", "Ingrese el número de cédula del paciente:", [])
        
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.obtener_cedula_facturacion).pack(pady=5)

    def obtener_cedula_facturacion(self):
        cedula = self.entry_cedula.get()
        if not cedula:
            messagebox.showerror("Error", "Por favor ingrese un número de cédula.")
            return

        try:
            # Verificar si el paciente existe
            paciente = self.hospital.buscarPaciente(int(cedula))
            if not paciente:
                raise ErrorPacienteNoEncontrado(int(cedula))  # Lanza la excepción si el paciente no se encuentra

            # Proceder con la facturación
            self.facturacion(cedula)
        except ErrorPacienteNoEncontrado as e:
            messagebox.showerror("Error", str(e))  # Muestra el mensaje de error de la excepción
        except ValueError as e:
            messagebox.showerror("Error", f"Valor incorrecto: {e}")  # En caso de que haya un error en el valor ingresado

    def facturacion(self, cedula):
        from uiMain.main import facturacion
        paciente = self.hospital.buscarPaciente(int(cedula))
        if paciente is None:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return

        servicios, total = facturacion(self.hospital, cedula)
        if not servicios:
            messagebox.showinfo("Información", "No se encontraron servicios facturables para este paciente.")
            return

        factura_detalle = "\n".join([f"{idx+1}. {desc} -- Costo: {costo}" for idx, (desc, costo) in enumerate(servicios)])
        self.actualizar_frame_contenido("Factura Detallada", f"Servicios facturados:\n{factura_detalle}\n\nTotal a pagar: {total}", [])

        ttk.Button(self.frame_contenido, text="Pagar", command=lambda: self.realizar_pago(total)).pack(pady=5)

    def realizar_pago(self, total):
        messagebox.showinfo("Pago Exitoso", f"Pago de {total} realizado con éxito.")

    def actualizar_frame_contenido(self, titulo, descripcion, criterios_valores):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        ttk.Label(self.frame_contenido, text=titulo, font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(self.frame_contenido, text=descripcion, wraplength=400).pack(pady=5)
        
        if criterios_valores:
            frame_tabla = ttk.Frame(self.frame_contenido)
            frame_tabla.pack(pady=5)
            
            for criterio, valor in criterios_valores:
                fila = ttk.Frame(frame_tabla)
                fila.pack(fill=tk.X, pady=2)
                ttk.Label(fila, text=criterio, width=20).pack(side=tk.LEFT)
                ttk.Label(fila, text=valor, width=20).pack(side=tk.LEFT)

    def obtener_cedula(self, titulo):
        cedula = self.entry_cedula.get()
        try:
            if not cedula:
                raise ErrorCampoVacio ("Número de cédula") # Lanza la excepción si el campo está vacío
        
        except ErrorCampoVacio as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            if type(cedula) != int:
                raise ErrorTipoDatoIncorrecto("Número de cédula", "int", type(cedula)) # Lanza la excepción si el tipo de dato es incorrecto
        except ErrorTipoDatoIncorrecto as e:
            messagebox.showerror("Error", str(e))
        try:
            # Verificar si el paciente existe
            paciente = self.hospital.buscarPaciente(int(cedula))
            if not paciente:
                raise ErrorPacienteNoEncontrado(int(cedula))  # Lanza la excepción si el paciente no se encuentra

            # Si el paciente no tiene errores, hacer algo según el título
            if titulo == "Agendar Citas":
                self.agendar_citas(cedula)
            elif titulo == "Generar Fórmulas Médicas":
                self.generar_formulas_medicas(cedula)
            elif titulo == "Asignar Habitaciones":
                self.asignar_habitaciones(cedula)
            elif titulo == "Aplicación de Vacunas":
                self.aplicar_vacunas(cedula)
            elif titulo == "Facturación":
                self.facturacion(cedula)
        except ErrorPacienteNoEncontrado as e:
            messagebox.showerror("Error", str(e))  # Muestra el mensaje de error de la excepción
        except ValueError as e:
            messagebox.showerror("Error", f"Valor incorrecto: {e}")  # En caso de que haya un error en el valor ingresado

    def mostrar_gestion_pacientes(self):
        self.actualizar_frame_contenido("Gestionar Pacientes", "Seleccione una opción:", [])
        opciones_pacientes = ["Registrar Paciente", "Registrar Enfermedad", "Eliminar Paciente", "Ver Paciente"]
        self.gestion_pacientes_combobox = ttk.Combobox(self.frame_contenido, values=opciones_pacientes)
        self.gestion_pacientes_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.seleccionar_gestion_pacientes).pack(pady=5)
    
    def seleccionar_gestion_pacientes(self):
        opcion = self.gestion_pacientes_combobox.get()
        if opcion == "Registrar Paciente":
            self.registrar_paciente()
        elif opcion == "Registrar Enfermedad":
            self.registrar_enfermedad()
        elif opcion == "Eliminar Paciente":
            self.eliminar_paciente()
        elif opcion == "Ver Paciente":
            self.ver_paciente()

    def registrar_paciente(self):
        self.actualizar_frame_contenido("Registrar Paciente", "Ingrese los datos del paciente:", [])
        
        ttk.Label(self.frame_contenido, text="Nombre:").pack(pady=5)
        self.entry_nombre = ttk.Entry(self.frame_contenido)
        self.entry_nombre.pack(pady=5)
        
        ttk.Label(self.frame_contenido, text="Cédula:").pack(pady=5)
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        
        ttk.Label(self.frame_contenido, text="EPS:").pack(pady=5)
        self.entry_eps = ttk.Entry(self.frame_contenido)
        self.entry_eps.pack(pady=5)
        
        ttk.Button(self.frame_contenido, text="Registrar", command=self.confirmar_registro_paciente).pack(pady=5)

    def confirmar_registro_paciente(self):
        nombre = self.entry_nombre.get()
        cedula = self.entry_cedula.get()
        eps = self.entry_eps.get()
        try:
            paciente = Paciente(int(cedula), nombre, eps)
            self.hospital.lista_pacientes.append(paciente)
            messagebox.showinfo("Éxito", "Paciente registrado con éxito.")
        except ValueError:
            messagebox.showerror("Error", "El número de cédula debe ser un valor numérico.")

    def registrar_enfermedad(self):
        self.actualizar_frame_contenido("Registrar Enfermedad", "Ingrese los datos de la enfermedad:", [])
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        self.entry_enfermedad = ttk.Entry(self.frame_contenido)
        self.entry_enfermedad.pack(pady=5)
        self.entry_tipologia = ttk.Entry(self.frame_contenido)
        self.entry_tipologia.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Registrar", command=self.confirmar_registro_enfermedad).pack(pady=5)

    def confirmar_registro_enfermedad(self):
        cedula = self.entry_cedula.get()
        enfermedad_nombre = self.entry_enfermedad.get()
        tipologia = self.entry_tipologia.get()
        try:
            cedula = int(cedula)
            paciente = self.hospital.buscarPaciente(cedula)
            if not paciente:
                messagebox.showerror("Error", "Paciente no encontrado.")
                return
            nueva_enfermedad = Enfermedad(tipologia, enfermedad_nombre, tipologia)
            if not hasattr(paciente, "historia_clinica") or paciente.historia_clinica is None:
                paciente.historia_clinica = HistoriaClinica(paciente)
            if not hasattr(paciente.historia_clinica, "enfermedades") or paciente.historia_clinica.enfermedades is None:
                paciente.historia_clinica.enfermedades = []
            paciente.historia_clinica.enfermedades.append(nueva_enfermedad)
            messagebox.showinfo("Éxito", "Nueva enfermedad registrada exitosamente para el paciente.")
        except ValueError:
            messagebox.showerror("Error", "La cédula debe ser un número entero.")

    def eliminar_paciente(self):
        self.actualizar_frame_contenido("Eliminar Paciente", "Seleccione el paciente a eliminar:", [])
        pacientes_opciones = [f"{paciente.nombre} - {paciente.cedula}" for paciente in self.hospital.lista_pacientes]
        self.paciente_combobox = ttk.Combobox(self.frame_contenido, values=pacientes_opciones)
        self.paciente_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Eliminar", command=self.confirmar_eliminar_paciente).pack(pady=5)

    def confirmar_eliminar_paciente(self):
        paciente_seleccionado_desc = self.paciente_combobox.get()
        paciente_seleccionado = next((paciente for paciente in self.hospital.lista_pacientes if f"{paciente.nombre} - {paciente.cedula}" == paciente_seleccionado_desc), None)
        if not paciente_seleccionado:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return
        self.hospital.lista_pacientes.remove(paciente_seleccionado)
        messagebox.showinfo("Éxito", "Paciente eliminado con éxito.")

    def ver_paciente(self):
        self.actualizar_frame_contenido("Ver Paciente", "Lista de pacientes registrados:", [])
        pacientes_opciones = [f"{paciente.nombre} - {paciente.cedula}" for paciente in self.hospital.lista_pacientes]
        for paciente in pacientes_opciones:
            ttk.Label(self.frame_contenido, text=paciente).pack(pady=2)

    def mostrar_gestion_doctores(self):
        self.actualizar_frame_contenido("Gestionar Doctores", "Seleccione una opción:", [])
        opciones_doctores = ["Registrar Doctor", "Eliminar Doctor", "Ver Doctor", "Agregar Citas", "Eliminar Citas"]
        self.gestion_doctores_combobox = ttk.Combobox(self.frame_contenido, values=opciones_doctores)
        self.gestion_doctores_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.seleccionar_gestion_doctores).pack(pady=5)
    
    def seleccionar_gestion_doctores(self):
        opcion = self.gestion_doctores_combobox.get()
        if opcion == "Registrar Doctor":
            self.registrar_doctor()
        elif opcion == "Eliminar Doctor":
            self.eliminar_doctor()
        elif opcion == "Ver Doctor":
            self.ver_doctor()
        elif opcion == "Agregar Citas":
            self.agregar_citas()
        elif opcion == "Eliminar Citas":
            self.eliminar_citas()

    def registrar_doctor(self):
        self.actualizar_frame_contenido("Registrar Doctor", "Ingrese los datos del doctor:", [])
        
        ttk.Label(self.frame_contenido, text="Nombre:").pack(pady=5)
        self.entry_nombre = ttk.Entry(self.frame_contenido)
        self.entry_nombre.pack(pady=5)
        
        ttk.Label(self.frame_contenido, text="Cédula:").pack(pady=5)
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        
        ttk.Label(self.frame_contenido, text="EPS:").pack(pady=5)
        self.entry_eps = ttk.Entry(self.frame_contenido)
        self.entry_eps.pack(pady=5)
        
        ttk.Label(self.frame_contenido, text="Especialidad:").pack(pady=5)
        self.entry_especialidad = ttk.Entry(self.frame_contenido)
        self.entry_especialidad.pack(pady=5)
        
        ttk.Button(self.frame_contenido, text="Registrar", command=self.confirmar_registro_doctor).pack(pady=5)

    def confirmar_registro_doctor(self):
        nombre = self.entry_nombre.get()
        cedula = self.entry_cedula.get()
        eps = self.entry_eps.get()
        especialidad = self.entry_especialidad.get()
        try:
            doctor = Doctor(int(cedula), nombre, eps, especialidad)
            self.hospital.lista_doctores.append(doctor)
            messagebox.showinfo("Éxito", "Doctor registrado con éxito.")
        except ValueError:
            messagebox.showerror("Error", "El número de cédula debe ser un valor numérico.")

    def eliminar_doctor(self):
        self.actualizar_frame_contenido("Eliminar Doctor", "Seleccione el doctor a eliminar:", [])
        doctores_opciones = [f"{doctor.nombre} - {doctor.cedula}" for doctor in self.hospital.lista_doctores]
        self.doctor_combobox = ttk.Combobox(self.frame_contenido, values=doctores_opciones)
        self.doctor_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Eliminar", command=self.confirmar_eliminar_doctor).pack(pady=5)

    def confirmar_eliminar_doctor(self):
        doctor_seleccionado_desc = self.doctor_combobox.get()
        doctor_seleccionado = next((doctor for doctor in self.hospital.lista_doctores if f"{doctor.nombre} - {doctor.cedula}" == doctor_seleccionado_desc), None)
        if not doctor_seleccionado:
            messagebox.showerror("Error", "Doctor no encontrado.")
            return
        self.hospital.lista_doctores.remove(doctor_seleccionado)
        messagebox.showinfo("Éxito", "Doctor eliminado con éxito.")

    def ver_doctor(self):
        self.actualizar_frame_contenido("Ver Doctor", "Lista de doctores registrados:", [])
        doctores_opciones = [f"{doctor.nombre} - {doctor.cedula}" for doctor in self.hospital.lista_doctores]
        for doctor in doctores_opciones:
            ttk.Label(self.frame_contenido, text=doctor).pack(pady=2)

    def agregar_citas(self):
        self.actualizar_frame_contenido("Agregar Citas", "Ingrese los datos de la cita:", [])
        self.entry_cedula = ttk.Entry(self.frame_contenido)
        self.entry_cedula.pack(pady=5)
        self.entry_fecha = ttk.Entry(self.frame_contenido)
        self.entry_fecha.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Agregar", command=self.confirmar_agregar_citas).pack(pady=5)

    def confirmar_agregar_citas(self):
        cedula = self.entry_cedula.get()
        fecha = self.entry_fecha.get()
        try:
            cedula = int(cedula)
            doctor = self.hospital.buscar_doctor(cedula)
            if not doctor:
                messagebox.showerror("Error", "Doctor no encontrado.")
                return
            nueva_cita = Cita(doctor, fecha, None)
            doctor.agenda.append(nueva_cita)
            messagebox.showinfo("Éxito", "Cita agregada con éxito.")
        except ValueError:
            messagebox.showerror("Error", "El número de cédula debe ser un valor numérico.")

    def eliminar_citas(self):
        self.actualizar_frame_contenido("Eliminar Citas", "Seleccione la cita a eliminar:", [])
        doctores_opciones = [f"{doctor.nombre} - {doctor.cedula}" for doctor in self.hospital.lista_doctores]
        self.doctor_combobox = ttk.Combobox(self.frame_contenido, values=doctores_opciones)
        self.doctor_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Seleccionar Doctor", command=self.seleccionar_doctor_para_eliminar_citas).pack(pady=5)

    def seleccionar_doctor_para_eliminar_citas(self):
        doctor_seleccionado_desc = self.doctor_combobox.get()
        doctor_seleccionado = next((doctor for doctor in self.hospital.lista_doctores if f"{doctor.nombre} - {doctor.cedula}" == doctor_seleccionado_desc), None)
        if not doctor_seleccionado:
            messagebox.showerror("Error", "Doctor no encontrado.")
            return
        citas_disponibles = [cita for cita in doctor_seleccionado.agenda if cita.paciente is None]
        if not citas_disponibles:
            messagebox.showerror("Error", "No hay citas disponibles para eliminar.")
            return
        self.actualizar_frame_contenido("Eliminar Citas", "Seleccione la cita a eliminar:", [])
        citas_opciones = [f"{cita.fecha}" for cita in citas_disponibles]
        self.cita_combobox = ttk.Combobox(self.frame_contenido, values=citas_opciones)
        self.cita_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Eliminar", command=lambda: self.confirmar_eliminar_citas(doctor_seleccionado, citas_disponibles)).pack(pady=5)

    def confirmar_eliminar_citas(self, doctor, citas_disponibles):
        cita_seleccionada_fecha = self.cita_combobox.get()
        cita_seleccionada = next((cita for cita in citas_disponibles if cita.fecha == cita_seleccionada_fecha), None)
        if not cita_seleccionada:
            messagebox.showerror("Error", "Cita no encontrada.")
            return
        doctor.agenda.remove(cita_seleccionada)
        messagebox.showinfo("Éxito", "Cita eliminada con éxito.")

    def mostrar_gestion_vacunas(self):
        self.actualizar_frame_contenido("Gestionar Vacunas", "Seleccione una opción:", [])
        opciones_vacunas = ["Registrar Vacuna", "Eliminar Vacuna", "Ver Información de Vacuna", "Agregar Cita a Vacuna", "Eliminar Cita de Vacuna"]
        self.gestion_vacunas_combobox = ttk.Combobox(self.frame_contenido, values=opciones_vacunas)
        self.gestion_vacunas_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.seleccionar_gestion_vacunas).pack(pady=5)
    
    def seleccionar_gestion_vacunas(self):
        opcion = self.gestion_vacunas_combobox.get()
        if opcion == "Registrar Vacuna":
            self.registrar_vacuna()
        elif opcion == "Eliminar Vacuna":
            self.eliminar_vacuna()
        elif opcion == "Ver Información de Vacuna":
            self.ver_vacuna()
        elif opcion == "Agregar Cita a Vacuna":
            self.agregar_cita_vacuna()
        elif opcion == "Eliminar Cita de Vacuna":
            self.eliminar_cita_vacuna()
        else:
            messagebox.showerror("Error", "Opción inválida.")
    
    def mostrar_gestion_hospital(self):
        self.actualizar_frame_contenido("Gestionar Hospital", "Seleccione una opción:", [])
        opciones_hospital = ["Construir Habitación", "Ver Lista de Habitaciones", "Destruir Habitación", "Agregar Medicamentos", "Ver Inventario de Medicamentos", "Ver Personas Registradas", "Ver Vacunas Registradas"]
        self.gestion_hospital_combobox = ttk.Combobox(self.frame_contenido, values=opciones_hospital)
        self.gestion_hospital_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.seleccionar_gestion_hospital).pack(pady=5)
    
    def seleccionar_gestion_hospital(self):
        opcion = self.gestion_hospital_combobox.get()
        if opcion == "Construir Habitación":
            self.construir_habitacion()
        elif opcion == "Ver Lista de Habitaciones":
            self.ver_habitacion()
        elif opcion == "Destruir Habitación":
            self.destruir_habitacion()
        elif opcion == "Agregar Medicamentos":
            self.agregar_medicamentos()
        elif opcion == "Ver Inventario de Medicamentos":
            self.ver_medicamentos()
        elif opcion == "Ver Personas Registradas":
            self.ver_personas_registradas()
        elif opcion == "Ver Vacunas Registradas":
            self.ver_vacunas()
        else:
            messagebox.showerror("Error", "Opción inválida.")

    def actualizar_frame_contenido(self, titulo, descripcion, criterios_valores):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        ttk.Label(self.frame_contenido, text=titulo, font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(self.frame_contenido, text=descripcion, wraplength=400).pack(pady=5)
        
        if criterios_valores:
            frame_tabla = ttk.Frame(self.frame_contenido)
            frame_tabla.pack(pady=5)
            
            for criterio, valor in criterios_valores:
                fila = ttk.Frame(frame_tabla)
                fila.pack(fill=tk.X, pady=2)
                ttk.Label(fila, text=criterio, width=20).pack(side=tk.LEFT)
                ttk.Label(fila, text=valor, width=20).pack(side=tk.LEFT)
            
            frame_botones = ttk.Frame(self.frame_contenido)
            frame_botones.pack(pady=10)
            
            ttk.Button(frame_botones, text="Aceptar").pack(side=tk.LEFT, padx=5)
            ttk.Button(frame_botones, text="Borrar").pack(side=tk.LEFT, padx=5)

    

    def agendar_citas(self, cedula):
        from uiMain.main import agendar_citas
        self.cedula = cedula
        self.actualizar_frame_contenido("Seleccione el tipo de cita", "Seleccione el tipo de cita que requiere:", [])
        
        self.tipo_cita_combobox = ttk.Combobox(self.frame_contenido, values=["General", "Odontologia", "Oftalmologia", "--Regresar al menú--"])
        self.tipo_cita_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.seleccionar_tipo_cita).pack(pady=5)

    def seleccionar_tipo_cita(self):
        tipo_cita = self.tipo_cita_combobox.get()
        if tipo_cita not in ["General", "Odontologia", "Oftalmologia", "--Regresar al menú--"]:
            messagebox.showerror("Error", "Opción inválida.")
            return
        if tipo_cita == "--Regresar al menú--":
            self.mostrar_agendar_citas()
            return
        
        doctores_disponibles = [doc for doc in self.hospital.lista_doctores if doc.especialidad == tipo_cita]
        if not doctores_disponibles:
            messagebox.showerror("Error", "No hay doctores disponibles para la especialidad seleccionada.")
            return
        
        self.actualizar_frame_contenido("Seleccione el doctor", "Doctores disponibles:", [])
        self.doctor_combobox = ttk.Combobox(self.frame_contenido, values=[f"{doc.nombre}" for doc in doctores_disponibles] + ["--Regresar al menú--"])
        self.doctor_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.seleccionar_doctor(doctores_disponibles)).pack(pady=5)

    def seleccionar_doctor(self, doctores_disponibles):
        doctor_seleccionado_nombre = self.doctor_combobox.get()
        if doctor_seleccionado_nombre == "--Regresar al menú--":
            self.mostrar_agendar_citas()
            return
        doctor_seleccionado = next((doc for doc in doctores_disponibles if doc.nombre == doctor_seleccionado_nombre), None)
        if not doctor_seleccionado:
            messagebox.showerror("Error", "Doctor no encontrado.")
            return
        
        agenda_disponible = [cita for cita in doctor_seleccionado.agenda if cita.paciente is None]
        if not agenda_disponible:
            messagebox.showerror("Error", "El doctor seleccionado no tiene citas disponibles.")
            return
        
        self.actualizar_frame_contenido("Seleccione la cita", "Citas disponibles:", [])
        self.cita_combobox = ttk.Combobox(self.frame_contenido, values=[f"{cita.fecha}" for cita in agenda_disponible])
        self.cita_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.confirmar_cita(doctor_seleccionado, agenda_disponible)).pack(pady=5)

    def confirmar_cita(self, doctor_seleccionado, agenda_disponible):
        cita_seleccionada_fecha = self.cita_combobox.get()
        cita_seleccionada = next((cita for cita in agenda_disponible if cita.fecha == cita_seleccionada_fecha), None)
        if not cita_seleccionada:
            messagebox.showerror("Error", "Cita no encontrada.")
            return
        
        paciente = self.hospital.buscarPaciente(int(self.cedula))
        cita_seleccionada.paciente = paciente
        messagebox.showinfo("Éxito", f"Cita agendada con éxito para {cita_seleccionada.fecha} con {doctor_seleccionado.nombre}.")
        self.mostrar_agendar_citas()


    
    def generar_formulas_medicas(self, cedula):
        self.cedula = cedula
        paciente = self.hospital.buscarPaciente(int(cedula))
        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return
        if not hasattr(paciente, "historia_clinica") or not paciente.historia_clinica.enfermedades:
            messagebox.showerror("Error", "No hay enfermedades registradas. Diríjase a la opción de registrar enfermedad.")
            return
        
        # Paso 1: Elegir la enfermedad a tratar
        self.actualizar_frame_contenido("Generar Fórmula Médica", "Seleccione la enfermedad a tratar:", [])
        enfermedades_disponibles = [f"{idx+1}. {enfermedad.nombre} - {enfermedad.tipologia}" 
                                    for idx, enfermedad in enumerate(paciente.historia_clinica.enfermedades)]
        self.enfermedad_combobox = ttk.Combobox(self.frame_contenido, values=enfermedades_disponibles, state="readonly")
        self.enfermedad_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Siguiente", command=self.seleccionar_enfermedad).pack(pady=5)
    
    def seleccionar_enfermedad(self):
        seleccion = self.enfermedad_combobox.get()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar una enfermedad.")
            return
        # Suponiendo que el formato es "índice. nombre - tipología"
        try:
            idx = int(seleccion.split('.')[0]) - 1
        except Exception as e:
            messagebox.showerror("Error", "Selección de enfermedad inválida.")
            return
        
        paciente = self.hospital.buscarPaciente(int(self.cedula))
        self.enfermedad_seleccionada = paciente.historia_clinica.enfermedades[idx]
        
        # Paso 2: Seleccionar el doctor (filtrar por tipología de la enfermedad)
        doctores_disponibles = [doc for doc in self.hospital.lista_doctores if doc.especialidad == self.enfermedad_seleccionada.tipologia]
        if not doctores_disponibles:
            messagebox.showerror("Error", f"No hay doctores disponibles para la especialidad {self.enfermedad_seleccionada.tipologia}.")
            return
        
        self.actualizar_frame_contenido("Generar Fórmula Médica", 
                                        f"Doctor(es) disponibles para tratar {self.enfermedad_seleccionada.nombre} ({self.enfermedad_seleccionada.tipologia}):", [])
        self.doctor_combobox = ttk.Combobox(self.frame_contenido, 
                                             values=[f"{idx+1}. {doc.nombre}" for idx, doc in enumerate(doctores_disponibles)],
                                             state="readonly")
        self.doctor_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Siguiente", command=lambda: self.seleccionar_doctor(doctores_disponibles)).pack(pady=5)
    
    def seleccionar_doctor(self, doctores_disponibles):
        seleccion = self.doctor_combobox.get()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un doctor.")
            return
        try:
            idx = int(seleccion.split('.')[0]) - 1
        except Exception as e:
            messagebox.showerror("Error", "Selección de doctor inválida.")
            return
        
        self.doctor_seleccionado = doctores_disponibles[idx]
        
        # Paso 3: Seleccionar medicamentos (se puede agregar más de uno)
        self.medicamentos_seleccionados = []
        self.actualizar_frame_contenido("Generar Fórmula Médica", 
                                        f"Medicamentos disponibles para tratar {self.enfermedad_seleccionada.nombre}:", [])
        # Filtrar medicamentos; por ejemplo, se muestran todos o se filtran por enfermedad si aplica.
        self.medicamentos_disponibles = self.hospital.lista_medicamentos  
        self.medicamento_combobox = ttk.Combobox(self.frame_contenido, 
                                                 values=[f"{idx+1}. {med.nombre}" for idx, med in enumerate(self.medicamentos_disponibles)],
                                                 state="readonly")
        self.medicamento_combobox.pack(pady=5)
        frame_botones = ttk.Frame(self.frame_contenido)
        frame_botones.pack(pady=5)
        ttk.Button(frame_botones, text="Agregar Medicamento", command=self.agregar_medicamento).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Terminar", command=self.confirmar_formula_final).pack(side=tk.LEFT, padx=5)
        # Mostrar lista de medicamentos seleccionados
        self.label_meds = ttk.Label(self.frame_contenido, text="Medicamentos agregados: Ninguno")
        self.label_meds.pack(pady=5)
    
    def agregar_medicamento(self):
        seleccion = self.medicamento_combobox.get()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un medicamento.")
            return
        try:
            idx = int(seleccion.split('.')[0]) - 1
        except Exception as e:
            messagebox.showerror("Error", "Selección de medicamento inválida.")
            return
        medicamento = self.medicamentos_disponibles[idx]
        self.medicamentos_seleccionados.append(medicamento)
        messagebox.showinfo("Éxito", f"Medicamento '{medicamento.nombre}' agregado.")
        # Actualizar la etiqueta con la lista de medicamentos seleccionados
        meds_str = ", ".join([med.nombre for med in self.medicamentos_seleccionados])
        self.label_meds.config(text=f"Medicamentos agregados: {meds_str}")
    
    def confirmar_formula_final(self):
        # Calcular costo total: por ejemplo, sumar los precios de los medicamentos
        total = sum(med.precio for med in self.medicamentos_seleccionados)
        paciente = self.hospital.buscarPaciente(int(self.cedula))
        formula_text = (f"FÓRMULA MÉDICA GENERADA:\n"
                        f"Fórmula para {paciente.nombre}, Doctor: {self.doctor_seleccionado.nombre},\n"
                        f"Medicamentos: {', '.join([med.nombre for med in self.medicamentos_seleccionados])}\n"
                        f"Precio total de la fórmula: {total}")
        messagebox.showinfo("Fórmula Médica", formula_text)
        # Aquí se podría guardar la fórmula en la historia clínica u otra estructura según lo requiera la lógica del programa.
        
        messagebox.showinfo("Éxito", f"Fórmula médica '{formula_seleccionada}' generada con éxito para la cédula {self.cedula}.")

    def asignar_habitaciones(self, cedula):
        from uiMain.main import asignar_habitacion
        self.cedula = cedula
        self.actualizar_frame_contenido("Seleccione la habitación", "Seleccione la habitación que desea asignar:", [])
        
        # Obtener las habitaciones disponibles desde la lógica del programa
        paciente = self.hospital.buscarPaciente(int(cedula))
        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return
        
        habitaciones_disponibles = [h for h in self.hospital.habitaciones if not h.ocupada]
        if not habitaciones_disponibles:
            messagebox.showerror("Error", "No hay habitaciones disponibles en el momento.")
            return
        
        habitaciones_opciones = [f"Número: {h.numero}, Categoría: {h.categoria.name}" for h in habitaciones_disponibles]
        self.habitacion_combobox = ttk.Combobox(self.frame_contenido, values=habitaciones_opciones)
        self.habitacion_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.confirmar_habitacion(habitaciones_disponibles)).pack(pady=5)



    def confirmar_habitacion(self, habitaciones_disponibles):
        habitacion_seleccionada_desc = self.habitacion_combobox.get()
        habitacion_seleccionada = next((h for h in habitaciones_disponibles 
                                        if f"Número: {h.numero}, Categoría: {h.categoria.name}" == habitacion_seleccionada_desc), None)
        if not habitacion_seleccionada:
            messagebox.showerror("Error", "Habitación no encontrada.")
            return

        # Solicitar el número de días mediante un diálogo de entrada
        dias = simpledialog.askinteger("Días de hospedaje", "Ingrese la cantidad de días de hospedaje:")
        if dias is None:
            messagebox.showerror("Error", "Debe ingresar un número de días válido.")
            return

        # Asignar la habitación al paciente y marcarla como ocupada
        paciente = self.hospital.buscarPaciente(int(self.cedula))
        habitacion_seleccionada.paciente = paciente
        habitacion_seleccionada.ocupada = True
        habitacion_seleccionada.dias = dias
        paciente.habitacion_asignada = habitacion_seleccionada

        # Calcular el costo: costo = días * valor de la categoría (definido en CategoriaHabitacion)
        costo_total = dias * habitacion_seleccionada.categoria.get_valor()
        messagebox.showinfo("Éxito", f"Habitación asignada con éxito.\nPaciente: {paciente.nombre}\n"
                                    f"Habitación número: {habitacion_seleccionada.numero}\n"
                                    f"Categoría: {habitacion_seleccionada.categoria.name}\n"
                                    f"Días de hospedaje: {dias}\nCosto total: {costo_total}")
            
            # Calcular el costo: costo = días * valor de la categoría (definido en CategoriaHabitacion)
        costo_total = dias * habitacion_seleccionada.categoria.get_valor()
        messagebox.showinfo("Éxito", f"Habitación asignada con éxito.\nPaciente: {paciente.nombre}\n"
                                    f"Habitación número: {habitacion_seleccionada.numero}\n"
                                    f"Categoría: {habitacion_seleccionada.categoria.name}\n"
                                    f"Días de hospedaje: {dias}\nCosto total: {costo_total}")
    def aplicar_vacunas(self, cedula):
        self.cedula = cedula
        self.actualizar_frame_contenido("Seleccione el tipo de vacuna", "Seleccione el tipo de vacuna que desea aplicar:", [])
        
        self.tipo_vacuna_combobox = ttk.Combobox(self.frame_contenido, values=["Obligatoria", "No Obligatoria"])
        self.tipo_vacuna_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.seleccionar_tipo_vacuna).pack(pady=5)

    def seleccionar_tipo_vacuna(self):
        tipo_vacuna = self.tipo_vacuna_combobox.get()
        if tipo_vacuna not in ["Obligatoria", "No Obligatoria"]:
            messagebox.showerror("Error", "Opción inválida.")
            return
        
        vacunas_disponibles = [vacuna for vacuna in self.hospital.lista_vacunas if vacuna.tipo == tipo_vacuna]
        if not vacunas_disponibles:
            messagebox.showerror("Error", f"No hay vacunas {tipo_vacuna.lower()}s disponibles en el momento.")
            return
        
        self.actualizar_frame_contenido("Seleccione la vacuna", "Vacunas disponibles:", [])
        self.vacuna_combobox = ttk.Combobox(self.frame_contenido, values=[vacuna.nombre for vacuna in vacunas_disponibles])
        self.vacuna_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.confirmar_vacuna(vacunas_disponibles)).pack(pady=5)

    def confirmar_vacuna(self, vacunas_disponibles):
        vacuna_seleccionada_nombre = self.vacuna_combobox.get()
        vacuna_seleccionada = next((vacuna for vacuna in vacunas_disponibles if vacuna.nombre == vacuna_seleccionada_nombre), None)
        if not vacuna_seleccionada:
            messagebox.showerror("Error", "Vacuna no encontrada.")
            return
        
        paciente = self.hospital.buscarPaciente(int(self.cedula))
        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return

        # Mostrar la agenda disponible para la vacuna seleccionada
        agenda_disponible = vacuna_seleccionada.mostrar_agenda_disponible()
        if not agenda_disponible:
            messagebox.showerror("Error", "No hay citas disponibles para esta vacuna.")
            return

        self.actualizar_frame_contenido("Seleccione la cita", "Citas disponibles:", [])
        self.cita_combobox = ttk.Combobox(self.frame_contenido, values=[cita.get_fecha() for cita in agenda_disponible])
        self.cita_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.confirmar_cita_vacuna(vacuna_seleccionada, agenda_disponible)).pack(pady=5)

    def confirmar_cita_vacuna(self, vacuna_seleccionada, agenda_disponible):
        fecha_cita = self.cita_combobox.get()
        cita_seleccionada = next((cita for cita in agenda_disponible if cita.get_fecha() == fecha_cita), None)
        if not cita_seleccionada:
            messagebox.showerror("Error", "Cita no encontrada.")
            return

        paciente = self.hospital.buscarPaciente(int(self.cedula))
        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return

        # Asignar la cita al paciente
        cita_seleccionada.paciente = paciente

        # Actualizar el historial de vacunas del paciente
        if not hasattr(paciente, "historia_clinica"):
            paciente.historia_clinica = type("HistoriaClinica", (), {"historial_vacunas": []})()
        paciente.historia_clinica.historial_vacunas.append(cita_seleccionada)

        # Agregar el costo de la vacuna a la lista de servicios del paciente
        if not hasattr(paciente, "servicios"):
            paciente.servicios = []
        paciente.servicios.append(("Vacuna", vacuna_seleccionada.precio))

        messagebox.showinfo("Éxito", f"Vacuna '{vacuna_seleccionada.nombre}' aplicada con éxito para la cédula {self.cedula}.\nCita: {cita_seleccionada.get_fecha()}\nCosto: {vacuna_seleccionada.precio}")

    def facturacion(self, cedula):
        try:
            cedula = int(cedula)
        except ValueError:
            messagebox.showerror("Error", "Cédula inválida.")
            return

        paciente = self.hospital.buscarPaciente(cedula)
        if paciente is None:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return

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
            messagebox.showinfo("Información", "No se encontraron servicios facturables para este paciente.")
            return

        factura_detalle = "\n".join([f"{idx+1}. {desc} -- Costo: {costo}" 
                                    for idx, (desc, costo) in enumerate(servicios)])
        factura_info = (f"--- Facturación para {paciente.nombre} ---\n\n"
                        f"Servicios facturados:\n{factura_detalle}\n\n"
                        f"Total a pagar: {total}")

        # Mostrar la factura en una ventana y preguntar si se desea pagar
        proceder_pago = messagebox.askyesno("Factura Detallada", f"{factura_info}\n\n¿Desea proceder con el pago?")
        if proceder_pago:
            # Aquí se incluye la lógica de pago, si es necesaria.
            messagebox.showinfo("Pago", "Pago realizado con éxito.")
        else:
            messagebox.showinfo("Pago", "Pago cancelado.")
    def ver_vacuna(self):
        self.actualizar_frame_contenido("Ver Información de Vacuna", "Seleccione la vacuna:", [])
        
        vacunas_disponibles = [vacuna.nombre for vacuna in self.hospital.lista_vacunas]
        self.vacuna_combobox = ttk.Combobox(self.frame_contenido, values=vacunas_disponibles)
        self.vacuna_combobox.pack(pady=5)
        
        ttk.Button(self.frame_contenido, text="Ver", command=self.confirmar_ver_vacuna).pack(pady=5)

    def confirmar_ver_vacuna(self):
        nombre = self.vacuna_combobox.get()
        vacuna = self.hospital.buscar_vacuna(nombre)
        if vacuna is None:
            messagebox.showerror("Error", "Esta vacuna no existe en el inventario del hospital.")
        else:
            info = f"Nombre: {vacuna.nombre}\nTipo: {vacuna.tipo}\nPrecio: {vacuna.precio}\nEPS disponibles: {', '.join(vacuna.tipo_eps)}"
            messagebox.showinfo("Información de Vacuna", info)

    def agregar_cita_vacuna(self):
        self.actualizar_frame_contenido("Agregar Cita a Vacuna", "Ingrese los datos de la cita:", [])
        
        ttk.Label(self.frame_contenido, text="Nombre de la vacuna:").pack(pady=5)
        self.entry_nombre_vacuna = ttk.Entry(self.frame_contenido)
        self.entry_nombre_vacuna.pack(pady=5)
        
        ttk.Label(self.frame_contenido, text="Fecha de la cita (Ej: '6 de Marzo, 9:00 am'):").pack(pady=5)
        self.entry_fecha_cita = ttk.Entry(self.frame_contenido)
        self.entry_fecha_cita.pack(pady=5)
        
        ttk.Button(self.frame_contenido, text="Agregar", command=self.confirmar_agregar_cita_vacuna).pack(pady=5)

    def confirmar_agregar_cita_vacuna(self):
        nombre = self.entry_nombre_vacuna.get()
        fecha = self.entry_fecha_cita.get()
        vacuna = self.hospital.buscar_vacuna(nombre)
        if vacuna is None:
            messagebox.showerror("Error", "Esta vacuna no existe en el inventario del hospital.")
            return
        nueva_cita = CitaVacuna(fecha, None, vacuna)
        vacuna.agenda.append(nueva_cita)
        messagebox.showinfo("Éxito", "Nueva cita agregada con éxito a la vacuna.")

    def eliminar_cita_vacuna(self):
        self.actualizar_frame_contenido("Eliminar Cita de Vacuna", "Ingrese los datos de la cita:", [])
        
        ttk.Label(self.frame_contenido, text="Nombre de la vacuna:").pack(pady=5)
        self.entry_nombre_vacuna = ttk.Entry(self.frame_contenido)
        self.entry_nombre_vacuna.pack(pady=5)
        
        ttk.Button(self.frame_contenido, text="Ver Citas", command=self.confirmar_ver_citas_vacuna).pack(pady=5)

    def confirmar_ver_citas_vacuna(self):
        nombre = self.entry_nombre_vacuna.get()
        vacuna = self.hospital.buscar_vacuna(nombre)
        if vacuna is None:
            messagebox.showerror("Error", "Esta vacuna no existe en el inventario del hospital.")
            return
        citas_disponibles = vacuna.mostrar_agenda_disponible()
        if not citas_disponibles:
            messagebox.showerror("Error", "No hay citas disponibles para eliminar en esta vacuna.")
            return
        self.actualizar_frame_contenido("Eliminar Cita de Vacuna", "Seleccione la cita a eliminar:", [])
        self.cita_combobox = ttk.Combobox(self.frame_contenido, values=[cita.get_fecha() for cita in citas_disponibles])
        self.cita_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Eliminar", command=lambda: self.confirmar_eliminar_cita_vacuna(vacuna, citas_disponibles)).pack(pady=5)

    def confirmar_eliminar_cita_vacuna(self, vacuna, citas_disponibles):
        fecha_cita = self.cita_combobox.get()
        cita_a_eliminar = next((cita for cita in citas_disponibles if cita.get_fecha() == fecha_cita), None)
        if cita_a_eliminar:
            vacuna.agenda.remove(cita_a_eliminar)
            messagebox.showinfo("Éxito", "¡Cita eliminada con éxito!")
        else:
            messagebox.showerror("Error", "Cita no encontrada.")

    def ver_vacunas(self):
        self.actualizar_frame_contenido("Vacunas Registradas", "Vacunas disponibles:", [])
        vacunas = self.hospital.lista_vacunas
        if vacunas:
            for vacuna in vacunas:
                ttk.Label(self.frame_contenido, text=f"Nombre: {vacuna.nombre}, Tipo: {vacuna.tipo}, Precio: {vacuna.precio}").pack(pady=5)
        else:
            ttk.Label(self.frame_contenido, text="No hay vacunas registradas.").pack(pady=5)

