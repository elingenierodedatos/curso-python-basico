"""Lección 8: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_08_sqlite/ejemplos.py

Después cambia valores y vuelve a correrlo. Experimentar aquí no afecta tus pruebas.
La base vive en la memoria (":memory:"), así que no se crea ningún archivo y
todo desaparece cuando el programa termina.
"""

import sqlite3

# --- Conectar: ":memory:" crea una base temporal para practicar ---
conexion = sqlite3.connect(":memory:")

# --- CREATE TABLE: el molde de la tabla, con el tipo de cada columna ---
conexion.execute(
    """
    CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido INTEGER PRIMARY KEY,
        fecha TEXT,
        cliente TEXT,
        ciudad TEXT,
        producto TEXT,
        cantidad INTEGER,
        precio_unitario REAL,
        estado TEXT
    )
    """
)

# --- INSERT con parámetros: un "?" por valor y los valores en una tupla ---
sql_insertar = "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
pedido = (
    1,
    "2024-03-01",
    "Ana López",
    "Ciudad de México",
    "Café de olla",
    3,
    89.9,
    "entregado",
)
conexion.execute(sql_insertar, pedido)

# --- executemany: la misma instrucción para cada tupla de una lista ---
mas_pedidos = [
    (
        2,
        "2024-03-01",
        "Luis Hernández",
        "Guadalajara",
        "Prensa francesa",
        1,
        499.0,
        "enviado",
    ),
    (
        3,
        "2024-03-02",
        "María Fernández",
        "Ciudad de México",
        "Molinillo manual",
        1,
        1250.5,
        "entregado",
    ),
    (
        4,
        "2024-03-02",
        "Rómulo O'Farrill",
        "Mérida",
        'Taza "La Abuela\'s"',
        2,
        185.0,
        "entregado",
    ),
    (
        5,
        "2024-03-03",
        "Sofía Ramírez",
        "Guadalajara",
        "Filtro de tela",
        4,
        65.0,
        "cancelado",
    ),
    (
        6,
        "2024-03-04",
        "Jorge Castillo",
        "Monterrey",
        "Taza de barro",
        2,
        120.0,
        "enviado",
    ),
]
conexion.executemany(sql_insertar, mas_pedidos)

# --- commit: confirma los cambios pendientes ---
print(conexion.in_transaction)  # True: hay cambios sin confirmar
conexion.commit()
print(conexion.in_transaction)  # False: ya quedaron guardados

# --- SELECT con fetchall: una lista de tuplas, una por fila ---
filas = conexion.execute("SELECT id_pedido, cliente, ciudad FROM pedidos").fetchall()
for fila in filas:
    print(fila)

# --- WHERE con parámetro: la coma hace que ("Guadalajara",) sea una tupla ---
sql = "SELECT id_pedido, producto, estado FROM pedidos WHERE ciudad = ?"
print(conexion.execute(sql, ("Guadalajara",)).fetchall())

# --- ORDER BY: del precio más alto al más bajo ---
sql = "SELECT producto, precio_unitario FROM pedidos ORDER BY precio_unitario DESC"
for fila in conexion.execute(sql).fetchall():
    print(fila)

# --- COUNT con fetchone: una sola fila, que también es una tupla ---
fila = conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone()
print(fila)  # (6,)
print(fila[0])  # 6

# --- De tuplas a diccionarios, con un bucle ---
sql = "SELECT id_pedido, cliente, producto FROM pedidos WHERE ciudad = ?"
pedidos_de_merida = []
for fila in conexion.execute(sql, ("Mérida",)).fetchall():
    pedidos_de_merida.append(
        {"id_pedido": fila[0], "cliente": fila[1], "producto": fila[2]}
    )
print(pedidos_de_merida)

# --- GROUP BY: un renglón por ciudad, con su número de pedidos y sus piezas ---
# SQLite compara el texto carácter por carácter: por eso deja Mérida después
# de Monterrey (para él, la é va después de todas las letras sin acento).
sql = """
    SELECT ciudad, COUNT(*), SUM(cantidad)
    FROM pedidos
    GROUP BY ciudad
    ORDER BY ciudad
"""
for fila in conexion.execute(sql).fetchall():
    print(fila)

# --- El error de clave repetida, atrapado con try y except ---
try:
    conexion.execute(sql_insertar, pedido)
except sqlite3.IntegrityError as error:
    print("No se insertó:", error)

# --- Cerrar: siempre al terminar ---
conexion.close()
