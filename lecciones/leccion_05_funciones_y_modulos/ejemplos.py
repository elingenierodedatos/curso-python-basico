"""Lección 5: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_05_funciones_y_modulos/ejemplos.py

Después cambia valores y vuelve a correrlo. Experimentar aquí no afecta tus pruebas.
"""

# Los imports van al inicio del archivo.
# math viene con Python; formato es el archivo formato.py de esta misma carpeta.
import math

import formato
from formato import describir_pedido

# --- Definir funciones: def, nombre, parámetros, docstring, cuerpo y return ---


def calcular_total(cantidad, precio_unitario):
    """Multiplica cantidad por precio unitario y redondea a dos decimales."""
    total = cantidad * precio_unitario
    return round(total, 2)


def aplicar_descuento(total, porcentaje=10):
    """Resta al total el porcentaje indicado. Si no se indica, resta 10."""
    descuento = total * porcentaje / 100
    return round(total - descuento, 2)


def calcular_minimo_y_maximo(precios):
    """Devuelve dos valores: el precio más bajo y el más alto."""
    ordenados = sorted(precios)
    return ordenados[0], ordenados[-1]


def saludar_sin_return(nombre):
    """Imprime un saludo, pero no devuelve nada."""
    print(f"Hola, {nombre}")


# --- Llamar una función: los argumentos llenan los parámetros ---
total = calcular_total(3, 45.5)
print(total)  # 136.5

# --- Argumentos por posición y por nombre ---
print(calcular_total(3, 45.5))  # por posición: el orden importa
print(calcular_total(precio_unitario=45.5, cantidad=3))  # por nombre: no importa

# --- Valores por defecto ---
print(aplicar_descuento(200))  # 180.0, usa el 10 por defecto
print(aplicar_descuento(200, 15))  # 170.0
print(aplicar_descuento(200, porcentaje=50))  # 100.0

# --- return frente a print: sin return, la función devuelve None ---
resultado = saludar_sin_return("Ana")  # imprime Hola, Ana
print(resultado)  # None

# --- Devolver varios valores: una tupla que se desempaqueta ---
precios = [120.0, 45.5, 890.0, 350.0]
minimo, maximo = calcular_minimo_y_maximo(precios)
print(minimo)  # 45.5
print(maximo)  # 890.0

# --- Funciones que se combinan: el resultado de una entra en la otra ---
total_con_descuento = aplicar_descuento(calcular_total(2, 350.0), 15)
print(total_con_descuento)  # 595.0

# --- Una lista de pedidos para los ejemplos que siguen ---
pedidos = [
    {
        "ciudad": "Puebla",
        "producto": "Taza de barro",
        "cantidad": 2,
        "precio_unitario": 120.0,
    },
    {
        "ciudad": "Mérida",
        "producto": "Filtro de tela",
        "cantidad": 5,
        "precio_unitario": 60.0,
    },
]

# --- Módulos: funciones que viven en otro archivo ---
print(math.ceil(7 / 6))  # 2: cajas de seis piezas para enviar siete
print(formato.formatear_importe(total))  # $136.50 MXN
print(describir_pedido(pedidos[0]))  # 2 x Taza de barro: $240.00 MXN

# Una función importada se usa igual que una definida aquí.
for pedido in pedidos:
    print(describir_pedido(pedido))
