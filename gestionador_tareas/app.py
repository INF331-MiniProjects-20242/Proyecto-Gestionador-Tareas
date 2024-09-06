import autenticador
import filtrador
import gestionador
import json
from models import Tarea
import logging
import datetime

# Configuracion de logging
logging.basicConfig(filename="app.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Funcion que carga todas las tareas independiente del usuario.
def todas_tareas():
    try:
        with open("tareas.json", "r") as file:
            tareas_data = json.load(file)
            return [Tarea.from_dict(t) for t in tareas_data]
    except FileNotFoundError as e:
        logging.warning(f"Archivo de tareas no encontrado, se creara uno nuevo: {e}")
        gestionador.guardar_tareas([])
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error al leer el archivo de tareas, no existen datos en archivo JSON: {e}")
        return []

# Funcion que cambia los estados de las tareas pasadas de la fecha actual a atrasadas automaticamente.
def verificar_atrasos_tareas():
    tareas = todas_tareas()
    try:
        for tarea in tareas:
            if tarea.estado == -1:
                continue
            if datetime.date.today() > tarea.fecha:
                logging.info(f"La tarea '{tarea.titulo}' se ha cambiado a estado atrasada")
                tarea.estado = -1
        gestionador.guardar_tareas(tareas)
    except Exception as e:
        logging.error(f"Error al verificar tareas: {e}")
        print(f"Error: No se pudo verificar tareas: {e}")
        return None

def main():
    verificar_atrasos_tareas()
    while True:
        cuenta = autenticador.main()
        if cuenta:
            while True:
                print("\nSelecciona accion a realizar:")
                print("1) Gestionar tareas")
                print("2) Filtrar/Buscar tareas")
                print("3) Salir")
                eleccion = input("Escriba el numero a seleccionar: ")
                if eleccion == "1":
                    gestionador.main(cuenta)
                elif eleccion == "2":
                    filtrador.main(cuenta)
                elif eleccion == "3":
                    break
                else:
                    print("No existe tal accion!")
        else:
            break

if __name__ == "__main__":
    main()