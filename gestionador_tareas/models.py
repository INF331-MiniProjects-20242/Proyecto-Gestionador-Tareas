import datetime

class Tarea:
    titulo: str
    descr: str
    fecha: datetime
    tipo: str #Equivalente a etiqueta
    estado: int # estado = 0 equivale a en progreso y = 1 completada
    usuario: str # Usuario quien ingresa tarea

    def __init__(self, titulo: str, descr: str, fecha: datetime, tipo: str, estado: int = 0, usuario: str = None):
        self.titulo = titulo
        self.descr = descr
        self.fecha = fecha
        self.tipo = tipo
        self.estado = estado
        self.usuario = usuario

    def VerTarea(self):
        print("Titulo: ", self.titulo)
        print("Descripcion: ", self.descr)
        print("Fecha Limite: ", self.fecha)
        print("Tipo/Etiqueta: ", self.tipo)
        print("Usuario: ", self.usuario)
        msg_estado = ""
        if self.estado == 0:
            msg_estado = "En progreso..."
        elif self.estado == -1:
            msg_estado = "Atrasado"
        else:
            msg_estado= "Completada!"
        print(f"Estado: {msg_estado}")
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descr": self.descr,
            "fecha": self.fecha.isoformat(),
            "tipo": self.tipo,
            "estado": self.estado,
            "usuario": self.usuario
        }

    @staticmethod
    def from_dict(data):
        fecha = datetime.datetime.fromisoformat(data['fecha'])
        return Tarea(data['titulo'], data['descr'], fecha, data['tipo'], data['estado'], data['usuario'])

class Cuenta:
    usuario: str
    nombre: str
    #contrasena: str  #Puede ser inseguro agregar este campo directamente a la clase


    def __init__(self, usuario: str, nombre: str):
        self.usuario = usuario
        self.nombre = nombre

    def ver_datos(self):
        print("Usuario: ", self.usuario)
        print("Nombre: ", self.nombre)