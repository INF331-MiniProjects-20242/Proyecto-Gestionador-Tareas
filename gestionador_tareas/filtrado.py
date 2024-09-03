import datetime
import json
import logging
from models import Tarea, Cuenta

ARCHIVO_TAREAS = "tareas.json"
LOG_FILE = "app.log"

# Configuración de logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cargar_tareas():
    tareas = []
    try:
        with open(ARCHIVO_TAREAS, 'r') as file:
            tareas_data = json.load(file)
            for data in tareas_data:
                tarea = Tarea.from_dict(data)
                tareas.append(tarea)
        logging.info("Tareas cargadas exitosamente.")
    except json.JSONDecodeError as e:
        logging.error(f"Error al leer el archivo de tareas: {e}")
    except FileNotFoundError:
        logging.warning("Archivo de tareas no encontrado, se creará uno nuevo al guardar tareas.")
    except Exception as e:
        logging.error(f"Error inesperado al cargar tareas: {e}")
    return tareas


def filtrar_por_rango_fechas(tareas, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_obj = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        if fecha_inicio_obj > fecha_fin_obj:
            logging.error(f"El rango de fechas es invalido: fecha_inicio ({fecha_inicio}) es mayor que fecha_fin ({fecha_fin})")
            print("Error: La fecha de inicio no puede ser mayor que la fecha de fin.")
            return []

        filtradas = [tarea for tarea in tareas if fecha_inicio_obj <= tarea.fecha <= fecha_fin_obj]
        logging.info(f"Filtradas {len(filtradas)} tareas entre {fecha_inicio} y {fecha_fin}.")
        return filtradas
    except ValueError as e:
        logging.error(f"Formato de fecha inválido para el filtrado: {e}")
        print("Error: Formato de fecha inválido. Use el formato YYYY-MM-DD.")
        return []

def filtrar_por_etiqueta(tareas, etiqueta):
    filtradas = [tarea for tarea in tareas if tarea.tipo.lower() == etiqueta.lower()]
    logging.info(f"Filtradas {len(filtradas)} tareas con etiqueta '{etiqueta}'.")
    return filtradas

def filtrar_por_estado(tareas, estado):
    filtradas = [tarea for tarea in tareas if tarea.estado == estado]
    logging.info(f"Filtradas {len(filtradas)} tareas con estado {estado}.")
    return filtradas

def mostrar_tareas(tareas):
    if tareas:
        for i, tarea in enumerate(tareas, start=1):
            print(f"\nTarea {i}: \n")
            tarea.VerTarea()
    else:
        print("No hay tareas para mostrar.")

cuentas = Cuenta(
    usuario="Test",
    nombre="Testing_c"
)


def main():
    tareas = cargar_tareas()
    print("Filtrado y busqueda de tareas")
    print("Seleccione accion: ")
    print("1) Filtrar tareas por fecha")
    print("2) Filtrar tareas por etiqueta")
    print("3) Filtrar tareas por estado")
    eleccion = input("Escriba el numero a seleccionar: ")

    if eleccion == "1":
        fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
        tareas_filtradas = filtrar_por_rango_fechas(tareas, fecha_inicio, fecha_fin)
        mostrar_tareas(tareas_filtradas)
    elif eleccion == "2":
        etiqueta = input("Ingrese la etiqueta para filtrar: ")
        tareas_filtradas = filtrar_por_etiqueta(tareas, etiqueta)
        mostrar_tareas(tareas_filtradas)
    elif eleccion == "3":
        print("Seleccione el estado:\n 0) Pendiente\n 1) En progreso\n 2) Completada\n-1) Atrasada")
        estado = input("Ingrese el estado de la tarea: ")
        if estado in ["0", "1", "2", "-1"]:
            tareas_filtradas = filtrar_por_estado(tareas, int(estado))
            mostrar_tareas(tareas_filtradas)
        else:
            print("Estado invalido, intenta nuevamente")
    else:
        print("No existe tal accion!")

if __name__ == "__main__":
    main()