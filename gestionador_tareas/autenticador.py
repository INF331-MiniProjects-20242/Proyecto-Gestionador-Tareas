from models import Cuenta
from logs import generar_log
import json
import bcrypt

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
        generar_log(f"Error al crear cuenta: {e}", "Error")
    return False

def crear_cuenta(usuario: str, nombre: str, contrasena: str):
    try:
        hash_contra = hash_contrasena(contrasena)
        cuenta = Cuenta(usuario, nombre, hash_contra)
        
        archivo = "users.txt"
        with open(archivo, 'a') as f:
            f.write(json.dumps({"usuario": cuenta.usuario, "nombre": cuenta.nombre, "contrasena": cuenta.contrasena}) + "\n")
        f.close()
    except Exception as e:
        generar_log(f"Error al crear cuenta: {e}", "Error")

def verificar_cuenta(usuario: str, contrasena: str):
    try:
        archivo = "users.txt"
        with open(archivo, 'r') as f:
            for linea in f:
                registro = json.loads(linea.strip())
                if registro["usuario"] == usuario:
                    if verificar_contrasena(contrasena, registro["contrasena"]):
                        f.close()
                        return True #El usuario coloco contrasena y usuario correctamente
        f.close()
    except Exception as e:
        generar_log(f"Error al verificar cuenta: {e}", "Error")
    return False
