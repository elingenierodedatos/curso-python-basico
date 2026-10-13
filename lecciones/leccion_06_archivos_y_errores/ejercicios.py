"""Lección 6: archivos y manejo de errores.

Completa las siete funciones en orden. Cada una tiene su guía paso a paso
en el README de esta carpeta.

Todas las funciones que reciben una ruta deben aceptar tanto un Path como
un texto. Para lograrlo, conviértela al inicio con Path(ruta).

Para evaluarte:

    pytest lecciones/leccion_06_archivos_y_errores

Para evaluar un solo ejercicio, por ejemplo el 3:

    pytest lecciones/leccion_06_archivos_y_errores -k ejercicio_3
"""

# Los módulos que vas a necesitar ya están importados. El comentario "noqa" le
# pide a ruff que no los marque como "sin usar" mientras completas los ejercicios.
import csv  # noqa: F401
import json  # noqa: F401
from pathlib import Path  # noqa: F401


def contar_lineas(ruta):
    """Cuenta las líneas no vacías de un archivo de texto en UTF-8.

    Una línea que solo tiene espacios cuenta como vacía.

    Ejemplo, con un archivo notas.txt que tiene tres líneas con texto
    y una en blanco:
        >>> contar_lineas(Path("notas.txt"))
        3
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función contar_lineas().")


def a_entero(texto, por_defecto=0):
    """Convierte un texto en entero; si no se puede, devuelve el valor por defecto.

    Ejemplo:
        >>> a_entero("12")
        12
        >>> a_entero("N/D")
        0
        >>> a_entero("dos", por_defecto=-1)
        -1
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función a_entero().")


def leer_csv(ruta):
    """Lee un archivo CSV en UTF-8 y devuelve una lista de diccionarios.

    Cada fila es un diccionario cuyas claves son los encabezados del archivo.
    Todos los valores llegan como texto.

    Si el archivo no existe, lanza FileNotFoundError con el mensaje
    "No se encontró el archivo: <ruta>".

    Ejemplo, con un archivo pedidos.csv de dos filas:
        >>> leer_csv(Path("pedidos.csv"))
        [{'id_pedido': '1001', 'ciudad': 'Mérida'}, {'id_pedido': '1002', ...}]
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función leer_csv().")


def escribir_csv(ruta, filas, columnas):
    """Escribe una lista de diccionarios en un archivo CSV en UTF-8.

    La primera línea es el encabezado, con las columnas en el orden recibido.
    Si la carpeta de destino no existe, la crea. Devuelve el número de filas
    escritas, sin contar el encabezado.

    Ejemplo:
        >>> filas = [{"id_pedido": "1001", "ciudad": "Mérida"}]
        >>> escribir_csv(Path("salida/pedidos.csv"), filas, ["id_pedido", "ciudad"])
        1
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función escribir_csv().")


def guardar_json(ruta, datos):
    """Guarda datos en un archivo JSON en UTF-8.

    Usa sangría de 2 espacios y conserva los acentos tal cual: el archivo
    debe decir México, no M\\u00e9xico. No devuelve nada.

    Ejemplo:
        >>> guardar_json(Path("resumen.json"), {"pais": "México", "pedidos": 9})
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función guardar_json().")


def leer_json(ruta):
    """Lee un archivo JSON en UTF-8 y devuelve los datos que contiene.

    Si el contenido no es JSON válido, lanza ValueError con el mensaje
    "El archivo no contiene JSON válido: <ruta>".

    Ejemplo, con el archivo que guardó el ejemplo anterior:
        >>> leer_json(Path("resumen.json"))
        {'pais': 'México', 'pedidos': 9}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función leer_json().")


def validar_cantidad(texto):
    """Convierte la cantidad de un pedido en entero y rechaza las inválidas.

    Lanza ValueError con uno de estos mensajes:
    - "La cantidad no es un número entero: <texto>" si no se puede convertir.
    - "La cantidad debe ser mayor que cero: <cantidad>" si es cero o negativa.

    Ejemplo:
        >>> validar_cantidad("3")
        3
        >>> validar_cantidad("dos")
        Traceback (most recent call last):
            ...
        ValueError: La cantidad no es un número entero: dos
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función validar_cantidad().")
