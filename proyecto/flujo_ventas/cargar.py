"""Etapa 3: cargar.

Guarda los pedidos limpios en una base de datos SQLite.
"""

import sqlite3  # noqa: F401
from pathlib import Path  # noqa: F401


def abrir_base(ruta):
    """Abre la base de datos y devuelve la conexión.

    Crea la carpeta del archivo si no existe. Si ruta es ":memory:", abre una
    base temporal en memoria y no crea ninguna carpeta.
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función abrir_base().")


def crear_tabla(conexion):
    """Crea la tabla pedidos si no existe. Llamarla dos veces no debe fallar.

    Columnas, en este orden:

        id_pedido        INTEGER, clave primaria
        fecha            TEXT
        cliente          TEXT
        ciudad           TEXT
        producto         TEXT
        cantidad         INTEGER
        precio_unitario  REAL
        estado           TEXT
        total            REAL
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función crear_tabla().")


def cargar_pedidos(conexion, pedidos):
    """Guarda los pedidos limpios en la tabla y devuelve cuántos recibió.

    La carga se puede repetir: si se corre dos veces con los mismos pedidos,
    la tabla termina con las mismas filas, sin duplicados y sin errores.
    Si un id_pedido ya existe, sus datos se reemplazan por los nuevos.

    Usa parámetros (?) para los valores. Nunca armes el SQL pegando textos.
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función cargar_pedidos().")
