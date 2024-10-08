# Proyecto-Gestionador-Tareas: MyTask

Software para la gestión de tareas realizado en Python que permite a los usuarios que se registren en el, crear, actualizar, visualizar, eliminar y archivar tareas. Las tareas activas y archivadas son almacenadas en archivos JSON respectivos para cada una. El sistema cuenta con funcionalidades como registro de actividades mediante logs y autenticación de usuarios, cuyas credenciales son almacenadas en un archivo de texto con contraseñas encriptadas. Además, las tareas pueden ser clasificadas por estado ('Pendiente', 'En progreso', 'Completada', 'Atrasada') y los usuarios pueden archivar las tareas completadas para consultarlas posteriormente.

## Instrucciones e Instalación:

Antes de ejecutar el programa, se debe considerar tener instalado Python y la libreria bycript, esta pudiendo ser instalada desde la terminal ejecutando el siguiente comando:

```
pip install bcrypt
```

Ahora bien, para el correcto funcionamiento del programa tenga en consideración seguir los siguientes pasos:

1. Asegúrate de que todos los archivos del programa (app.py, models.py, autenticador.py, etc.) presentes en la carpeta del repositorio "gestionador_tareas" se encuentren en la misma ubicacion.
2. Abre una terminal en la carpeta donde están los archivos.
3. Ejecuta el siguiente comando:
```
python app.py 
```

## Cómo usar:

El programa se utiliza a través de la línea de comandos, por lo tanto, una vez ejecutado se desplegará texto que sumula un menú por donde se deberá interactuar según las indicaciones descritas por el mismo. En algunas ocaciones se debe escribir números por consola para seleccionar opciones del Menú, en otras ocasiones (cuando el programa lo indique) se debera escribir texto o algun formato indicado por el programa.

## Cómo contribuir:

Para contribuir a este proyecto, puedes seguir los siguientes pasos:

* Crea un fork: Crea un fork del repositorio completo a tu cuenta personal.

* Crea una rama nueva: En tu fork, a partir de la rama ```develop``` crea una nueva rama donde puedas desarrollar la nueva funcionalidad que deseas implementar.

* Desarrolla la funcionalidad: Realiza los cambios necesarios y asegúrate de probar el código para verificar que todo funcione correctamente.

* Crea un pull request a develop: Cuando termines tu trabajo, crea un pull request desde tu fork hacia la rama ```develop``` de este repositorio. (El pull request será revisado por al menos un revisor)

* Integración a main: Si tu pull request es aprobado y los cambios funcionan correctamente, se integrará a la rama principal (```main```).

Asegúrate de incluir una buena descripción de los cambios propuestos y explica explica el propósito de las modificaciones realizadas en el pull request.

## Licencia:

Este proyecto está bajo la Licencia MIT. Esto significa que puedes clonar, modificar y redistribuir el código, siempre y cuando mantengas los créditos al repositorio original y el aviso de derechos de autor.
