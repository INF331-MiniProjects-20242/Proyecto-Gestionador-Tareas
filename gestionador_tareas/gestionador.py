import datetime
import logging
import json
from models import Tarea, Cuenta
from etiquetas import *

# Configuracion de logging
logging.basicConfig(filename="app.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ARCHIVO_TAREAS = "tareas.json"

def cargar_tareas():
    try:
        with open(ARCHIVO_TAREAS, 'r') as file:
            tareas_data = json.load(file)
            return [Tarea.from_dict(t) for t in tareas_data]
    except FileNotFoundError as e:
        logging.warning(f"Archivo de tareas no encontrado, se creara uno nuevo al crear una nueva tarea: {e}")
        print(f"Archivo de tareas no encontrado, se creara uno nuevo al crear una nueva tarea: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error al leer el archivo de tareas, no existen datos en archivo JSON: {e}")
        return []

def guardar_tareas(tareas):
    try:
        with open(ARCHIVO_TAREAS, 'w') as file:
            json.dump([t.to_dict() for t in tareas], file, indent=4)
            logging.info("Tareas guardadas correctamente.")
    except Exception as e:
        logging.error(f"Error al guardar las tareas: {e}")
        print(f"Error al guardar las tareas: {e}")

def crear_tarea(usuario):
    try:
        # Verificacion de titulo para que no exceda los 50 caracteres
        while True:
            titulo = input("Ingrese el titulo de la tarea: ")
            if len(titulo) > 50:
                print("El titulo debe contener a lo mas 50 caracteres, intenta nuevamente")
            else:
                break
        # Verificacion de descripcion para que no exceda los 200 caracteres
        while True:
            descr = input("Ingrese la descripcion de la tarea: ")
            if len(descr) > 200:
                print("La descripcion debe contener a los mas 200 caracteres, intenta nuevamente")
            else:
                break

        # Fecha por defecto 1 mes despues de la fecha de creacion o se puede ingresar manualmente
        fecha_default = (datetime.date.today() + datetime.timedelta(days=30))
        while True:
            fecha_str = input(f"Ingrese la fecha de vencimiento (YYYY-MM-DD) o presione Enter para la fecha por defecto ({fecha_default}): ")
            # Verificacion de fecha ingresada, si el formato entregado corresponde a una fecha posterior a la actual o si cumple el formato YYYY-MM-DD
            if fecha_str:
                try:
                    fecha_val = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
                    if fecha_val < datetime.date.today():
                        print("Fecha ingresada no puede ser anterior a la actual, intenta nuevamente")
                    else:
                        break
                except ValueError:
                    print("Formato de fecha invalido, intenta nuevamente con el formato YYYY-MM-DD")
            else:
                break
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else fecha_default

        etiquetas = cargar_etiquetas()
        tipo = obtener_etiqueta(etiquetas)

        tarea = Tarea(titulo, descr, fecha, tipo, usuario=usuario)
        logging.info(f"Tarea '{tarea.titulo}' creada por el usuario {usuario}")

        tareas = cargar_tareas()
        tareas.append(tarea)

        # Guardado automatico despues de crear tarea
        guardar_tareas(tareas)
        print("Tarea creada y guardada con exito.")
    except Exception as e:
        logging.error(f"Error al crear la tarea: {e}")
        print(f"Error: No se pudo crear la tarea. Verifique los datos ingresados: {e}")
        return None
    
def mostrar_tareas(tareas):
    if not tareas:
        print("No hay tareas disponibles.")
        return
    for i, tarea in enumerate(tareas, start=1):
        print(f"\nTarea {i}:\n")
        tarea.VerTarea()

def actualizar_tarea(usuario):
    tareas = cargar_tareas()
    mostrar_tareas(tareas)
    try:
        seleccion = int(input("Ingrese el numero de la tarea a actualizar: "))
        if 1 <= seleccion <= len(tareas):
            tarea = tareas[seleccion - 1]
            print(f"Actualizando tarea '{tarea.titulo}'")
            # Verificacion de titulo para que no exceda los 50 caracteres
            while True:
                titulo = input(f"Nuevo titulo (dejar en blanco para mantener '{tarea.titulo}'): ") or tarea.titulo
                if len(titulo) > 50:
                    print("El titulo debe contener a lo mas 50 caracteres, intenta nuevamente")
                else:
                    break
                # Verificacion de descripcion para que no exceda los 200 caracteres
            while True:
                descr = input(f"Nueva descripcion (dejar en blanco para mantener '{tarea.descr}'): ") or tarea.descr
                if len(descr) > 200:
                    print("La descripcion debe contener a los mas 200 caracteres, intenta nuevamente")
                else:
                    break
            
            # Actualizar la fecha de vencimiento si se proporciona una nueva
            while True:
                fecha_str = input(f"Nueva fecha de vencimiento (YYYY-MM-DD HH:MM) o presione Enter para mantener '{tarea.fecha}'): ")
                # Verificacion de fecha ingresada, si el formato entregado corresponde a una fecha posterior a la actual o si cumple el formato YYYY-MM-DD
                if fecha_str:
                    try:
                        fecha_val = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
                        if fecha_val < datetime.date.today():
                            print("Fecha ingresada no puede ser anterior a la actual, intenta nuevamente")
                        else:
                            break
                    except ValueError:
                        print("Formato de fecha invalido, intenta nuevamente con el formato YYYY-MM-DD")
                else:
                    break
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else tarea.fecha
            
            # Flag que indica si se cambia la etiqueta o no
            tipo_f = input(f"¿Desea mantener la etiqueta (dejar en blanco) o cambiar la etiqueta (ingrese 1)?: ")
            if tipo_f == "1":
                etiquetas = cargar_etiquetas()
                tipo = obtener_etiqueta(etiquetas)
            else:
                tipo = tarea.tipo
            
            # Actualizacion atributos de tarea
            tarea.titulo = titulo
            tarea.descr = descr
            tarea.fecha = fecha
            tarea.tipo = tipo

            # Guardar tarea actualizada 
            guardar_tareas(tareas)
            logging.info(f"Tarea '{tarea.titulo}' actualizada por el usuario {usuario}")
            print("Tarea actualizada con exito.")
        else:
            print("Numero de tarea invalido.")
    except ValueError:
        print("Entrada invalida.")
        logging.error("Error al actualizar la tarea: Entrada invalida.")

def eliminar_tarea(usuario):
    tareas = cargar_tareas()
    mostrar_tareas(tareas)
    try:
        seleccion = int(input("Ingrese el numero de la tarea a eliminar: "))
        if 1 <= seleccion <= len(tareas):
            tarea = tareas.pop(seleccion - 1)
            logging.info(f"Tarea '{tarea.titulo}' eliminada por el usuario {usuario}")

            guardar_tareas(tareas)  # Guardar la lista de tareas actualizada
            print("Tarea eliminada con exito.")
        else:
            print("Numero de tarea invalido.")
    except ValueError:
        print("Entrada invalida.")
        logging.error("Error al eliminar la tarea: Entrada invalida.")

def main(cuenta):
    logging.info(f"El usuario {cuenta.usuario} ha entrado al gestionador de tareas.")
    while True:
        print("\nBienvenido al gestionador de tareas")
        print("Seleccione accion:")
        print("1) Mostrar cuenta")
        print("2) Crear tarea")
        print("3) Mostrar tareas")
        print("4) Actualizar tarea")
        print("5) Eliminar tarea")
        print("6) Salir")
        eleccion = input("Escriba el numero a seleccionar: ")
        if eleccion == "1":
            cuenta.ver_datos()
        elif eleccion == "2":
            crear_tarea(cuenta.usuario)
        elif eleccion == "3":
            tareas = cargar_tareas()
            mostrar_tareas(tareas)
        elif eleccion == "4":
            actualizar_tarea(cuenta.usuario)
        elif eleccion == "5":
            eliminar_tarea(cuenta.usuario)
        elif eleccion == "6":
            logging.info(f"El usuario {cuenta.usuario} ha salido del gestionador de tareas.")
            break
        else:
            print("No existe tal accion!")

if __name__ == "__main__":
    cuenta = Cuenta(
        usuario="Test",
        nombre="Testing_c"
    )
    main(cuenta)