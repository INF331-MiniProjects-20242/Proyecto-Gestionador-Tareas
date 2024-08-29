import datetime
from models import Tarea, Cuenta

cuentas = Cuenta(
    usuario="Test",
    nombre="Testing_c"
)

tarea1 = Tarea(
    titulo="Completar proyecto",
    descr="Finalizar el proyecto de Python",
    fecha= datetime.datetime(2024, 8, 29, 12, 0),
    tipo="Trabajo",
    estado=0
)

print("Bienvenido al gestionador de tareas")
print("Seleccione accion: ")
print("1) Mostrar cuenta")
print("2) Mostrar tarea")
print("Escriba el numero a seleccionar: ")
eleccion = input()

if eleccion == "1":
    cuentas.ver_datos()
elif eleccion == "2":
    tarea1.VerTarea()
else:
    print("No existe tal accion!")