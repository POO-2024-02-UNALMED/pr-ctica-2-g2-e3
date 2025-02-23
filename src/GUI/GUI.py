import tkinter as tk
from tkinter import ttk, PhotoImage
import os

class Inicio(ttk.Frame):
    def __init__(self, parent, switch_callback):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        
        # Main container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (Menu)
        self.frame_menu = ttk.Frame(self.container, borderwidth=2, relief="ridge")
        self.frame_menu.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ttk.Label(self.frame_menu, text="Menu Inicio", font=("Arial", 14)).pack(pady=10)
        self.texto_hoja_vida = ttk.Label(self.frame_menu, text="[Hoja de vida del desarrollador]", wraplength=200)
        self.texto_hoja_vida.pack(pady=10)
        
        image_folder = os.path.join(os.path.dirname(__file__), "archivos")
        self.image_index = 0
        self.images = []
        
        for i in range(1, 6):
            filename = os.path.join(image_folder, f"image{i}.png")
            if os.path.exists(filename):
                self.images.append(PhotoImage(file=filename))
        
        if self.images:
            self.label_image = ttk.Label(self.frame_menu, image=self.images[self.image_index])
            self.label_image.pack(pady=10)
            self.label_image.bind("<Enter>", self.change_image)
        else:
            self.label_image = ttk.Label(self.frame_menu, text="No images found")
            self.label_image.pack(pady=10)
        
        ttk.Button(self.frame_menu, text="Ingresar", command=switch_callback).pack(pady=10)
        
        # Right panel (Scene)
        self.frame_scene = ttk.Frame(self.container, borderwidth=2, relief="ridge")
        self.frame_scene.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ttk.Label(self.frame_scene, text="Scene", font=("Arial", 14)).pack(pady=10)
        
        # Adjust grid proportions
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=2)
        self.container.rowconfigure(0, weight=1)

    def change_image(self, event):
        if self.images:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.label_image.configure(image=self.images[self.image_index])

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
        
        ttk.Label(self, text="Ventana Principal", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Gestión de Pacientes", command=self.gestion_pacientes).pack(pady=10)
        ttk.Button(self, text="Gestión de Doctores", command=self.gestion_doctores).pack(pady=10)
        
    def gestion_pacientes(self):
        print("Lógica de gestión de pacientes aquí")
    
    def gestion_doctores(self):
        print("Lógica de gestión de doctores aquí")
