import logging
import json
from gestionador import cargar_tareas, verificacion_tareas_indices, mostrar_tareas, guardar_tareas
from models import Tarea

ARCHIVADOR = "archivados.json"

def cargar_tareas_archivadas(usuario):
    try:
        archivados = []
        indices_archivados = {}
        j = 1
        with open(ARCHIVADOR, 'r') as file:
            tareas_archivadas_data = json.load(file)
            for i, t in enumerate(tareas_archivadas_data):
                archivados.append(Tarea.from_dict(t))
                if t["usuario"] == usuario:
                    indices_archivados[j] = i
                    j += 1
            return archivados, indices_archivados
    except FileNotFoundError as e:
        logging.warning(f"Archivo de tareas archivadas no encontrado, se creara uno nuevo al archivar una nueva tarea: {e}")
        print(f"Archivo de tareas archivadas no encontrado, se creara uno nuevo al archivar una nueva tarea: {e}")
        return [], {}
    except json.JSONDecodeError as e:
        logging.error(f"Error al leer el archivo de tareas archivadas, no existen datos en archivo JSON: {e}")
        return [], {}

def guardar_tareas_archivadas(tareas_archivadas):
    try:
        with open(ARCHIVADOR, 'w') as file:
            json.dump([t.to_dict() for t in tareas_archivadas], file, indent=4)
    except Exception as e:
        logging.error(f"Error al guardar las tareas archivadas: {e}")
        print(f"Error al guardar las tareas archivadas: {e}")

def archivar_tarea(tarea, usuario):
    try:
        tareas_archivadas, _ = cargar_tareas_archivadas(usuario)
        tareas_archivadas.append(tarea)
        guardar_tareas_archivadas(tareas_archivadas)
        print("La tarea ha sido archivada correctamente!")
    except Exception as e:
        logging.error(f"Error al archivar tarea: {e}")
        print(f"Error al archivar tarea: {e}")

def actualizar_estado_tarea(usuario):
    tareas, indices_tareas = cargar_tareas(usuario)
    if verificacion_tareas_indices(tareas, indices_tareas):
        mostrar_tareas(tareas, indices_tareas)
        try:
            seleccion = int(input("Ingrese el numero de la tarea para actualizar estado: "))
            if 1 <= seleccion <= len(indices_tareas):
                tarea = tareas[indices_tareas[seleccion]]
                print(f"\nActualizando estado de la tarea '{tarea.titulo}'")
                while True:
                    print("Estados disponibles para actualizar: ")
                    print("1) Pendiente")
                    print("2) En progreso...")
                    print("3) Completada!")
                    nuevo_estado = input(f"Ingrese el numero deseado para la tarea (actualmente el estado es: '{tarea.ver_estado()}'): ")
                    if nuevo_estado == "1":
                        tarea.estado = 0
                        guardar_tareas(tareas)
                        logging.info(f"Estado de la tarea '{tarea.titulo}' actualizado correctamente")
                        print("Estado de tarea actualizado correctamente!")
                        break
                    elif nuevo_estado == "2":
                        tarea.estado = 1
                        guardar_tareas(tareas)
                        logging.info(f"Estado de la tarea '{tarea.titulo}' actualizado correctamente")
                        print("Estado de tarea actualizado correctamente!")
                        break
                    elif nuevo_estado == "3":
                        tarea.estado = 2
                        print("\nCambiaste una tarea a estado Completado, Felicidades!")
                        while True:
                            print("Deseas archivar o eliminar la tarea? ")
                            print("1) Eliminar Tarea")
                            print("2) Archivar tarea")
                            eleccion = input(f"Escriba el numero a seleccionar: ")
                            if eleccion == "1":
                                tarea = tareas.pop(indices_tareas[seleccion])
                                logging.info(f"Estado de la Tarea '{tarea.titulo}' actualizada y eliminada por el usuario {usuario}")
                                guardar_tareas(tareas)
                                print("Estado de la tarea actualizada y eliminada correctamente!")
                                break
                            elif eleccion == "2":
                                archivar_tarea(tarea, usuario)
                                # Eliminar tarea de archivos tareas.json (solo en archivado)
                                tarea = tareas.pop(indices_tareas[seleccion])
                                logging.info(f"Estado de la Tarea '{tarea.titulo}' actualizada y archivada por el usuario {usuario}")
                                guardar_tareas(tareas)
                                break
                            else:
                                print("Accion invalida! intente nuevamente\n")
                        break
                    else:
                        print("Numero invalido! intente nuevamente\n")
            else:
                print("\nNumero de tarea invalido.")
        except Exception as e:
            logging.error(f"Error al actualizar estado de la tarea: {e}")

def eliminar_archivados(usuario):
    archivados, indices_tareas = cargar_tareas_archivadas(usuario)
    if verificacion_tareas_indices(archivados, indices_tareas):
        mostrar_tareas(archivados, indices_tareas)
        try:
            seleccion = int(input("Ingrese el numero de la tarea archivada a eliminar: "))
            if 1 <= seleccion <= len(indices_tareas):
                tarea = archivados.pop(indices_tareas[seleccion])
                logging.info(f"Tarea '{tarea.titulo}' eliminada por el usuario {usuario} de archivados")

                guardar_tareas_archivadas(archivados)  # Guardar la lista de tareas actualizada
                print("Tarea eliminada de archivados con exito.")
            else:
                print("Numero de tarea invalido.")
        except ValueError:
            print("Entrada invalida.")
            logging.error("Error al eliminar la tarea de archivados: Entrada invalida.")