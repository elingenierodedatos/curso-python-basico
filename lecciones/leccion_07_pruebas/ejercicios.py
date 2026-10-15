"""Lección 7: pruebas con pytest.

En esta lección no completas funciones del negocio: escribes las
comprobaciones que las cuidan. El ejercicio 0 es un calentamiento: una
función que recibe otra función y la llama. Cada una de las comprobaciones
que siguen recibe como parámetro la función que debe revisar y la pone a
prueba con `assert`.

Nuestras pruebas llaman a cada comprobación tuya varias veces: una con la
función correcta de `funciones.py`, que debe pasar sin error, y otras con
versiones defectuosas, que tu comprobación debe atrapar.

El ejercicio 6 no está aquí: lo resuelves en `test_mis_pruebas.py`.
La guía paso a paso está en el README de esta carpeta.

Para evaluarte:

    pytest lecciones/leccion_07_pruebas/test_ejercicios.py

Para evaluar un solo ejercicio, por ejemplo el 3:

    pytest lecciones/leccion_07_pruebas/test_ejercicios.py -k ejercicio_3
"""

import pytest  # noqa: F401  (lo vas a usar en el ejercicio 3)


def aplicar_a_todos(pedidos, funcion):
    """Devuelve una lista con el resultado de llamar funcion(elemento) con cada uno.

    El parámetro funcion recibe una función, que se llama aquí dentro. La
    lista puede traer pedidos, textos o cualquier otra cosa que esa función
    sepa recibir.

    Ejemplo:
        >>> def obtener_ciudad(pedido):
        ...     return pedido["ciudad"]
        >>> aplicar_a_todos([{"ciudad": "Puebla"}, {"ciudad": "Mérida"}],
        ...                 obtener_ciudad)
        ['Puebla', 'Mérida']
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función aplicar_a_todos().")


def comprobar_limpiar_precio(limpiar_precio):
    """Comprueba con `assert` que la función recibida limpia bien los precios.

    Recibe la función a revisar. Si funciona bien, termina sin error. Si
    devuelve algo equivocado, algún `assert` debe fallar. No devuelve nada.

    Ejemplo:
        >>> from lecciones.leccion_07_pruebas.funciones import limpiar_precio
        >>> comprobar_limpiar_precio(limpiar_precio)
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función comprobar_limpiar_precio().")


def comprobar_limites_de_clasificar_importe(clasificar_importe):
    """Comprueba que la función recibida respeta los límites de 500 y 2000.

    Revisa el valor de cada límite y el valor justo anterior. No devuelve nada.

    Ejemplo:
        >>> from lecciones.leccion_07_pruebas.funciones import clasificar_importe
        >>> comprobar_limites_de_clasificar_importe(clasificar_importe)
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError(
        "Aún no completas la función comprobar_limites_de_clasificar_importe()."
    )


def comprobar_validar_cantidad_rechaza_invalidos(validar_cantidad):
    """Comprueba que la función recibida lanza ValueError con cantidades inválidas.

    Usa `pytest.raises` una vez por cada texto inválido. No devuelve nada.

    Ejemplo:
        >>> from lecciones.leccion_07_pruebas.funciones import validar_cantidad
        >>> comprobar_validar_cantidad_rechaza_invalidos(validar_cantidad)
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError(
        "Aún no completas la función comprobar_validar_cantidad_rechaza_invalidos()."
    )


def comprobar_contar_por_ciudad(contar_por_ciudad):
    """Comprueba que la función recibida cuenta bien los pedidos de cada ciudad.

    Prepara una lista pequeña de pedidos, con ciudades repetidas y escritas de
    formas distintas, y revisa el diccionario completo. Revisa también qué
    pasa con una lista vacía. No devuelve nada.

    Ejemplo:
        >>> from lecciones.leccion_07_pruebas.funciones import contar_por_ciudad
        >>> comprobar_contar_por_ciudad(contar_por_ciudad)
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError(
        "Aún no completas la función comprobar_contar_por_ciudad()."
    )


def casos_de_limpiar_precio():
    """Devuelve los casos para probar limpiar_precio(), listos para parametrizar.

    Es una lista de al menos cuatro tuplas `(texto, esperado)`: el texto que
    recibe limpiar_precio() y el número que debe devolver.

    Ejemplo:
        >>> casos = casos_de_limpiar_precio()
        >>> casos[0]
        ('45.5', 45.5)
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función casos_de_limpiar_precio().")
