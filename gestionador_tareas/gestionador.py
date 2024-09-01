import datetime
import logging
import json
from models import Tarea, Cuenta
from etiquetas import *

# Configuración de logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ARCHIVO_TAREAS = 'tareas.json'

def cargar_tareas():
    try:
        with open(ARCHIVO_TAREAS, 'r') as file:
            tareas_data = json.load(file)
            return [Tarea.from_dict(t) for t in tareas_data]
    except FileNotFoundError as e:
        logging.warning(f"Archivo de tareas no encontrado, se creara uno nuevo: {e}")
        print(f"Archivo de tareas no encontrado, se creara uno nuevo: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error al leer el archivo de tareas: {e}")
        print(f"Error al leer el archivo de tareas: {e}")
        return []
    
def guardar_tarea(tarea):
    try:
        tareas = cargar_tareas()
        with open(ARCHIVO_TAREAS, 'w') as file:
            tareas.append(tarea)
            json.dump([t.to_dict() for t in tareas], file, indent=4)
            logging.info("Tarea guardada correctamente.")
    except Exception as e:
        logging.error(f"Error al guardar la tarea: {e}")
        print(f"Error al guardar la tarea: {e}")

def crear_tarea(usuario):
    try:
        titulo = input("Ingrese el título de la tarea: ")
        descr = input("Ingrese la descripción de la tarea: ")

        # Fecha por defecto 1 mes después de la fecha de creación o se puede ingresar manualmente
        fecha_default = (datetime.datetime.now() + datetime.timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_str = input(f"Ingrese la fecha de vencimiento (YYYY-MM-DD HH:MM) o presione Enter para la fecha por defecto ({fecha_default}): ")
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M') if fecha_str else fecha_default

        etiquetas = cargar_etiquetas()
        tipo = obtener_etiqueta(etiquetas)

        tarea = Tarea(titulo, descr, fecha, tipo, usuario=usuario)
        logging.info(f"Tarea creada por usuario {usuario}: {tarea.titulo}")

        guardar_tarea(tarea)  # Guardar automáticamente después de crear
        print("Tarea creada y guardada con éxito.")
    except Exception as e:
        logging.error(f"Error al crear la tarea: {e}")
        print(f"Error: No se pudo crear la tarea. Verifique los datos ingresados: {e}")
        return None

cuenta = Cuenta(
    usuario="Test",
    nombre="Testing_c"
)

print("Bienvenido al gestionador de tareas")
print("Seleccione accion: ")
print("1) Mostrar cuenta")
print("2) Crear tarea")
print("3) Mostrar tareas")
print("Escriba el numero a seleccionar: ")
eleccion = input()

if eleccion == "1":
    cuenta.ver_datos()
elif eleccion == "2":
    crear_tarea(cuenta.usuario)
elif eleccion == "3":
    tareas = cargar_tareas()
    for tarea in tareas:
        tarea.VerTarea()
else:
    print("No existe tal accion!")