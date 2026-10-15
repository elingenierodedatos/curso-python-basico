"""Lección 5: funciones y módulos.

Antes de empezar aquí, escribe las funciones de los ejercicios 1, 2 y 3
en limpieza.py. Las tres funciones de este archivo las reutilizan.

Completa las funciones en orden. Cada una tiene su guía paso a paso
en el README de esta carpeta.

Para evaluarte:

    pytest lecciones/leccion_05_funciones_y_modulos

Para evaluar un solo ejercicio, por ejemplo el 4:

    pytest lecciones/leccion_05_funciones_y_modulos -k ejercicio_4
"""

# Este import trae el módulo limpieza.py de esta misma carpeta. Sus funciones
# se usan con el nombre del módulo y un punto: limpieza.limpiar_texto(...).
# La marca "noqa" le pide a ruff que no avise del import sin usar mientras
# completas los ejercicios.
from lecciones.leccion_05_funciones_y_modulos import limpieza  # noqa: F401


def limpiar_pedido(pedido_crudo):
    """Devuelve un diccionario nuevo con los datos del pedido ya limpios.

    Todos los valores de pedido_crudo llegan como texto. En el resultado:
    id_pedido y cantidad son enteros, precio_unitario es un número con
    decimales, ciudad y producto van limpios y con mayúscula inicial en cada
    palabra, y estado va limpio y en minúsculas. No modifica pedido_crudo.

    Ejemplo:
        >>> crudo = {"id_pedido": "1001", "ciudad": "  PUEBLA ",
        ...          "producto": "taza de barro", "cantidad": "2",
        ...          "precio_unitario": "$120.00", "estado": " Entregado "}
        >>> limpio = limpiar_pedido(crudo)
        >>> limpio["ciudad"]
        'Puebla'
        >>> limpio["precio_unitario"]
        120.0
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función limpiar_pedido().")


def es_pedido_valido(pedido):
    """Indica si un pedido ya limpio sirve para el análisis.

    Es válido si su ciudad no es un faltante, su cantidad es mayor que 0
    y su precio unitario es mayor que 0.

    Ejemplo:
        >>> es_pedido_valido({"id_pedido": 1001, "ciudad": "Puebla",
        ...                   "producto": "Taza De Barro", "cantidad": 2,
        ...                   "precio_unitario": 120.0, "estado": "entregado"})
        True
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función es_pedido_valido().")


def separar_validos(pedidos):
    """Reparte una lista de pedidos limpios en dos listas: válidos y rechazados.

    Devuelve las dos listas juntas, en una tupla, en ese orden.

    Ejemplo:
        >>> bueno = {"ciudad": "Puebla", "cantidad": 2, "precio_unitario": 120.0}
        >>> malo = {"ciudad": "", "cantidad": 1, "precio_unitario": 60.0}
        >>> separar_validos([bueno, malo]) == ([bueno], [malo])
        True
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función separar_validos().")
