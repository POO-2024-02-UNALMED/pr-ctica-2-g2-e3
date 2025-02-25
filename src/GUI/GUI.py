import tkinter as tk
from tkinter import ttk, Menu, messagebox
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk  # Importar Pillow
from gestorAplicacion.administracion.Hospital import Hospital
from gestorAplicacion.servicios.CitaVacuna import CitaVacuna

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
            "Desarrollador 2: Info",
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
        
        menu_ayuda = Menu(self.menu_bar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_autores)
        
        self.menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
        self.menu_bar.add_cascade(menu=menu_procesos, label="Procesos y Consultas")
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
    
    def mostrar_generar_formulas_medicas(self):
        self.actualizar_frame_contenido("Generar Fórmulas Médicas", "Ingrese el número de cédula del paciente:", [])
    
    def mostrar_asignar_habitaciones(self):
        self.actualizar_frame_contenido("Asignar Habitaciones", "Ingrese el número de cédula del paciente:", [])
    
    def mostrar_aplicar_vacunas(self):
        self.actualizar_frame_contenido("Aplicación de Vacunas", "Ingrese el número de cédula del paciente:", [])
    
    def mostrar_facturacion(self):
        self.actualizar_frame_contenido("Facturación", "Ingrese el número de cédula del paciente:", [])

    def actualizar_frame_contenido(self, titulo, descripcion, criterios_valores):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        ttk.Label(self.frame_contenido, text=titulo, font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(self.frame_contenido, text=descripcion, wraplength=400).pack(pady=5)
        
        if titulo in ["Agendar Citas", "Generar Fórmulas Médicas", "Asignar Habitaciones", "Aplicación de Vacunas", "Facturación"]:
            self.entry_cedula = ttk.Entry(self.frame_contenido)
            self.entry_cedula.pack(pady=5)
            ttk.Button(self.frame_contenido, text="Aceptar", command=lambda: self.obtener_cedula(titulo)).pack(pady=5)
        else:
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

    def obtener_cedula(self, titulo):
        cedula = self.entry_cedula.get()
        if not cedula:
            messagebox.showerror("Error", "Por favor ingrese un número de cédula.")
            return
        
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
        from uiMain.main import formula_medica
        self.cedula = cedula
        self.actualizar_frame_contenido("Seleccione la fórmula médica", "Seleccione la fórmula médica que requiere:", [])
        
        # Obtener las opciones de fórmulas médicas desde la lógica del programa
        paciente = self.hospital.buscarPaciente(int(cedula))
        if not paciente:
            messagebox.showerror("Error", "Paciente no encontrado.")
            return
        
        if not paciente.historia_clinica.enfermedades:
            messagebox.showerror("Error", "No hay enfermedades registradas. Diríjase a la opción de registrar enfermedad.")
            return
        
        enfermedades_disponibles = [f"{enfermedad.nombre} - {enfermedad.tipologia}" for enfermedad in paciente.historia_clinica.enfermedades]
        self.formula_combobox = ttk.Combobox(self.frame_contenido, values=enfermedades_disponibles)
        self.formula_combobox.pack(pady=5)
        ttk.Button(self.frame_contenido, text="Aceptar", command=self.confirmar_formula_medica).pack(pady=5)

    def confirmar_formula_medica(self):
        formula_seleccionada = self.formula_combobox.get()
        if not formula_seleccionada:
            messagebox.showerror("Error", "Por favor seleccione una fórmula médica.")
            return
        
        messagebox.showinfo("Éxito", f"Fórmula médica '{formula_seleccionada}' generada con éxito para la cédula {self.cedula}.")

    def asignar_habitaciones(self, cedula):
        from uiMain.main import asignar_habitacion
        asignar_habitacion(self.hospital, cedula)

    def aplicar_vacunas(self, cedula):
        from uiMain.main import vacunacion
        vacunacion(self.hospital, cedula)

    def facturacion(self, cedula):
        from uiMain.main import facturacion
        facturacion(self.hospital, cedula)
