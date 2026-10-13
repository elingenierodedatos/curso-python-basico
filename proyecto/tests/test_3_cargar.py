"""Pruebas de la etapa 3: cargar. No modifiques este archivo."""

import sqlite3

import pytest
from conftest import crear_limpio
from flujo_ventas import cargar

COLUMNAS_TABLA = [
    ("id_pedido", "INTEGER"),
    ("fecha", "TEXT"),
    ("cliente", "TEXT"),
    ("ciudad", "TEXT"),
    ("producto", "TEXT"),
    ("cantidad", "INTEGER"),
    ("precio_unitario", "REAL"),
    ("estado", "TEXT"),
    ("total", "REAL"),
]


def contar(conexion):
    return conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]


# --- abrir_base ---


def test_etapa_3_abrir_base_crea_la_carpeta_y_el_archivo(tmp_path):
    ruta = tmp_path / "salida" / "nueva" / "ventas.db"

    conexion = cargar.abrir_base(ruta)

    try:
        assert isinstance(conexion, sqlite3.Connection), (
            "abrir_base() debe devolver la conexión de sqlite3. "
            f"Devolvió {type(conexion).__name__}."
        )
        assert ruta.exists(), (
            f"No se creó el archivo {ruta.name}. La carpeta no existía: "
            "hay que crearla antes de conectar."
        )
    finally:
        if isinstance(conexion, sqlite3.Connection):
            conexion.close()


def test_etapa_3_abrir_base_acepta_memoria(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    conexion = cargar.abrir_base(":memory:")

    try:
        assert isinstance(conexion, sqlite3.Connection), (
            "Con ':memory:' abrir_base() debe devolver una conexión en memoria."
        )
        assert list(tmp_path.iterdir()) == [], (
            "Con ':memory:' no debe crearse ningún archivo ni carpeta."
        )
    finally:
        if isinstance(conexion, sqlite3.Connection):
            conexion.close()


# --- crear_tabla ---


def test_etapa_3_crear_tabla_define_las_columnas(conexion):
    cargar.crear_tabla(conexion)

    columnas = [
        (fila[1], fila[2].upper())
        for fila in conexion.execute("PRAGMA table_info(pedidos)").fetchall()
    ]
    assert columnas == COLUMNAS_TABLA, (
        f"La tabla pedidos debe tener estas columnas y tipos: {COLUMNAS_TABLA}. "
        f"Tiene: {columnas}."
    )


def test_etapa_3_crear_tabla_usa_id_pedido_como_clave_primaria(conexion):
    cargar.crear_tabla(conexion)

    claves = [
        fila[1]
        for fila in conexion.execute("PRAGMA table_info(pedidos)").fetchall()
        if fila[5]
    ]
    assert claves == ["id_pedido"], (
        f"La clave primaria debe ser id_pedido y es {claves}."
    )


def test_etapa_3_crear_tabla_se_puede_llamar_dos_veces(conexion):
    cargar.crear_tabla(conexion)

    try:
        cargar.crear_tabla(conexion)
    except sqlite3.OperationalError as error:
        pytest.fail(
            f"La segunda llamada a crear_tabla() falló con: {error}. "
            "La tabla solo debe crearse si no existe."
        )


# --- cargar_pedidos ---


def test_etapa_3_cargar_pedidos_guarda_todas_las_filas(conexion, pedidos_limpios):
    cargar.crear_tabla(conexion)

    recibidos = cargar.cargar_pedidos(conexion, pedidos_limpios)

    assert recibidos == 5, (
        f"cargar_pedidos() debe devolver cuántos pedidos recibió: 5. Devolvió "
        f"{recibidos!r}."
    )
    assert contar(conexion) == 5, (
        f"La tabla debe tener 5 filas y tiene {contar(conexion)}."
    )


def test_etapa_3_cargar_pedidos_guarda_cada_valor_en_su_columna(conexion):
    cargar.crear_tabla(conexion)
    pedido = crear_limpio(77, "Mérida", "Molinillo manual", 2, 1250.5, "enviado")

    cargar.cargar_pedidos(conexion, [pedido])

    fila = conexion.execute("SELECT * FROM pedidos").fetchone()
    assert fila == tuple(pedido.values()), (
        f"Se esperaba la fila {tuple(pedido.values())!r} y se guardó {fila!r}. "
        "Revisa el orden de los valores."
    )


def test_etapa_3_cargar_pedidos_confirma_los_cambios(tmp_path, pedidos_limpios):
    ruta = tmp_path / "ventas.db"
    conexion = cargar.abrir_base(ruta)
    try:
        cargar.crear_tabla(conexion)
        cargar.cargar_pedidos(conexion, pedidos_limpios)
    finally:
        conexion.close()

    otra = sqlite3.connect(ruta)
    try:
        filas = contar(otra)
    finally:
        otra.close()
    assert filas == 5, (
        f"Al abrir de nuevo la base debe haber 5 filas y hay {filas}. "
        "Los cambios no se guardan en el archivo hasta confirmarlos."
    )


def test_etapa_3_cargar_pedidos_se_puede_repetir(conexion, pedidos_limpios):
    cargar.crear_tabla(conexion)
    cargar.cargar_pedidos(conexion, pedidos_limpios)

    try:
        cargar.cargar_pedidos(conexion, pedidos_limpios)
    except sqlite3.IntegrityError:
        pytest.fail(
            "La segunda carga falló por clave primaria repetida. La carga debe "
            "poder repetirse: si el id_pedido ya existe, se reemplaza."
        )

    assert contar(conexion) == 5, (
        f"Tras cargar dos veces los mismos 5 pedidos debe haber 5 filas y hay "
        f"{contar(conexion)}."
    )


def test_etapa_3_cargar_pedidos_reemplaza_los_datos_del_mismo_id(conexion):
    cargar.crear_tabla(conexion)
    cargar.cargar_pedidos(
        conexion, [crear_limpio(1, "Puebla", "Café de olla", 1, 185.0, "enviado")]
    )

    cargar.cargar_pedidos(
        conexion, [crear_limpio(1, "Puebla", "Café de olla", 1, 185.0, "entregado")]
    )

    estado = conexion.execute("SELECT estado FROM pedidos").fetchone()[0]
    assert estado == "entregado", (
        "Al cargar de nuevo el pedido 1 con estado 'entregado', la tabla debe "
        f"quedar con ese estado. Tiene {estado!r}."
    )


def test_etapa_3_cargar_pedidos_resiste_comillas_y_apostrofos(conexion):
    cargar.crear_tabla(conexion)
    pedido = crear_limpio(1, "Ek' Balam", 'Taza "La Abuela"', 1, 120.0, "enviado")
    pedido["cliente"] = "Rómulo O'Farrill'); DELETE FROM pedidos; --"

    try:
        cargar.cargar_pedidos(conexion, [pedido])
    except sqlite3.Error as error:
        pytest.fail(
            f"La carga falló con un texto que trae comillas: {error}. "
            "Los valores se pasan como parámetros, no pegados dentro del SQL."
        )

    fila = conexion.execute("SELECT cliente, ciudad FROM pedidos").fetchone()
    assert fila == (pedido["cliente"], "Ek' Balam"), (
        f"El texto debe guardarse tal cual. Se guardó {fila!r}."
    )


def test_etapa_3_cargar_pedidos_con_lista_vacia(conexion):
    cargar.crear_tabla(conexion)

    recibidos = cargar.cargar_pedidos(conexion, [])

    assert recibidos == 0, (
        f"Con una lista vacía debe devolver 0 y devolvió {recibidos!r}."
    )
    assert contar(conexion) == 0, "Con una lista vacía la tabla debe quedar sin filas."
