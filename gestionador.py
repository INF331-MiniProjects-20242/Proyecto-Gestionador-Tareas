from models import Tarea, Cuenta
from autenticador import *
from logs import generar_log
import datetime

def desplegar_inicio():
    try:
        print("\nBienvenido al gestionador de tareas")
        print("Seleccione accion: ")
        print("1) Ingresar con tu Cuenta")
        print("2) Registrar Cuenta")
        print("3) Salir")
        print("Escriba el numero a seleccionar: ")
        eleccion = input()

        if eleccion == "1":
            desplegar_login()
        elif eleccion == "2":
            if desplegar_registro():
                print("Mandar al menu de tareas")
        elif eleccion == "3":
            return False
        else:
            print("No existe tal accion!")
        return True
    except Exception as e:
        print(f"Error durante el Menu de inicio: {e}")
        generar_log(f"Error: {e}", "Error")

def desplegar_registro():
    try:
        print("\n--- Creacion de Cuenta ---")

        print("Escriba su nombre: ")
        nombre = input()

        no_unico = True
        while no_unico:
            print("Escriba un usuario unico: ")
            usuario = input()
            no_unico = existe_usuario(usuario)

            if no_unico:
                #El usuario escribio un nombre ya utilizado por otro
                print("El usuario escrito ya existe en el sistema!")
                print("Intenta con otro porfavor!\n")

        print("Escriba una contraseña: ")
        contrasena = input()

        crear_cuenta(usuario, nombre, contrasena)
        print("La cuenta ha sido creada con exito!")
    except Exception as e:
        print(f"Error durante el registro: {e}")
        generar_log(f"Error: {e}", "Error")


def desplegar_login():
    try:
        print("\n--- Login ---")
        print("Escriba su nombre de usuario: ")
        usuario = input()
        print("Escriba su contraseña: ")
        contrasena = input()

        logea = verificar_cuenta(usuario, contrasena)

        if logea:
            print("\nLogin existoso!\n")
            return True
        else:
            print("Usuario o contraseña equivocados, regresando al menu...")
    except Exception as e:
        print(f"Error durante el login: {e}")
        generar_log(f"Error: {e}", "Error")
    return False

#Aqui creo el archivo si no existe
archivo = "users.txt"
f = open(archivo, 'a')
f.close()

cuentas = Cuenta(
    usuario="Test",
    nombre="Testing_c",
    contrasena="123"
)

tarea1 = Tarea(
    titulo="Completar proyecto",
    descr="Finalizar el proyecto de Python",
    fecha= datetime.datetime(2024, 8, 29, 12, 0),
    tipo="Trabajo",
    estado=0
)

flag = True
while flag:
    flag = desplegar_inicio()

print(existe_usuario("Test"))
