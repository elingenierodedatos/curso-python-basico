"""Lección 4: diccionarios y conjuntos.

Completa las siete funciones en orden. Cada una tiene su guía paso a paso
en el README de esta carpeta.

Para evaluarte:

    pytest lecciones/leccion_04_diccionarios

Para evaluar un solo ejercicio, por ejemplo el 3:

    pytest lecciones/leccion_04_diccionarios -k ejercicio_3
"""


def crear_pedido(id_pedido, producto, cantidad, precio_unitario):
    """Devuelve un diccionario con los cuatro datos del pedido.

    Las claves se llaman igual que los parámetros.

    Ejemplo:
        >>> pedido = crear_pedido(1001, "Café de olla", 2, 185.0)
        >>> pedido["producto"]
        'Café de olla'
        >>> pedido["precio_unitario"]
        185.0
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función crear_pedido().")


def obtener_ciudad(pedido):
    """Devuelve la ciudad del pedido, o "sin ciudad" si no tiene esa clave.

    Ejemplo:
        >>> obtener_ciudad({"id_pedido": 1001, "ciudad": "Puebla"})
        'Puebla'
        >>> obtener_ciudad({"id_pedido": 1002})
        'sin ciudad'
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función obtener_ciudad().")


def agregar_total(pedido):
    """Devuelve una copia del pedido con la clave nueva "total".

    El total es cantidad por precio unitario, redondeado a dos decimales.
    El pedido original no debe cambiar.

    Ejemplo:
        >>> agregar_total({"cantidad": 2, "precio_unitario": 185.0})
        {'cantidad': 2, 'precio_unitario': 185.0, 'total': 370.0}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función agregar_total().")


def contar_por_ciudad(pedidos):
    """Cuenta cuántos pedidos hay en cada ciudad.

    Recibe una lista de pedidos y devuelve un diccionario: ciudad -> número de pedidos.

    Ejemplo:
        >>> contar_por_ciudad([{"ciudad": "Puebla"}, {"ciudad": "Puebla"}])
        {'Puebla': 2}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función contar_por_ciudad().")


def ventas_por_producto(pedidos):
    """Suma el importe vendido de cada producto.

    El importe de un pedido es cantidad por precio unitario. Devuelve un
    diccionario: producto -> suma de importes, redondeada a dos decimales.

    Ejemplo:
        >>> pedidos = [
        ...     {"producto": "Taza de barro", "cantidad": 2, "precio_unitario": 95.5},
        ...     {"producto": "Taza de barro", "cantidad": 1, "precio_unitario": 95.5},
        ... ]
        >>> ventas_por_producto(pedidos)
        {'Taza de barro': 286.5}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función ventas_por_producto().")


def ciudades_unicas(pedidos):
    """Devuelve la lista de ciudades distintas, ordenada con sorted().

    Ejemplo:
        >>> pedidos = [
        ...     {"id_pedido": 1001, "ciudad": "Tijuana"},
        ...     {"id_pedido": 1002, "ciudad": "Puebla"},
        ...     {"id_pedido": 1003, "ciudad": "Tijuana"},
        ... ]
        >>> ciudades_unicas(pedidos)
        ['Puebla', 'Tijuana']
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función ciudades_unicas().")


def pedido_mas_grande(pedidos):
    """Devuelve el pedido con el mayor importe (cantidad por precio unitario).

    Redondea cada importe a dos decimales antes de comparar. Si la lista está
    vacía devuelve None. Si hay empate, devuelve el primero.

    Ejemplo:
        >>> pedidos = [
        ...     {"id_pedido": 1001, "cantidad": 2, "precio_unitario": 185.0},
        ...     {"id_pedido": 1002, "cantidad": 1, "precio_unitario": 420.0},
        ... ]
        >>> pedido_mas_grande(pedidos)
        {'id_pedido': 1002, 'cantidad': 1, 'precio_unitario': 420.0}
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función pedido_mas_grande().")
