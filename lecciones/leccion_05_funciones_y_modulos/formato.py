"""Módulo de ejemplo: funciones para mostrar importes y pedidos.

Este archivo ya está resuelto. Sirve para que veas un módulo completo:
un archivo .py con funciones que otros archivos pueden importar.

ejemplos.py lo importa con "import formato". También puedes correrlo solo:

    python lecciones/leccion_05_funciones_y_modulos/formato.py
"""


def formatear_importe(importe, moneda="MXN"):
    """Devuelve el importe como texto, con comas de miles, dos decimales y moneda.

    Ejemplo:
        >>> formatear_importe(1250.5)
        '$1,250.50 MXN'
    """
    return f"${importe:,.2f} {moneda}"


def describir_pedido(pedido):
    """Devuelve una línea de texto que resume un pedido.

    Ejemplo:
        >>> describir_pedido({"producto": "Taza de barro", "cantidad": 2,
        ...                   "precio_unitario": 120.0})
        '2 x Taza de barro: $240.00 MXN'
    """
    cantidad = pedido["cantidad"]
    producto = pedido["producto"]
    total = cantidad * pedido["precio_unitario"]
    return f"{cantidad} x {producto}: {formatear_importe(total)}"


# Este bloque solo corre cuando ejecutas este archivo directamente.
# Cuando otro archivo importa el módulo, Python se lo salta.
if __name__ == "__main__":
    print("Demostración del módulo formato")
    print(formatear_importe(1250.5))
    print(formatear_importe(99.9, moneda="USD"))
