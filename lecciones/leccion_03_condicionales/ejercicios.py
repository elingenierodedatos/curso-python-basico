"""Lección 3: decisiones con if y bucles while.

Completa las siete funciones en orden. Cada una tiene su guía paso a paso
en el README de esta carpeta.

Para evaluarte:

    pytest lecciones/leccion_03_condicionales

Para evaluar un solo ejercicio, por ejemplo el 3:

    pytest lecciones/leccion_03_condicionales -k ejercicio_3
"""


def es_cantidad_valida(cantidad):
    """Indica si la cantidad es un número entero mayor que cero.

    Devuelve True o False. Un texto como "3" o un número con decimales
    como 2.5 no son cantidades válidas. Tampoco lo son True ni False:
    para Python son enteros (True vale 1), así que hay que excluirlos aparte.

    Ejemplo:
        >>> es_cantidad_valida(3)
        True
        >>> es_cantidad_valida("3")
        False
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función es_cantidad_valida().")


def clasificar_importe(importe):
    """Clasifica un importe en pesos como "bajo", "medio" o "alto".

    Es "bajo" si es menor que 500, "medio" de 500 a menos de 2000
    y "alto" de 2000 en adelante.

    Ejemplo:
        >>> clasificar_importe(1250.5)
        'medio'
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función clasificar_importe().")


def es_faltante(valor):
    """Indica si un valor crudo representa un dato faltante.

    Es faltante si vale None o si, ya sin espacios en los extremos y en
    minúsculas, es "", "n/d", "na" o "null". El valor llega como None o como texto.

    Ejemplo:
        >>> es_faltante(" N/D ")
        True
        >>> es_faltante("Puebla")
        False
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función es_faltante().")


def normalizar_estado(estado):
    """Devuelve el estado de un pedido escrito de una sola forma.

    Limpia el texto y devuelve "entregado", "enviado" o "cancelado".
    Acepta los sinónimos "entregada", "en camino" (que cuenta como "enviado")
    y "cancelada". Cualquier otro texto devuelve "desconocido".

    Ejemplo:
        >>> normalizar_estado("  EN CAMINO ")
        'enviado'
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función normalizar_estado().")


def filtrar_mayores(importes, minimo):
    """Devuelve una lista nueva con los importes mayores o iguales al mínimo.

    Conserva el orden original y no modifica la lista recibida.

    Ejemplo:
        >>> filtrar_mayores([450.0, 1200.0, 380.0, 2500.0], 1000)
        [1200.0, 2500.0]
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función filtrar_mayores().")


def contar_faltantes(valores):
    """Cuenta cuántos elementos de la lista son datos faltantes.

    Usa tu función es_faltante() para decidir si cada elemento lo es.

    Ejemplo:
        >>> contar_faltantes(["Puebla", "", "N/D", "Mérida", None])
        3
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función contar_faltantes().")


def posicion_del_primer_faltante(valores):
    """Devuelve el índice del primer dato faltante de la lista, o -1 si no hay.

    Resuélvelo con un bucle while y tu función es_faltante().

    Ejemplo:
        >>> posicion_del_primer_faltante(["Puebla", "Mérida", "NA", ""])
        2
        >>> posicion_del_primer_faltante(["Puebla", "Mérida"])
        -1
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError(
        "Aún no completas la función posicion_del_primer_faltante()."
    )
