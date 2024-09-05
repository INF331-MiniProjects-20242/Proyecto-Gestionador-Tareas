import datetime
import logging
from models import Cuenta
from etiquetas import *
from archivador import cargar_tareas, cargar_tareas_archivadas

# Configuracion de logging
logging.basicConfig(filename="app.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def validacion_fecha(fecha):
    if fecha:
        try:
            datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
            return True
        except ValueError:
            print("Formato de fecha invalido, intenta nuevamente con el formato YYYY-MM-DD")
            return False
    return False

def filtrar_por_rango_fechas(tareas, indices_tareas, fecha_inicio, fecha_fin):
    try:
        fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_obj = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        if fecha_inicio_obj > fecha_fin_obj:
            logging.error(f"El rango de fechas es invalido: fecha_inicio ({fecha_inicio}) es mayor que fecha_fin ({fecha_fin})")
            print("Error: La fecha de inicio no puede ser mayor que la fecha de fin.")
            return []

        filtradas = []
        for i in indices_tareas.values():
            tarea = tareas[i]
            if fecha_inicio_obj <= tarea.fecha <= fecha_fin_obj:
                filtradas.append(tarea)
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

def filtrar_por_etiqueta(tareas, indices_tareas, etiqueta):
    filtradas = []
    for i in indices_tareas.values():
        tarea = tareas[i]
        if tarea.tipo == etiqueta:
            filtradas.append(tarea)
    n_filtradas = len(filtradas)
    if n_filtradas == 1:
        logging.info(f"Filtrada {n_filtradas} tarea con etiqueta '{etiqueta}'.")
    else:
        logging.info(f"Filtradas {n_filtradas} tareas con etiqueta '{etiqueta}'.")
    return filtradas

def filtrar_por_estado(tareas, indices_tareas, estado):
    filtradas = []
    for i in indices_tareas.values():
        tarea = tareas[i]
        if tarea.estado == estado:
            filtradas.append(tarea)
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
    while True:
        print("\nFiltrado y busqueda de tareas")
        print("Seleccione accion: ")
        print("1) Mostrar cuenta")
        print("2) Filtrar tareas por fecha")
        print("3) Filtrar tareas por etiqueta")
        print("4) Filtrar tareas por estado")
        print("5) Salir")
        eleccion = input("Escriba el numero a seleccionar: ")
        tareas, indices_tareas = cargar_tareas(cuenta.usuario)
        tareas_archivadas, indices_archivados = cargar_tareas_archivadas(cuenta.usuario)
        if eleccion == "1":
            cuenta.ver_datos()
        elif eleccion == "2":
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            if validacion_fecha(fecha_inicio):
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                if validacion_fecha(fecha_fin):
                    tareas_filtradas = filtrar_por_rango_fechas(tareas, indices_tareas, fecha_inicio, fecha_fin)
                    tareas_filtradas_archivadas = filtrar_por_rango_fechas(tareas_archivadas, indices_archivados, fecha_inicio, fecha_fin)
                    mostrar_tareas(tareas_filtradas + tareas_filtradas_archivadas)
                else:
                    print("Formato de fecha invalido, intenta nuevamente con el formato YYYY-MM-DD")
            else:
                print("Formato de fecha invalido, intenta nuevamente con el formato YYYY-MM-DD")
        elif eleccion == "3":
            etiquetas = cargar_etiquetas()
            etiqueta = obtener_etiqueta(etiquetas)
            tareas_filtradas = filtrar_por_etiqueta(tareas, indices_tareas, etiqueta)
            tareas_filtradas_archivadas = filtrar_por_etiqueta(tareas_archivadas, indices_archivados, etiqueta)
            mostrar_tareas(tareas_filtradas + tareas_filtradas_archivadas)
        elif eleccion == "4":
            print("Seleccione el estado:\n 0) Pendiente\n 1) En progreso\n 2) Completada\n-1) Atrasada")
            estado = input("Ingrese el estado de la tarea: ")
            if estado in ["0", "1", "-1"]:
                tareas_filtradas = filtrar_por_estado(tareas, indices_tareas, int(estado))
                mostrar_tareas(tareas_filtradas)
            elif estado == "2":
                tareas_filtradas_archivadas = filtrar_por_estado(tareas_archivadas, indices_archivados, int(estado))
                mostrar_tareas(tareas_filtradas_archivadas)
            else:
                print("Estado invalido, intenta nuevamente")
        elif eleccion == "5":
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