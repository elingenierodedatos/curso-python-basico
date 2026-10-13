"""Lección 2: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_02_listas_y_bucles/ejemplos.py

Después cambia valores y vuelve a correrlo. Experimentar aquí no afecta tus pruebas.
"""

# --- Una lista: varios valores en orden, bajo un solo nombre ---
ciudades = ["Puebla", "Mérida", "Tijuana"]
importes = [450.0, 1250.5, 89.9, 780.0]

print(ciudades)  # ['Puebla', 'Mérida', 'Tijuana']

# --- Índices: se cuenta desde 0; el -1 es el último ---
print(ciudades[0])  # Puebla
print(ciudades[2])  # Tijuana
print(ciudades[-1])  # Tijuana

# --- Modificar, agregar y contar ---
ciudades[1] = "Monterrey"
ciudades.append("Guadalajara")

print(ciudades)  # ['Puebla', 'Monterrey', 'Tijuana', 'Guadalajara']
print(len(ciudades))  # 4

# --- sorted() devuelve una lista nueva; .sort() cambia la original ---
ordenados = sorted(importes)
print(ordenados)  # [89.9, 450.0, 780.0, 1250.5]
print(importes)  # [450.0, 1250.5, 89.9, 780.0]

de_mayor_a_menor = sorted(importes, reverse=True)
print(de_mayor_a_menor)  # [1250.5, 780.0, 450.0, 89.9]

cantidades = [3, 1, 2]
cantidades.sort()
print(cantidades)  # [1, 2, 3]

# --- Bucle for: las líneas con sangría se repiten una vez por elemento ---
for ciudad in ciudades:
    print(f"Envío a {ciudad}")
print("Fin de los envíos")  # sin sangría: se ejecuta una sola vez

# --- Patrón acumulador con un número: empieza en 0 y crece en cada vuelta ---
total = 0
for importe in importes:
    total = total + importe

print(total)  # 2570.4

# --- Patrón acumulador con una lista: empieza vacía y se llena con append ---
productos_crudos = ["  café de olla", "TAZA DE BARRO ", " filtro de tela "]
productos_limpios = []
for producto in productos_crudos:
    productos_limpios.append(producto.strip().lower())

print(productos_limpios)  # ['café de olla', 'taza de barro', 'filtro de tela']
print(productos_crudos)  # la lista original sigue igual

# --- range: una serie de números, útil para recorrer posiciones ---
for numero in range(3):
    print(numero)  # 0, 1 y 2

productos = ["Café de olla", "Taza de barro", "Filtro de tela"]
existencias = [12, 0, 30]
for posicion in range(len(productos)):
    print(f"{productos[posicion]}: {existencias[posicion]} piezas")

# --- sum, min y max ---
print(sum(importes))  # 2570.4
print(min(importes))  # 89.9
print(max(importes))  # 1250.5

# --- Slices: un tramo de la lista, como lista nueva ---
print(importes[:2])  # [450.0, 1250.5]
print(importes[1:3])  # [1250.5, 89.9]
print(importes[-2:])  # [89.9, 780.0]
print(importes[:10])  # un slice que pide de más no falla: devuelve lo que hay

# --- Copiar frente a asignar ---
pedidos = [1001, 1002, 1003]
misma_lista = pedidos  # otro nombre para la misma lista
copia = pedidos[:]  # una lista nueva con los mismos valores

pedidos.append(1004)

print(misma_lista)  # [1001, 1002, 1003, 1004]
print(copia)  # [1001, 1002, 1003]

# --- Tuplas: como una lista, pero no se pueden cambiar ---
estados = ("entregado", "enviado", "cancelado")

print(estados[0])  # entregado
print(len(estados))  # 3
