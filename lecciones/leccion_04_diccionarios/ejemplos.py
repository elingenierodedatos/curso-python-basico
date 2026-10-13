"""Lección 4: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_04_diccionarios/ejemplos.py

Después cambia valores y vuelve a correrlo. Experimentar aquí no afecta tus pruebas.
"""

# --- Un diccionario es un registro: clave = columna, valor = dato ---
pedido = {
    "id_pedido": 1001,
    "producto": "Café de olla",
    "cantidad": 2,
    "precio_unitario": 185.0,
}

print(pedido["producto"])  # Café de olla
print(len(pedido))  # 4

# --- Agregar y modificar: la misma sintaxis ---
pedido["estado"] = "enviado"  # la clave no existía: se agrega
pedido["cantidad"] = 3  # la clave ya existía: se cambia su valor
print(pedido)

# --- Leer sin romper el programa: .get() e in ---
print(pedido.get("ciudad"))  # None
print(pedido.get("ciudad", "sin ciudad"))  # sin ciudad
print("ciudad" in pedido)  # False
print("producto" in pedido)  # True

# --- Borrar una clave ---
del pedido["estado"]
print(pedido)

# --- Recorrer un diccionario ---
for clave, valor in pedido.items():
    print(f"{clave}: {valor}")

for clave in pedido.keys():
    print(clave)

for valor in pedido.values():
    print(valor)

# --- Lista de diccionarios: una tabla ---
pedidos = [
    {"id_pedido": 1001, "ciudad": "Puebla", "cantidad": 2, "estado": "entregado"},
    {"id_pedido": 1002, "ciudad": "Monterrey", "cantidad": 1, "estado": "enviado"},
    {"id_pedido": 1003, "ciudad": "Puebla", "cantidad": 4, "estado": "entregado"},
    {"id_pedido": 1004, "ciudad": "Tijuana", "cantidad": 3, "estado": "cancelado"},
    {"id_pedido": 1005, "ciudad": "Puebla", "cantidad": 5, "estado": "entregado"},
]

print(len(pedidos))  # 5 filas
print(pedidos[0]["ciudad"])  # Puebla

for fila in pedidos:
    print(fila["id_pedido"], fila["estado"])

# --- Contar por grupo ---
conteo = {}
for fila in pedidos:
    estado = fila["estado"]
    conteo[estado] = conteo.get(estado, 0) + 1

print(conteo)  # {'entregado': 3, 'enviado': 1, 'cancelado': 1}

# --- Sumar por grupo ---
piezas = {}
for fila in pedidos:
    ciudad = fila["ciudad"]
    piezas[ciudad] = piezas.get(ciudad, 0) + fila["cantidad"]

print(piezas)  # {'Puebla': 11, 'Monterrey': 1, 'Tijuana': 3}

# --- Conjuntos: valores únicos, sin orden ---
estados = set()
for fila in pedidos:
    estados.add(fila["estado"])

print(len(estados))  # 3
print(estados)  # el orden puede cambiar cada vez que corres el archivo
print(sorted(estados))  # ['cancelado', 'entregado', 'enviado']

# --- Dos nombres, un solo diccionario ---
original = {"id_pedido": 1001, "estado": "enviado"}
otro_nombre = original
otro_nombre["estado"] = "entregado"
print(original["estado"])  # entregado: el original también cambió

# --- Con .copy() cada nombre tiene su propio diccionario ---
original = {"id_pedido": 1001, "estado": "enviado"}
copia = original.copy()
copia["estado"] = "entregado"
print(original["estado"])  # enviado
print(copia["estado"])  # entregado
