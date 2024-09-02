import datetime

def generar_log(mensaje, nivel="Info"):
    with open("app.log", 'a') as log_file:
        tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{tiempo} {nivel}: {mensaje}\n")