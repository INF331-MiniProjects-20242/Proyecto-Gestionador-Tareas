import datetime
import json
import logging
from models import Tarea, Cuenta
from etiquetas import *

# Configuracion de logging
logging.basicConfig(filename="app.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ARCHIVO_TAREAS = "tareas.json"

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
        logging.warning("Archivo de tareas no encontrado, se creara uno nuevo al guardar tareas.")
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
        n_filtradas = len(filtradas)
        if n_filtradas == 1:
            logging.info(f"Filtrada {len(filtradas)} tarea entre {fecha_inicio} y {fecha_fin}.")
        else:
            logging.info(f"Filtradas {len(filtradas)} tareas entre {fecha_inicio} y {fecha_fin}.")
        return filtradas
    except ValueError as e:
        logging.error(f"Formato de fecha invalido para el filtrado: {e}")
        print("Error: Formato de fecha invalido. Use el formato YYYY-MM-DD.")
        return []

def filtrar_por_etiqueta(tareas, etiqueta):
    filtradas = [tarea for tarea in tareas if tarea.tipo.lower() == etiqueta.lower()]
    n_filtradas = len(filtradas)
    if n_filtradas == 1:
        logging.info(f"Filtrada {n_filtradas} tarea con etiqueta '{etiqueta}'.")
    else:
        logging.info(f"Filtradas {n_filtradas} tareas con etiqueta '{etiqueta}'.")
    return filtradas

def filtrar_por_estado(tareas, estado):
    filtradas = [tarea for tarea in tareas if tarea.estado == estado]
    n_filtradas = len(filtradas)
    if n_filtradas == 1:
        logging.info(f"Filtrada {len(filtradas)} tarea con estado {estado}.")
    else:
        logging.info(f"Filtradas {len(filtradas)} tareas con estado {estado}.")
    return filtradas

def mostrar_tareas(tareas):
    if tareas:
        for i, tarea in enumerate(tareas, start=1):
            print(f"\nTarea {i}: \n")
            tarea.VerTarea()
    else:
        print("No hay tareas para mostrar.")

def main(cuenta):
    logging.info(f"El usuario {cuenta.usuario} ha entrado al filtrador de tareas.")
    tareas = cargar_tareas()
    while True:
        print("\nFiltrado y busqueda de tareas")
        print("Seleccione accion: ")
        print("1) Filtrar tareas por fecha")
        print("2) Filtrar tareas por etiqueta")
        print("3) Filtrar tareas por estado")
        print("4) Salir")
        eleccion = input("Escriba el numero a seleccionar: ")

        if eleccion == "1":
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
            tareas_filtradas = filtrar_por_rango_fechas(tareas, fecha_inicio, fecha_fin)
            mostrar_tareas(tareas_filtradas)
        elif eleccion == "2":
            etiquetas = cargar_etiquetas()
            etiqueta = obtener_etiqueta(etiquetas)
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
        elif eleccion == "4":
            logging.info(f"El usuario {cuenta.usuario} ha salido del filtrador de tareas")
            break
        else:
            print("No existe tal accion!")

if __name__ == "__main__":
    cuenta = Cuenta(
    usuario="Test",
    nombre="Testing_c"
    )
    main(cuenta)