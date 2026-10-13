"""Etapa 1: extraer.

Lee el archivo CSV de pedidos tal como llega, sin corregir nada.
"""

import csv  # noqa: F401
from pathlib import Path  # noqa: F401

COLUMNAS = [
    "id_pedido",
    "fecha",
    "cliente",
    "ciudad",
    "producto",
    "cantidad",
    "precio_unitario",
    "estado",
]


def leer_pedidos(ruta):
    """Lee el CSV de pedidos y devuelve una lista de diccionarios, uno por fila.

    Todos los valores se devuelven como texto, tal como vienen en el archivo.

    Errores:
        FileNotFoundError: si el archivo no existe, con el mensaje
            "No se encontró el archivo: <ruta>".
        ValueError: si al encabezado le falta alguna de las COLUMNAS, con el
            mensaje "Faltan columnas en el archivo: <nombres separados por coma>",
            en el mismo orden en que aparecen en COLUMNAS.

    Ejemplo:
        >>> pedidos = leer_pedidos(Path("proyecto/datos/pedidos_crudos.csv"))
        >>> pedidos[0]["id_pedido"]
        '1001'
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función leer_pedidos().")
