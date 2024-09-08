from models import Cuenta
import json
import bcrypt
import logging

# Configuracion de logging
logging.basicConfig(filename="app.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def hash_contrasena(contrasena: str):
    return bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_contrasena(contrasena: str, hash_contra: str):
    return bcrypt.checkpw(contrasena.encode('utf-8'), hash_contra.encode('utf-8'))

def existe_usuario(usuario: str):
    try:
        archivo = "users.txt"
        with open(archivo, 'r') as f:
            for linea in f:
                registro = json.loads(linea.strip())
                if registro["usuario"] == usuario:
                    f.close()
                    return True #El usuario existe, por lo que retorna True
        f.close()
    except Exception as e:
        logging.error(f"Error al verificar existencia de usuario: {e}")
    return False

def crear_cuenta(usuario: str, nombre: str, contrasena: str):
    try:
        hash_contra = hash_contrasena(contrasena)
        cuenta = Cuenta(usuario, nombre, hash_contra)
        
        archivo = "users.txt"
        with open(archivo, 'a') as f:
            f.write(json.dumps({"usuario": cuenta.usuario, "nombre": cuenta.nombre, "contrasena": cuenta.contrasena}) + "\n")
        f.close()
        logging.info(f"Cuenta de usuario {usuario} creada correctamente")
    except Exception as e:
        logging.error(f"Error al crear cuenta: {e}")

def verificar_cuenta(usuario: str, contrasena: str):
    try:
        archivo = "users.txt"
        with open(archivo, 'r') as f:
            for linea in f:
                registro = json.loads(linea.strip())
                if registro["usuario"] == usuario:
                    if verificar_contrasena(contrasena, registro["contrasena"]):
                        f.close()
                        logging.info(f"Cuenta de usuario {usuario} ingresada correctamente")
                        return registro["usuario"], registro["nombre"] #El usuario coloco contrasena y usuario correctamente, se entrega el usuario y el nombre
        logging.warning(f"Inicio de sesion fallido para el usuario {usuario}")
        f.close()
    except Exception as e:
        logging.error(f"Error al verificar cuenta: {e}")
    return False

def desplegar_registro():
    try:
        print("\n--- Creacion de Cuenta ---")

        while True:
            print("Escriba su nombre (Al menos 2 caracteres): ")
            nombre = input()
            if len(nombre) < 2:
                print("Su nombre debe contener al menos 2 caracteres!, intente nuevamente")
            else:
                break

        no_unico = True
        minimo = True #Flag para que tenga caracteres el usuario
        while no_unico and minimo:
            print("Escriba un usuario unico (Al menos 2 caracteres): ")
            usuario = input()
            no_unico = existe_usuario(usuario)

            if no_unico:
                #El usuario escribio un nombre ya utilizado por otro
                print("El usuario escrito ya existe en el sistema!")
                print("Intenta con otro porfavor!\n")
            else:
                #Se verifica si el usuario escrito no esta vacio
                if len(usuario) < 2:
                    print("Su usuario debe contener al menos 2 caracteres!, intente nuevamente")
                    no_unico = True
                    minimo = True
                else:
                    # El minimo de caracteres y usuario unico se cumple, entonces se sale del while
                    minimo = False

        while True:
            print("Escriba una contraseña (Al menos 2 caracteres): ")
            contrasena = input()
            if len(contrasena) < 2:
                print("Su contraseña debe contener al menos 2 caracteres!, intente nuevamente")
            else:
                break

        crear_cuenta(usuario, nombre, contrasena)
        print("La cuenta ha sido creada con exito!")
    except Exception as e:
        print(f"Error durante el registro: {e}")
        logging.error(f"Error durante el despliegue registro: {e}")


def desplegar_login():
    try:
        print("\n--- Login ---")
        usuario = input("Escriba su nombre de usuario: ")
        contrasena = input("Escriba su contraseña: ")

        logea = verificar_cuenta(usuario, contrasena)

        if logea:
            print("\nLogin existoso!\n")
            return logea
        else:
            print("Usuario o contraseña equivocados, regresando al menu...")
    except Exception as e:
        print(f"Error durante el login: {e}")
        logging.error(f"Error durante el despliegue del login: {e}")
    return False

def main():
    #Aqui creo el archivo si no existe
    archivo = "users.txt"
    f = open(archivo, 'a')
    f.close()
    logging.info("Se ha entrado al autenticador de cuentas.")
    while True:
        try:
            print("\nBienvenido al autenticador de cuentas")
            print("Seleccione accion: ")
            print("1) Ingresar con tu Cuenta")
            print("2) Registrar Cuenta")
            print("3) Salir")
            eleccion = input("Escriba el numero a seleccionar: ")
            if eleccion == "1":
                login = desplegar_login()
                if login:
                    return Cuenta(
                        usuario=login[0],
                        nombre=login[1],
                        contrasena="***"
                    )
            elif eleccion == "2":
                desplegar_registro()
            elif eleccion == "3":
                logging.info("Se ha salido del autenticador de cuentas.")
                break
            else:
                print("No existe tal accion!")
        except Exception as e:
            print(f"Error durante el Menu de inicio: {e}")
            logging.error(f"Error durante el Menu de inicio: {e}")

if __name__ == "__main__":
    main()