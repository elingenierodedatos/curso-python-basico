"""Lección 2: listas y bucles.

Completa las seis funciones en orden. Cada una tiene su guía paso a paso
en el README de esta carpeta.

Para evaluarte:

    pytest lecciones/leccion_02_listas_y_bucles

Para evaluar un solo ejercicio, por ejemplo el 3:

    pytest lecciones/leccion_02_listas_y_bucles -k ejercicio_3
"""


def primero_y_ultimo(valores):
    """Devuelve una tupla con el primer y el último elemento de la lista.

    Se garantiza que la lista tiene al menos un elemento.

    Ejemplo:
        >>> primero_y_ultimo([1001, 1002, 1003])
        (1001, 1003)
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función primero_y_ultimo().")


def sumar_importes(importes):
    """Suma los importes con un bucle acumulador y redondea a dos decimales.

    Si la lista está vacía, devuelve 0.

    Ejemplo:
        >>> sumar_importes([100, 250.5, 49.5])
        400.0
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función sumar_importes().")


def limpiar_ciudades(ciudades):
    """Devuelve una lista nueva con cada ciudad limpia.

    Cada texto queda sin espacios en los extremos y con mayúscula inicial
    en cada palabra. La lista original no se modifica.

    Ejemplo:
        >>> limpiar_ciudades(["  puebla ", "MÉRIDA"])
        ['Puebla', 'Mérida']
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función limpiar_ciudades().")


def calcular_totales(cantidades, precios):
    """Devuelve una lista con cantidad por precio de cada posición.

    Cada total se redondea a dos decimales. Se garantiza que las dos listas
    tienen la misma longitud. Ninguna de las dos se modifica.

    Ejemplo:
        >>> calcular_totales([2, 1], [45.5, 1250.0])
        [91.0, 1250.0]
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función calcular_totales().")


def los_mas_altos(importes, n):
    """Devuelve los n importes más altos, de mayor a menor.

    La lista original no se modifica. Si n es mayor que la cantidad de
    importes, devuelve todos.

    Ejemplo:
        >>> los_mas_altos([450.0, 1250.5, 89.9, 780.0], 2)
        [1250.5, 780.0]
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función los_mas_altos().")


def importe_promedio(importes):
    """Devuelve el promedio de los importes, redondeado a dos decimales.

    Se garantiza que la lista tiene al menos un importe, así que no
    necesitas revisar si está vacía.

    Ejemplo:
        >>> importe_promedio([100, 200, 300])
        200.0
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función importe_promedio().")
