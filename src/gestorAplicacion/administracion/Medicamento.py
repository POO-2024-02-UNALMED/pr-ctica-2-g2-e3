class Medicamento:
    def __init__(self, nombre: str, enfermedad, descripcion: str, cantidad: int, precio: float):
        self.nombre = nombre
        self.enfermedad = enfermedad
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio
    
    def eliminar_cantidad(self):
        self.cantidad -= 1
    
    @property
    def get_nombre(self) -> str:
        return self.nombre
    
    @get_nombre.setter
    def set_nombre(self, nombre: str):
        self.nombre = nombre
    
    @property
    def get_enfermedad(self):
        return self.enfermedad
    
    @get_enfermedad.setter
    def set_enfermedad(self, enfermedad):
        self.enfermedad = enfermedad
    
    @property
    def get_descripcion(self) -> str:
        return self.descripcion
    
    @get_descripcion.setter
    def set_descripcion(self, descripcion: str):
        self.descripcion = descripcion
    
    @property
    def get_cantidad(self) -> int:
        return self.cantidad
    
    @get_cantidad.setter
    def set_cantidad(self, cantidad: int):
        self.cantidad = cantidad
    
    @property
    def get_precio(self) -> float:
        return self.precio
    
    @get_precio.setter
    def set_precio(self, precio: float):
        self.precio = precio
    
    def __str__(self) -> str:
        return f"Nombre: {self.nombre}, Enfermedad: {self.enfermedad.nombre} {self.enfermedad.tipologia}, Descripcion: {self.descripcion}"