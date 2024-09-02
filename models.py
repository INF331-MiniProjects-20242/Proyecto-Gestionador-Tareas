import datetime

class Tarea:
    titulo: str
    descr: str
    fecha: datetime
    tipo: str #Equivalente a etiqueta
    estado: int # estado = 0 equivale a en progreso y = 1 completada

    def __init__(self, titulo: str, descr: str, fecha: datetime, tipo: str, estado: int = 0):
        self.titulo = titulo
        self.descr = descr
        self.fecha = fecha
        self.tipo = tipo
        self.estado = estado

    def VerTarea(self):
        print("Titulo: ", self.titulo)
        print("Descripcion: ", self.descr)
        print("Fecha Limite: ", self.fecha)
        print("Tipo/Etiqueta: ", self.tipo)
        if self.estado == 0:
            print("En progreso...")
        else:
            print("Completada!")

class Cuenta:
    usuario: str
    nombre: str
    contrasena: str


    def __init__(self, usuario: str, nombre: str, contrasena: str):
        self.usuario = usuario
        self.nombre = nombre
        self.contrasena = contrasena

    def ver_datos(self):
        print("Usuario: ", self.usuario)
        print("Nombre: ", self.nombre)