import autenticador
import filtrador
import gestionador

def main():
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