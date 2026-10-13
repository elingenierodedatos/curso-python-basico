"""Lección 3: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_03_condicionales/ejemplos.py

Después cambia valores y vuelve a correrlo. Experimentar aquí no afecta tus pruebas.
"""

# --- Valores booleanos: una comparación responde True o False ---
cantidad = 3
precio_unitario = 45.5

print(cantidad == 3)  # True
print(cantidad != 3)  # False
print(precio_unitario >= 100)  # False
print(type(cantidad > 0))  # <class 'bool'>

# --- Comparar texto: mayúsculas y espacios cuentan ---
ciudad_cruda = "  PUEBLA "

print(ciudad_cruda == "puebla")  # False
print(ciudad_cruda.strip().lower() == "puebla")  # True

# --- and, or, not ---
estado = "entregado"

print(cantidad > 0 and precio_unitario > 0)  # True: se cumplen las dos
print(estado == "enviado" or estado == "entregado")  # True: se cumple una
print(not estado == "cancelado")  # True: invierte el False

# --- isinstance: pregunta si un valor es de cierto tipo ---
print(isinstance(3, int))  # True
print(isinstance("3", int))  # False

# --- in y not in: pertenencia en listas y en textos ---
ciudades_con_envio = ["Guadalajara", "Monterrey", "Puebla"]

print("Puebla" in ciudades_con_envio)  # True
print("Tijuana" not in ciudades_con_envio)  # True
print("olla" in "Café de olla")  # True

# --- if y else: dos caminos ---
if estado == "cancelado":
    mensaje = "El pedido no se cobra"
else:
    mensaje = "El pedido se cobra"

print(mensaje)  # El pedido se cobra

# --- if-elif-else: solo corre el primer bloque verdadero ---
piezas = 12

if piezas >= 10:
    tipo_de_venta = "mayoreo"
elif piezas >= 5:
    tipo_de_venta = "medio mayoreo"
else:
    tipo_de_venta = "menudeo"

print(tipo_de_venta)  # mayoreo

# El mismo código con las condiciones en otro orden da un resultado equivocado:
# 12 también es mayor o igual que 5, y el primer bloque verdadero gana.
if piezas >= 5:
    tipo_equivocado = "medio mayoreo"
elif piezas >= 10:
    tipo_equivocado = "mayoreo"
else:
    tipo_equivocado = "menudeo"

print(tipo_equivocado)  # medio mayoreo

# --- None: no hay valor ---
fecha_de_entrega = None

print(fecha_de_entrega is None)  # True

if fecha_de_entrega is None:
    print("El pedido todavía no se entrega")

# --- if dentro de un for: filtrar ---
cantidades = [3, 0, 12, -1, 5]
cantidades_validas = []

for valor in cantidades:
    if valor > 0:
        cantidades_validas.append(valor)

print(cantidades_validas)  # [3, 12, 5]

# --- if dentro de un for: contar ---
estados = ["entregado", "cancelado", "enviado", "cancelado", "entregado"]
cancelados = 0

for estado_del_pedido in estados:
    if estado_del_pedido == "cancelado":
        cancelados += 1

print(cancelados)  # 2

# --- while con contador ---
contador = 1

while contador <= 3:
    print("Intento", contador)
    contador += 1

# --- while cuando no sabes cuántas vueltas hacen falta ---
importes = [450.0, 1200.0, 380.0, 2500.0, 99.0]
meta = 2000
acumulado = 0
posicion = 0

while acumulado < meta and posicion < len(importes):
    acumulado += importes[posicion]
    posicion += 1

print(posicion, acumulado)  # 3 2030.0

# --- break: salir del bucle antes de tiempo ---
existencias = 10
piezas_pedidas = [3, 4, 5, 2]
posicion = 0

while posicion < len(piezas_pedidas):
    if piezas_pedidas[posicion] > existencias:
        print("No alcanza para el pedido de la posición", posicion)
        break
    existencias -= piezas_pedidas[posicion]
    posicion += 1

print(existencias)  # 3
