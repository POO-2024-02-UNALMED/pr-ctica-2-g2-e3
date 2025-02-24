import tkinter as tk
from tkinter import ttk, Menu, messagebox
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk  # Importar Pillow

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
        self.images = [self.load_image(os.path.join(self.image_folder, f"image{i}.png")) for i in range(1, 7)]
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
        menu_procesos.add_command(label="Agendar Citas", command=self.agendar_citas)
        menu_procesos.add_command(label="Generar Fórmulas Médicas", command=self.generar_formulas_medicas)
        menu_procesos.add_command(label="Asignar Habitaciones", command=self.asignar_habitaciones)
        menu_procesos.add_command(label="Aplicación de Vacunas", command=self.aplicar_vacunas)
        menu_procesos.add_command(label="Facturación", command=self.facturacion)
        
        menu_ayuda = Menu(self.menu_bar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_autores)
        
        self.menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
        self.menu_bar.add_cascade(label="Procesos y Consultas", menu=menu_procesos)
        self.menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
        
        self.frame_contenido = ttk.Frame(self, borderwidth=2, relief="ridge")
        self.frame_contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(self.frame_contenido, text="Seleccione una opción del menú", font=("Arial", 12, "bold")).pack(pady=5)
    
    def mostrar_info_app(self):
        messagebox.showinfo("Aplicación", "Sistema de Gestión Hospitalaria: Gestión de pacientes, doctores y servicios médicos.")
    
    def mostrar_autores(self):
        messagebox.showinfo("Acerca de", "Autores: Samuel Gutierrez, Samuel Garcia, Samuel Botero")

    def agendar_citas(self):
        from uiMain.main import agendar_citas
        agendar_citas(self.hospital)

    def generar_formulas_medicas(self):
        from uiMain.main import formula_medica
        formula_medica(self.hospital)

    def asignar_habitaciones(self):
        from uiMain.main import asignar_habitacion
        asignar_habitacion(self.hospital)

    def aplicar_vacunas(self):
        from uiMain.main import vacunacion
        vacunacion(self.hospital)

    def facturacion(self):
        from uiMain.main import facturacion
        facturacion(self.hospital)
