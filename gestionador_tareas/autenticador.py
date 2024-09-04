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
                        return True #El usuario coloco contrasena y usuario correctamente
        logging.warning(f"Inicio de sesion fallido para el usuario {usuario}")
        f.close()
    except Exception as e:
        logging.error(f"Error al verificar cuenta: {e}")
    return False
