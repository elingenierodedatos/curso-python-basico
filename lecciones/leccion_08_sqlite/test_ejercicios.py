"""Pruebas de la lección 8. No modifiques este archivo."""

import sqlite3
from contextlib import closing

import pytest

from lecciones.leccion_08_sqlite.ejercicios import (
    abrir_base,
    buscar_por_ciudad,
    contar_pedidos,
    crear_tabla,
    insertar_pedido,
    insertar_varios,
    ventas_por_ciudad,
)

COLUMNAS = [
    "id_pedido",
    "fecha",
    "cliente",
    "ciudad",
    "producto",
    "cantidad",
    "precio_unitario",
    "estado",
]

SQL_CREAR_TABLA = """
    CREATE TABLE pedidos (
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

SQL_INSERTAR = "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

SQL_LEER_TODO = """
    SELECT id_pedido, fecha, cliente, ciudad, producto,
           cantidad, precio_unitario, estado
    FROM pedidos
    ORDER BY id_pedido
"""

# Están desordenadas a propósito: el orden lo debe poner la consulta.
FILAS = [
    (
        6,
        "2024-03-04",
        "Jorge Castillo",
        "Ek' Balam",
        "Taza de barro",
        2,
        120.0,
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
        8,
        "2024-03-05",
        "Ana López",
        "Ciudad de México",
        "Filtro de tela",
        3,
        65.1,
        "enviado",
    ),
    (
        1,
        "2024-03-01",
        "Ana López",
        "Ciudad de México",
        "Café de olla",
        3,
        89.9,
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
        2,
        "2024-03-01",
        "Luis Hernández",
        "Guadalajara",
        "Prensa francesa",
        1,
        499.0,
        "enviado",
    ),
    (7, "2024-03-05", "Carla Mendoza", "Puebla", "Café de olla", 5, 89.9, "cancelado"),
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
]


def fila_a_pedido(fila):
    pedido = {}
    for posicion in range(len(COLUMNAS)):
        pedido[COLUMNAS[posicion]] = fila[posicion]
    return pedido


def pedidos_de_ejemplo():
    pedidos = []
    for fila in FILAS:
        pedidos.append(fila_a_pedido(fila))
    return pedidos


def pedidos_ordenados():
    pedidos = []
    for fila in sorted(FILAS):
        pedidos.append(fila_a_pedido(fila))
    return pedidos


def leer_todo(conexion):
    pedidos = []
    for fila in conexion.execute(SQL_LEER_TODO).fetchall():
        pedidos.append(fila_a_pedido(fila))
    return pedidos


@pytest.fixture
def base_vacia():
    """Base de datos en memoria, sin tablas. Se cierra al terminar la prueba."""
    with closing(sqlite3.connect(":memory:")) as conexion:
        yield conexion


@pytest.fixture
def base_con_tabla(base_vacia):
    """Base de datos en memoria con la tabla pedidos vacía."""
    base_vacia.execute(SQL_CREAR_TABLA)
    return base_vacia


@pytest.fixture
def base_con_pedidos(base_con_tabla):
    """Base de datos en memoria con los ocho pedidos de ejemplo."""
    base_con_tabla.executemany(SQL_INSERTAR, FILAS)
    base_con_tabla.commit()
    return base_con_tabla


# --- Ejercicio 1: abrir_base ---


def test_ejercicio_1_devuelve_una_conexion_que_funciona(tmp_path):
    ruta = tmp_path / "tienda.db"

    with closing(abrir_base(ruta)) as conexion:
        es_conexion = isinstance(conexion, sqlite3.Connection)

    assert es_conexion, (
        "abrir_base() debe devolver la conexión que entrega sqlite3.connect(). "
        f"Devolvió {conexion!r}, que es de tipo {type(conexion).__name__}. "
        "Revisa que la función termine con return."
    )


def test_ejercicio_1_crea_el_archivo_de_la_base(tmp_path):
    ruta = tmp_path / "tienda.db"

    with closing(abrir_base(ruta)) as conexion:
        conexion.execute("CREATE TABLE notas (texto TEXT)")
        conexion.commit()

    assert ruta.is_file(), (
        f"Después de abrir_base({ruta.name!r}) y de guardar una tabla, se esperaba "
        "que existiera el archivo de la base y no existe. Abre la conexión "
        "con la ruta que recibe la función, no con una ruta fija ni en memoria."
    )


def test_ejercicio_1_crea_la_carpeta_si_no_existe(tmp_path):
    ruta = tmp_path / "datos" / "bases" / "tienda.db"

    with closing(abrir_base(ruta)) as conexion:
        conexion.execute("CREATE TABLE notas (texto TEXT)")
        conexion.commit()

    assert ruta.is_file(), (
        "Con una ruta dentro de carpetas que aún no existen (datos/bases/tienda.db) "
        "se esperaba que abrir_base() las creara y luego abriera la base, "
        "pero el archivo no existe. La carpeta se crea antes de conectar."
    )


def test_ejercicio_1_no_falla_si_la_carpeta_ya_existe(tmp_path):
    ruta = tmp_path / "datos" / "tienda.db"
    ruta.parent.mkdir()
    with closing(abrir_base(ruta)) as conexion:
        conexion.execute("CREATE TABLE notas (texto TEXT)")
        conexion.execute("INSERT INTO notas VALUES (?)", ("sigue aquí",))
        conexion.commit()

    with closing(abrir_base(ruta)) as conexion:
        filas = conexion.execute("SELECT texto FROM notas").fetchall()

    assert filas == [("sigue aquí",)], (
        "Al abrir por segunda vez una base que ya existía se esperaba encontrar "
        f"lo guardado, [('sigue aquí',)], y se obtuvo {filas!r}. "
        "abrir_base() no debe borrar ni reemplazar un archivo existente."
    )


# --- Ejercicio 2: crear_tabla ---


def test_ejercicio_2_crea_la_tabla_pedidos(base_vacia):
    crear_tabla(base_vacia)

    sql = "SELECT name FROM sqlite_master WHERE type = 'table'"
    tablas = base_vacia.execute(sql).fetchall()

    assert tablas == [("pedidos",)], (
        "Después de crear_tabla() se esperaba una sola tabla llamada 'pedidos' "
        f"y la base tiene estas tablas: {tablas!r}. Revisa el nombre en tu "
        "CREATE TABLE."
    )


def test_ejercicio_2_tiene_las_columnas_en_orden(base_vacia):
    crear_tabla(base_vacia)

    columnas = []
    for fila in base_vacia.execute("PRAGMA table_info(pedidos)").fetchall():
        columnas.append(fila[1])

    assert columnas == COLUMNAS, (
        f"Se esperaban las columnas {COLUMNAS!r} y la tabla tiene {columnas!r}. "
        "Revisa los nombres y el orden: son los mismos del docstring."
    )


@pytest.mark.parametrize(
    ("columna", "tipo_esperado"),
    [
        ("id_pedido", "INTEGER"),
        ("fecha", "TEXT"),
        ("cliente", "TEXT"),
        ("ciudad", "TEXT"),
        ("producto", "TEXT"),
        ("cantidad", "INTEGER"),
        ("precio_unitario", "REAL"),
        ("estado", "TEXT"),
    ],
)
def test_ejercicio_2_cada_columna_tiene_su_tipo(base_vacia, columna, tipo_esperado):
    crear_tabla(base_vacia)

    tipos = {}
    for fila in base_vacia.execute("PRAGMA table_info(pedidos)").fetchall():
        tipos[fila[1]] = fila[2].upper()
    tipo = tipos.get(columna)

    assert tipo == tipo_esperado, (
        f"Para la columna {columna!r} se esperaba el tipo {tipo_esperado!r} "
        f"y se obtuvo {tipo!r}. Los números enteros van como INTEGER, "
        "los que llevan decimales como REAL y el texto como TEXT."
    )


def test_ejercicio_2_llamarla_dos_veces_no_falla_ni_borra_datos(base_vacia):
    crear_tabla(base_vacia)
    base_vacia.execute(SQL_INSERTAR, FILAS[0])

    crear_tabla(base_vacia)

    filas = base_vacia.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]

    assert filas == 1, (
        "Con un pedido guardado, al llamar crear_tabla() por segunda vez se "
        f"esperaba que siguiera habiendo 1 fila y hay {filas!r}. "
        "La tabla solo se crea si todavía no existe."
    )


def test_ejercicio_2_id_pedido_es_la_clave_primaria(base_vacia):
    crear_tabla(base_vacia)
    base_vacia.execute(SQL_INSERTAR, FILAS[0])

    repetido_rechazado = False
    try:
        base_vacia.execute(SQL_INSERTAR, FILAS[0])
    except sqlite3.IntegrityError:
        repetido_rechazado = True

    assert repetido_rechazado, (
        "Al insertar dos veces el mismo id_pedido se esperaba que SQLite lo "
        "rechazara con IntegrityError y lo aceptó. Marca la columna id_pedido "
        "como clave primaria."
    )


# --- Ejercicio 3: insertar_pedido ---


def test_ejercicio_3_guarda_todas_las_columnas(base_con_tabla):
    pedido = fila_a_pedido(FILAS[3])

    insertar_pedido(base_con_tabla, pedido)

    guardados = leer_todo(base_con_tabla)

    assert guardados == [pedido], (
        f"Después de insertar {pedido!r} se esperaba encontrar justo ese pedido "
        f"en la tabla y se encontró {guardados!r}. Revisa que cada valor "
        "vaya a su columna."
    )


def test_ejercicio_3_acepta_textos_con_apostrofo_y_comillas(base_con_tabla):
    pedido = fila_a_pedido(FILAS[7])

    insertar_pedido(base_con_tabla, pedido)

    sql = "SELECT cliente, producto FROM pedidos"
    guardado = base_con_tabla.execute(sql).fetchone()
    esperado = ("Rómulo O'Farrill", 'Taza "La Abuela\'s"')

    assert guardado == esperado, (
        f"Con cliente={pedido['cliente']!r} y producto={pedido['producto']!r} "
        f"se esperaba guardar {esperado!r} y se obtuvo {guardado!r}. "
        "Los valores deben viajar como parámetros, no pegados dentro del SQL."
    )


def test_ejercicio_3_guarda_un_texto_con_sql_tal_cual(base_con_tabla):
    pedido = fila_a_pedido(FILAS[0])
    pedido["cliente"] = "x'); DELETE FROM pedidos; --"

    insertar_pedido(base_con_tabla, pedido)

    guardado = base_con_tabla.execute("SELECT cliente FROM pedidos").fetchone()

    assert guardado == (pedido["cliente"],), (
        f"Con cliente={pedido['cliente']!r} se esperaba guardar ese texto "
        f"sin cambios y se obtuvo {guardado!r}. Un valor nunca debe "
        "interpretarse como parte de la instrucción."
    )


def test_ejercicio_3_no_depende_del_orden_de_las_claves(base_con_tabla):
    pedido = fila_a_pedido(FILAS[1])
    al_reves = {}
    for clave in reversed(COLUMNAS):
        al_reves[clave] = pedido[clave]

    insertar_pedido(base_con_tabla, al_reves)

    guardados = leer_todo(base_con_tabla)

    assert guardados == [pedido], (
        "Con un diccionario cuyas claves vienen en otro orden se esperaba "
        f"guardar {pedido!r} y se guardó {guardados!r}. Toma cada valor "
        "por su clave, no por la posición que ocupa en el diccionario."
    )


def test_ejercicio_3_no_modifica_el_diccionario(base_con_tabla):
    pedido = fila_a_pedido(FILAS[0])
    copia = dict(pedido)

    insertar_pedido(base_con_tabla, pedido)

    assert pedido == copia, (
        f"El diccionario recibido era {copia!r} y después de insertar_pedido() "
        f"quedó como {pedido!r}. La función solo debe leerlo."
    )


def test_ejercicio_3_confirma_el_cambio_con_commit(tmp_path):
    ruta = tmp_path / "tienda.db"
    with closing(sqlite3.connect(ruta)) as conexion:
        conexion.execute(SQL_CREAR_TABLA)
        insertar_pedido(conexion, fila_a_pedido(FILAS[0]))

    with closing(sqlite3.connect(ruta)) as otra_conexion:
        filas = otra_conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]

    assert filas == 1, (
        "Después de insertar un pedido, cerrar la base y volver a abrirla "
        f"se esperaba encontrar 1 fila y hay {filas!r}. Sin confirmar el "
        "cambio, lo insertado se pierde al cerrar."
    )


def test_ejercicio_3_un_id_repetido_lanza_integrity_error(base_con_tabla):
    pedido = fila_a_pedido(FILAS[0])
    insertar_pedido(base_con_tabla, pedido)

    with pytest.raises(sqlite3.IntegrityError):
        insertar_pedido(base_con_tabla, pedido)


# --- Ejercicio 4: insertar_varios ---


def test_ejercicio_4_inserta_todos_los_pedidos(base_con_tabla):
    pedidos = pedidos_de_ejemplo()

    insertar_varios(base_con_tabla, pedidos)

    guardados = leer_todo(base_con_tabla)
    esperados = pedidos_ordenados()

    assert guardados == esperados, (
        f"Después de insertar los {len(pedidos)} pedidos de ejemplo se esperaba "
        f"encontrar {esperados!r} y se encontró {guardados!r}."
    )


@pytest.mark.parametrize("cuantos", [1, 3, 8])
def test_ejercicio_4_devuelve_cuantos_inserto(base_con_tabla, cuantos):
    pedidos = pedidos_de_ejemplo()[:cuantos]

    resultado = insertar_varios(base_con_tabla, pedidos)

    assert resultado == cuantos, (
        f"Con una lista de {cuantos} pedidos se esperaba que devolviera {cuantos} "
        f"y se obtuvo {resultado!r}. La función devuelve cuántos insertó."
    )


def test_ejercicio_4_con_lista_vacia_devuelve_cero(base_con_tabla):
    resultado = insertar_varios(base_con_tabla, [])

    filas = base_con_tabla.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]

    assert (resultado, filas) == (0, 0), (
        "Con una lista vacía se esperaba que devolviera 0 y que la tabla "
        f"siguiera con 0 filas. Devolvió {resultado!r} y la tabla tiene "
        f"{filas!r} filas."
    )


def test_ejercicio_4_agrega_sin_borrar_lo_que_ya_habia(base_con_tabla):
    pedidos = pedidos_de_ejemplo()
    base_con_tabla.execute(SQL_INSERTAR, FILAS[0])

    insertar_varios(base_con_tabla, pedidos[1:4])

    filas = base_con_tabla.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]

    assert filas == 4, (
        "Con 1 pedido ya guardado, después de insertar 3 más se esperaban "
        f"4 filas y hay {filas!r}. Insertar agrega filas, no reemplaza."
    )


def test_ejercicio_4_no_modifica_la_lista_ni_sus_pedidos(base_con_tabla):
    pedidos = pedidos_de_ejemplo()
    copia = pedidos_de_ejemplo()

    insertar_varios(base_con_tabla, pedidos)

    assert pedidos == copia, (
        "La lista recibida cambió después de llamar a insertar_varios(). "
        f"Era {copia!r} y quedó como {pedidos!r}. La función solo debe leerla."
    )


def test_ejercicio_4_confirma_el_cambio_con_commit(tmp_path):
    ruta = tmp_path / "tienda.db"
    with closing(sqlite3.connect(ruta)) as conexion:
        conexion.execute(SQL_CREAR_TABLA)
        insertar_varios(conexion, pedidos_de_ejemplo())

    with closing(sqlite3.connect(ruta)) as otra_conexion:
        filas = otra_conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]

    assert filas == 8, (
        "Después de insertar 8 pedidos, cerrar la base y volver a abrirla "
        f"se esperaba encontrar 8 filas y hay {filas!r}. Sin confirmar el "
        "cambio, lo insertado se pierde al cerrar."
    )


# --- Ejercicio 5: contar_pedidos ---


def test_ejercicio_5_tabla_vacia_devuelve_cero(base_con_tabla):
    resultado = contar_pedidos(base_con_tabla)

    assert resultado == 0, (
        f"Con la tabla vacía se esperaba 0 y se obtuvo {resultado!r}. "
        "Recuerda que fetchone() entrega una tupla: el número está dentro."
    )


def test_ejercicio_5_cuenta_todas_las_filas(base_con_pedidos):
    resultado = contar_pedidos(base_con_pedidos)

    assert resultado == 8, (
        f"Con los 8 pedidos de ejemplo se esperaba 8 y se obtuvo {resultado!r}. "
        "Se cuentan todas las filas, sin importar su estado."
    )


def test_ejercicio_5_devuelve_un_entero(base_con_pedidos):
    resultado = contar_pedidos(base_con_pedidos)

    assert isinstance(resultado, int), (
        "contar_pedidos() debe devolver un número entero (int). "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}. "
        "Saca el número de la tupla que entrega fetchone()."
    )


def test_ejercicio_5_el_conteo_cambia_al_insertar(base_con_pedidos):
    nueva = (
        9,
        "2024-03-06",
        "Ana López",
        "Tijuana",
        "Café de olla",
        1,
        89.9,
        "enviado",
    )
    base_con_pedidos.execute(SQL_INSERTAR, nueva)

    resultado = contar_pedidos(base_con_pedidos)

    assert resultado == 9, (
        "Con 8 pedidos y uno más recién insertado se esperaba 9 y se obtuvo "
        f"{resultado!r}. El número debe salir de una consulta a la tabla."
    )


# --- Ejercicio 6: buscar_por_ciudad ---


def test_ejercicio_6_devuelve_diccionarios_con_todas_las_columnas(base_con_pedidos):
    resultado = buscar_por_ciudad(base_con_pedidos, "Mérida")

    esperado = [fila_a_pedido(FILAS[7])]

    assert resultado == esperado, (
        f"Con ciudad='Mérida' se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "Cada fila se convierte en un diccionario con las ocho columnas."
    )


def test_ejercicio_6_ordena_por_id_pedido(base_con_pedidos):
    resultado = buscar_por_ciudad(base_con_pedidos, "Ciudad de México")

    esperado = [
        fila_a_pedido(FILAS[3]),
        fila_a_pedido(FILAS[1]),
        fila_a_pedido(FILAS[2]),
    ]

    assert resultado == esperado, (
        "Con ciudad='Ciudad de México' se esperaban los pedidos 1, 3 y 8, "
        f"en ese orden, y se obtuvo {resultado!r}. Filtra por la ciudad "
        "y ordena por id_pedido."
    )


def test_ejercicio_6_ciudad_inexistente_devuelve_lista_vacia(base_con_pedidos):
    resultado = buscar_por_ciudad(base_con_pedidos, "Atlantis")

    assert resultado == [], (
        f"Con ciudad='Atlantis', que no tiene pedidos, se esperaba [] "
        f"y se obtuvo {resultado!r}."
    )


def test_ejercicio_6_ciudad_con_apostrofo_no_rompe_la_consulta(base_con_pedidos):
    resultado = buscar_por_ciudad(base_con_pedidos, "Ek' Balam")

    esperado = [fila_a_pedido(FILAS[0])]

    assert resultado == esperado, (
        f'Con ciudad="Ek\' Balam" se esperaba {esperado!r} y se obtuvo '
        f"{resultado!r}. La ciudad debe viajar como parámetro."
    )


def test_ejercicio_6_un_texto_con_sql_no_cambia_la_consulta(base_con_pedidos):
    ciudad = "Mérida' OR '1' = '1"

    resultado = buscar_por_ciudad(base_con_pedidos, ciudad)

    assert resultado == [], (
        f"Con ciudad={ciudad!r} se esperaba [] porque ninguna ciudad se llama así, "
        f"y se obtuvieron {len(resultado)} pedidos. Si armas el SQL pegando "
        "el texto, quien escribe la ciudad puede cambiar tu consulta."
    )


def test_ejercicio_6_incluye_los_cancelados_de_esa_ciudad(base_con_pedidos):
    resultado = buscar_por_ciudad(base_con_pedidos, "Guadalajara")

    ids = []
    for pedido in resultado:
        ids.append(pedido["id_pedido"])

    assert ids == [2, 5], (
        "Con ciudad='Guadalajara' se esperaban los pedidos [2, 5] (el cancelado "
        f"también cuenta en esta búsqueda) y se obtuvieron {ids!r}."
    )


# --- Ejercicio 7: ventas_por_ciudad ---


def test_ejercicio_7_tabla_vacia_devuelve_lista_vacia(base_con_tabla):
    resultado = ventas_por_ciudad(base_con_tabla)

    assert resultado == [], (
        f"Con la tabla vacía se esperaba [] y se obtuvo {resultado!r}."
    )


def test_ejercicio_7_suma_por_ciudad_de_mayor_a_menor(base_con_pedidos):
    resultado = ventas_por_ciudad(base_con_pedidos)

    esperado = [
        ("Ciudad de México", 1715.5),
        ("Guadalajara", 499.0),
        ("Mérida", 370.0),
        ("Ek' Balam", 240.0),
    ]

    assert resultado == esperado, (
        f"Con los pedidos de ejemplo se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Suma cantidad por precio_unitario en cada ciudad, "
        "deja fuera los cancelados y ordena del total más alto al más bajo."
    )


def test_ejercicio_7_no_cuenta_los_cancelados(base_con_tabla):
    filas = [
        (1, "2024-03-01", "Ana López", "Puebla", "Café de olla", 2, 100.0, "entregado"),
        (
            2,
            "2024-03-01",
            "Ana López",
            "Puebla",
            "Taza de barro",
            5,
            100.0,
            "cancelado",
        ),
        (
            3,
            "2024-03-02",
            "Luis Hernández",
            "Tijuana",
            "Café de olla",
            9,
            100.0,
            "cancelado",
        ),
    ]
    base_con_tabla.executemany(SQL_INSERTAR, filas)

    resultado = ventas_por_ciudad(base_con_tabla)

    assert resultado == [("Puebla", 200.0)], (
        "Con un pedido entregado de 200.0 en Puebla, uno cancelado en Puebla y "
        "uno cancelado en Tijuana se esperaba [('Puebla', 200.0)] y se obtuvo "
        f"{resultado!r}. Una ciudad que solo tiene cancelados no aparece."
    )


def test_ejercicio_7_redondea_a_dos_decimales(base_con_tabla):
    filas = [
        (
            1,
            "2024-03-01",
            "Ana López",
            "Puebla",
            "Filtro de tela",
            3,
            19.99,
            "entregado",
        ),
        (2, "2024-03-01", "Ana López", "Puebla", "Filtro de tela", 3, 0.1, "enviado"),
    ]
    base_con_tabla.executemany(SQL_INSERTAR, filas)

    resultado = ventas_por_ciudad(base_con_tabla)

    assert resultado == [("Puebla", 60.27)], (
        "Con 3 piezas de 19.99 y 3 piezas de 0.1 en Puebla se esperaba "
        f"[('Puebla', 60.27)] y se obtuvo {resultado!r}. El total se "
        "redondea a dos decimales."
    )


def test_ejercicio_7_cada_elemento_es_una_tupla_ciudad_total(base_con_pedidos):
    resultado = ventas_por_ciudad(base_con_pedidos)

    primero = resultado[0]

    assert isinstance(primero, tuple) and len(primero) == 2, (
        "Cada elemento debe ser una tupla (ciudad, total). El primero fue "
        f"{primero!r}. Pide en el SELECT solo esas dos columnas."
    )
