"""Lección 8: guardar y consultar datos con SQLite.

Completa las siete funciones en orden. Cada una tiene su guía paso a paso
en el README de esta carpeta.

Todas trabajan con la tabla pedidos, que tiene estas columnas, en este orden:

    id_pedido, fecha, cliente, ciudad, producto, cantidad, precio_unitario, estado

Para evaluarte:

    pytest lecciones/leccion_08_sqlite

Para evaluar un solo ejercicio, por ejemplo el 3:

    pytest lecciones/leccion_08_sqlite -k ejercicio_3
"""

import sqlite3  # noqa: F401  (lo vas a usar en el ejercicio 1)
from pathlib import Path  # noqa: F401  (lo vas a usar en el ejercicio 1)


def abrir_base(ruta):
    """Abre la base de datos guardada en ruta y devuelve la conexión.

    Si la carpeta donde va el archivo no existe, la crea antes de abrir.
    Quien llama a la función es responsable de cerrar la conexión.

    Ejemplo:
        >>> conexion = abrir_base(Path("salida") / "tienda.db")
        >>> conexion.execute("SELECT 1 + 1").fetchone()
        (2,)
        >>> conexion.close()
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función abrir_base().")


def crear_tabla(conexion):
    """Crea la tabla pedidos si todavía no existe. No devuelve nada.

    Llamarla dos veces no debe fallar ni borrar lo que ya esté guardado.

    Ejemplo:
        >>> conexion = sqlite3.connect(":memory:")
        >>> crear_tabla(conexion)
        >>> crear_tabla(conexion)
        >>> conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone()
        (0,)
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función crear_tabla().")


def insertar_pedido(conexion, pedido):
    """Inserta un pedido (un diccionario) en la tabla y confirma el cambio.

    Los valores viajan como parámetros, con signos de interrogación en el SQL.
    No devuelve nada y no modifica el diccionario recibido.

    Ejemplo:
        >>> pedido = {
        ...     "id_pedido": 1,
        ...     "fecha": "2024-03-01",
        ...     "cliente": "Ana López",
        ...     "ciudad": "Puebla",
        ...     "producto": "Café de olla",
        ...     "cantidad": 3,
        ...     "precio_unitario": 89.9,
        ...     "estado": "entregado",
        ... }
        >>> insertar_pedido(conexion, pedido)
        >>> conexion.execute("SELECT cliente, cantidad FROM pedidos").fetchall()
        [('Ana López', 3)]
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función insertar_pedido().")


def insertar_varios(conexion, pedidos):
    """Inserta una lista de pedidos con executemany y confirma el cambio.

    Devuelve cuántos pedidos insertó.

    Ejemplo:
        >>> insertar_varios(conexion, [pedido_1, pedido_2, pedido_3])
        3
        >>> insertar_varios(conexion, [])
        0
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función insertar_varios().")


def contar_pedidos(conexion):
    """Devuelve cuántas filas tiene la tabla pedidos, como número entero.

    Ejemplo:
        >>> contar_pedidos(conexion)
        3
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función contar_pedidos().")


def buscar_por_ciudad(conexion, ciudad):
    """Devuelve los pedidos de una ciudad como lista de diccionarios.

    Cada diccionario lleva las ocho columnas de la tabla. La lista viene
    ordenada por id_pedido. Si no hay pedidos de esa ciudad, devuelve [].

    Ejemplo:
        >>> pedidos = buscar_por_ciudad(conexion, "Puebla")
        >>> pedidos[0]["cliente"]
        'Ana López'
        >>> buscar_por_ciudad(conexion, "Atlantis")
        []
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función buscar_por_ciudad().")


def ventas_por_ciudad(conexion):
    """Devuelve el total vendido en cada ciudad, sin contar los cancelados.

    El resultado es una lista de tuplas (ciudad, total). El total es la suma
    de cantidad por precio_unitario, redondeada a dos decimales. La lista va
    ordenada del total más alto al más bajo.

    Ejemplo:
        >>> ventas_por_ciudad(conexion)
        [('Ciudad de México', 1715.5), ('Guadalajara', 499.0)]
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función ventas_por_ciudad().")
