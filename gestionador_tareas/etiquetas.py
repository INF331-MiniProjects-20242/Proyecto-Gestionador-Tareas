import logging

# Configuración de logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ARCHIVO_ETIQUETAS = 'etiquetas.txt'

def cargar_etiquetas():
    try:
        with open(ARCHIVO_ETIQUETAS, 'r') as file:
            etiquetas = file.read().strip().split('\n')
            return etiquetas
    except FileNotFoundError:
        logging.error("Archivo de etiquetas no encontrado.")
        return []

def mostrar_etiquetas(etiquetas):
    print("Seleccione una etiqueta:")
    for i, etiqueta in enumerate(etiquetas, start=1):
        print(f"{i}. {etiqueta}")

def obtener_etiqueta(etiquetas):
    mostrar_etiquetas(etiquetas)
    while True:
        try:
            seleccion = int(input("Ingrese el número de la etiqueta: "))
            if 1 <= seleccion <= len(etiquetas):
                return etiquetas[seleccion - 1]
            else:
                print("Número inválido. Intenta nuevamente.")
        except ValueError:
            print("Entrada inválida. Intenta nuevamente.")