"""Lección 7: las funciones que vas a probar.

Este módulo ya está resuelto y funciona bien. No lo edites para resolver los
ejercicios: en esta lección tu trabajo es escribir las pruebas que lo cuidan.

Solo lo vas a modificar una vez, a propósito, cuando la guía te pida provocar
un error. Al terminar ese experimento, deja el archivo como estaba.
"""


def limpiar_precio(texto):
    """Convierte un precio escrito como texto en un número con decimales.

    Quita los espacios, el símbolo de pesos y las comas de miles.

    Ejemplo:
        >>> limpiar_precio(" $1,250.50 ")
        1250.5
    """
    sin_simbolos = texto.strip().replace("$", "").replace(",", "")
    return float(sin_simbolos)


def clasificar_importe(importe):
    """Clasifica un importe en pesos como "bajo", "medio" o "alto".

    - "bajo": menos de 500.
    - "medio": de 500 a menos de 2000.
    - "alto": de 2000 en adelante.

    Ejemplo:
        >>> clasificar_importe(750)
        'medio'
    """
    if importe < 500:
        return "bajo"
    if importe < 2000:
        return "medio"
    return "alto"


def validar_cantidad(texto):
    """Convierte el texto de una cantidad en un entero mayor que cero.

    Lanza ValueError si el texto no es un número entero o si la cantidad
    es cero o negativa.

    Ejemplo:
        >>> validar_cantidad(" 3 ")
        3
    """
    # int() lanza por su cuenta un ValueError si el texto no es un entero.
    cantidad = int(texto)
    if cantidad <= 0:
        raise ValueError(f"La cantidad debe ser mayor que cero: {cantidad}")
    return cantidad


def contar_por_ciudad(pedidos):
    """Cuenta cuántos pedidos hay en cada ciudad.

    Recibe una lista de pedidos (diccionarios con la clave "ciudad") y devuelve
    un diccionario de ciudad a número de pedidos. La ciudad se limpia antes de
    contar: sin espacios en los extremos y en minúsculas, para que
    " Puebla" y "PUEBLA" cuenten como la misma.

    Ejemplo:
        >>> contar_por_ciudad([{"ciudad": "Puebla"}, {"ciudad": " PUEBLA"}])
        {'puebla': 2}
    """
    conteo = {}
    for pedido in pedidos:
        ciudad = pedido["ciudad"].strip().lower()
        conteo[ciudad] = conteo.get(ciudad, 0) + 1
    return conteo
