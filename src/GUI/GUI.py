import tkinter as tk
from tkinter import ttk, Menu, messagebox

class Inicio(ttk.Frame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.frame_menu = ttk.Frame(self.container, borderwidth=2, relief="ridge")
        self.frame_menu.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ttk.Label(self.frame_menu, text="Bienvenido al Sistema de Gestión Hospitalaria", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.frame_menu, text="Ingresar", command=switch_callback).pack(pady=10)
        
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

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
        messagebox.showinfo("Acerca de", "Autores: [Nombres de los desarrolladores]")

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
