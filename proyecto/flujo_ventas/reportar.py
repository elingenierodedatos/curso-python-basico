"""Etapa 4: reportar.

Consulta la base de datos y arma el reporte de ventas.

En todo el reporte, una venta es un pedido cuyo estado no es "cancelado".
"""

import json  # noqa: F401
from pathlib import Path  # noqa: F401


def ventas_por_ciudad(conexion):
    """Devuelve las ventas agrupadas por ciudad, sin contar pedidos cancelados.

    El resultado es una lista de diccionarios con las claves "ciudad",
    "pedidos" (cuántos pedidos) y "total" (suma de total, redondeada a
    2 decimales), ordenada de mayor a menor total.

    Ejemplo de un elemento:
        {"ciudad": "Puebla", "pedidos": 3, "total": 1480.5}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función ventas_por_ciudad().")


def ventas_por_producto(conexion):
    """Devuelve las ventas agrupadas por producto, sin contar pedidos cancelados.

    El resultado es una lista de diccionarios con las claves "producto",
    "unidades" (suma de cantidad) y "total" (suma de total, redondeada a
    2 decimales), ordenada de mayor a menor total.

    Ejemplo de un elemento:
        {"producto": "Prensa francesa", "unidades": 7, "total": 4515.0}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función ventas_por_producto().")


def contar_motivos(rechazados):
    """Cuenta cuántos pedidos se rechazaron por cada motivo.

    Recibe la lista de rechazados que produce limpiar_pedidos y devuelve un
    diccionario motivo -> número de pedidos.

    Ejemplo:
        >>> contar_motivos([{"fila": 3, "motivo": "ciudad faltante", "datos": {}}])
        {'ciudad faltante': 1}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función contar_motivos().")


def construir_reporte(conexion, rechazados):
    """Arma el reporte completo como un diccionario con estas claves:

    "pedidos_cargados"     número de filas en la tabla pedidos
    "pedidos_rechazados"   número de elementos en rechazados
    "pedidos_cancelados"   número de pedidos con estado "cancelado"
    "ventas_totales"       suma de total de los pedidos no cancelados,
                           redondeada a 2 decimales (0 si no hay ninguno)
    "ventas_por_ciudad"    resultado de ventas_por_ciudad
    "ventas_por_producto"  resultado de ventas_por_producto
    "motivos_de_rechazo"   resultado de contar_motivos
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función construir_reporte().")


def guardar_reporte(ruta, reporte):
    """Guarda el reporte como JSON legible y devuelve la ruta como Path.

    Crea la carpeta si no existe. El archivo va en UTF-8, con sangría de
    2 espacios y con los acentos tal cual (no como \\u00e9).
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función guardar_reporte().")
