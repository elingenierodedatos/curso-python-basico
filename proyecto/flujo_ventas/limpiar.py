"""Etapa 2: limpiar.

Convierte los pedidos crudos (solo texto, con errores) en pedidos confiables.
Lo que no se puede corregir se rechaza y se anota el motivo: nunca se descarta
un dato en silencio.
"""

FALTANTES = ["", "n/d", "na", "null"]

# Formas en que llega escrita cada ciudad, ya sin espacios y en minúsculas.
CIUDADES = {
    "ciudad de méxico": "Ciudad de México",
    "ciudad de mexico": "Ciudad de México",
    "cdmx": "Ciudad de México",
    "guadalajara": "Guadalajara",
    "gdl": "Guadalajara",
    "monterrey": "Monterrey",
    "mty": "Monterrey",
    "puebla": "Puebla",
    "mérida": "Mérida",
    "merida": "Mérida",
    "tijuana": "Tijuana",
}

ESTADOS = {
    "entregado": "entregado",
    "entregada": "entregado",
    "enviado": "enviado",
    "en camino": "enviado",
    "cancelado": "cancelado",
    "cancelada": "cancelado",
}


def es_faltante(valor):
    """Indica si un valor representa un dato faltante.

    Es faltante si es None o si, sin espacios en los extremos y en minúsculas,
    aparece en la lista FALTANTES.

    Ejemplo:
        >>> es_faltante(" N/D ")
        True
        >>> es_faltante("Puebla")
        False
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función es_faltante().")


def limpiar_fecha(texto):
    """Devuelve la fecha en formato AAAA-MM-DD.

    El archivo trae dos formatos: "2025-03-07" (ya correcto) y "07/03/2025"
    (día/mes/año). El día y el mes pueden venir con un solo dígito: "7/3/2025".

    Errores:
        ValueError: con el mensaje "fecha inválida" si el texto es faltante o
            no tiene ninguno de los dos formatos.

    Ejemplo:
        >>> limpiar_fecha(" 7/3/2025 ")
        '2025-03-07'
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función limpiar_fecha().")


def limpiar_ciudad(texto):
    """Devuelve el nombre oficial de la ciudad.

    Si el texto, sin espacios y en minúsculas, es una clave de CIUDADES,
    devuelve su valor. Si no, devuelve el texto limpio con mayúscula inicial
    en cada palabra.

    Errores:
        ValueError: con el mensaje "ciudad faltante" si el valor es faltante.

    Ejemplo:
        >>> limpiar_ciudad("  CDMX ")
        'Ciudad de México'
        >>> limpiar_ciudad("san luis potosí")
        'San Luis Potosí'
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función limpiar_ciudad().")


def limpiar_pedido(crudo):
    """Convierte un pedido crudo en un pedido limpio. No modifica el original.

    Recibe un diccionario con todas las columnas como texto y devuelve uno
    nuevo con estas claves y reglas:

        id_pedido        entero
        fecha            texto AAAA-MM-DD (usa limpiar_fecha)
        cliente          sin espacios en los extremos, mayúscula inicial en
                         cada palabra; "Sin nombre" si es faltante
        ciudad           nombre oficial (usa limpiar_ciudad)
        producto         sin espacios en los extremos, solo la primera letra
                         en mayúscula: "Café de olla"
        cantidad         entero mayor que cero
        precio_unitario  número con decimales mayor que cero; el texto puede
                         traer espacios, el símbolo $ y comas de miles
        estado           valor de ESTADOS; "desconocido" si no está ahí
        total            cantidad por precio_unitario, redondeado a 2 decimales

    Errores:
        ValueError: si el pedido no se puede corregir. El mensaje es el motivo,
            y se revisa en este orden: "id_pedido inválido", "fecha inválida",
            "ciudad faltante", "producto faltante", "cantidad inválida",
            "precio inválido".

    Ejemplo:
        >>> crudo = {"id_pedido": "1001", "fecha": "7/3/2025", "cliente": " ana ruiz",
        ...          "ciudad": "cdmx", "producto": "CAFÉ DE OLLA", "cantidad": "2",
        ...          "precio_unitario": "$185.00", "estado": "Entregada"}
        >>> limpiar_pedido(crudo)["total"]
        370.0
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función limpiar_pedido().")


def limpiar_pedidos(crudos):
    """Limpia una lista de pedidos crudos y separa los que no se pueden usar.

    Devuelve una tupla (limpios, rechazados):

        limpios      lista de pedidos limpios, en el orden en que llegaron
        rechazados   lista de diccionarios con tres claves:
                         "fila"    número de fila de datos, empezando en 1
                         "motivo"  el mensaje del ValueError de limpiar_pedido
                         "datos"   el pedido crudo, sin cambios

    Si un id_pedido ya apareció antes, el pedido repetido se rechaza con el
    motivo "id_pedido duplicado" y se conserva el primero.

    Ejemplo:
        >>> limpios, rechazados = limpiar_pedidos([])
        >>> limpios, rechazados
        ([], [])
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función limpiar_pedidos().")
