"""Pruebas de la etapa 4: reportar. No modifiques este archivo."""

import json
import sqlite3

import pytest
from conftest import crear_limpio
from flujo_ventas import reportar

SQL_TABLA = """
    CREATE TABLE pedidos (
        id_pedido INTEGER PRIMARY KEY, fecha TEXT, cliente TEXT, ciudad TEXT,
        producto TEXT, cantidad INTEGER, precio_unitario REAL, estado TEXT, total REAL
    )
"""


def llenar(conexion, pedidos):
    """Crea la tabla y la llena sin depender de la etapa 3."""
    conexion.execute(SQL_TABLA)
    conexion.executemany(
        "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [tuple(pedido.values()) for pedido in pedidos],
    )
    conexion.commit()


@pytest.fixture
def base(conexion, pedidos_limpios):
    llenar(conexion, pedidos_limpios)
    return conexion


# --- ventas_por_ciudad ---


def test_etapa_4_ventas_por_ciudad_agrupa_y_ordena(base):
    resultado = reportar.ventas_por_ciudad(base)

    esperado = [
        {"ciudad": "Mérida", "pedidos": 1, "total": 2501.0},
        {"ciudad": "Puebla", "pedidos": 2, "total": 1015.0},
        {"ciudad": "Tijuana", "pedidos": 1, "total": 120.0},
    ]
    assert resultado == esperado, (
        f"Se esperaba {esperado!r} y se obtuvo {resultado!r}. Revisa: una fila por "
        "ciudad, sin los cancelados, de mayor a menor total, y cada elemento como "
        "diccionario con las claves ciudad, pedidos y total."
    )


def test_etapa_4_ventas_por_ciudad_no_cuenta_cancelados(conexion):
    llenar(
        conexion,
        [
            crear_limpio(1, "Puebla", "Café de olla", 1, 185.0, "cancelado"),
            crear_limpio(2, "Mérida", "Café de olla", 1, 185.0, "cancelado"),
        ],
    )

    resultado = reportar.ventas_por_ciudad(conexion)

    assert resultado == [], (
        "Si todos los pedidos están cancelados no hay ventas: se esperaba una "
        f"lista vacía y se obtuvo {resultado!r}."
    )


def test_etapa_4_ventas_por_ciudad_redondea(conexion):
    llenar(
        conexion,
        [
            crear_limpio(1, "Puebla", "Filtro de tela", 1, 0.1, "enviado"),
            crear_limpio(2, "Puebla", "Filtro de tela", 1, 0.2, "enviado"),
        ],
    )

    resultado = reportar.ventas_por_ciudad(conexion)

    assert resultado == [{"ciudad": "Puebla", "pedidos": 2, "total": 0.3}], (
        f"0.1 más 0.2 debe reportarse como 0.3. Se obtuvo {resultado!r}. "
        "Redondea la suma a 2 decimales."
    )


# --- ventas_por_producto ---


def test_etapa_4_ventas_por_producto_agrupa_y_ordena(base):
    resultado = reportar.ventas_por_producto(base)

    esperado = [
        {"producto": "Molinillo manual", "unidades": 2, "total": 2501.0},
        {"producto": "Prensa francesa", "unidades": 1, "total": 645.0},
        {"producto": "Café de olla", "unidades": 2, "total": 370.0},
        {"producto": "Taza de barro", "unidades": 1, "total": 120.0},
    ]
    assert resultado == esperado, (
        f"Se esperaba {esperado!r} y se obtuvo {resultado!r}. Las unidades son la "
        "suma de cantidad; el pedido cancelado de Café de olla no cuenta."
    )


# --- contar_motivos ---


def test_etapa_4_contar_motivos_cuenta_por_motivo():
    rechazados = [
        {"fila": 2, "motivo": "ciudad faltante", "datos": {}},
        {"fila": 5, "motivo": "cantidad inválida", "datos": {}},
        {"fila": 9, "motivo": "ciudad faltante", "datos": {}},
    ]

    resultado = reportar.contar_motivos(rechazados)

    assert resultado == {"ciudad faltante": 2, "cantidad inválida": 1}, (
        "Se esperaba {'ciudad faltante': 2, 'cantidad inválida': 1} y se obtuvo "
        f"{resultado!r}."
    )


def test_etapa_4_contar_motivos_sin_rechazados():
    resultado = reportar.contar_motivos([])

    assert resultado == {}, (
        f"Sin rechazados se espera un diccionario vacío y se obtuvo {resultado!r}."
    )


# --- construir_reporte ---


def test_etapa_4_construir_reporte_tiene_todas_las_claves(base):
    reporte = reportar.construir_reporte(base, [])

    esperadas = [
        "pedidos_cargados",
        "pedidos_rechazados",
        "pedidos_cancelados",
        "ventas_totales",
        "ventas_por_ciudad",
        "ventas_por_producto",
        "motivos_de_rechazo",
    ]
    assert isinstance(reporte, dict), (
        f"El reporte debe ser un diccionario y es {type(reporte).__name__}."
    )
    assert sorted(reporte) == sorted(esperadas), (
        f"El reporte debe tener las claves {esperadas} y tiene {list(reporte)}."
    )


def test_etapa_4_construir_reporte_calcula_los_totales(base):
    rechazados = [
        {"fila": 2, "motivo": "ciudad faltante", "datos": {}},
        {"fila": 3, "motivo": "ciudad faltante", "datos": {}},
    ]

    reporte = reportar.construir_reporte(base, rechazados)

    esperado = {
        "pedidos_cargados": 5,
        "pedidos_rechazados": 2,
        "pedidos_cancelados": 1,
        "ventas_totales": 3636.0,
        "motivos_de_rechazo": {"ciudad faltante": 2},
    }
    for clave, valor in esperado.items():
        assert reporte[clave] == valor, (
            f"En {clave!r} se esperaba {valor!r} y se obtuvo {reporte[clave]!r}. "
            "La tabla tiene 5 pedidos: uno cancelado y cuatro que suman 3636.00."
        )
    assert reporte["ventas_por_ciudad"] == reportar.ventas_por_ciudad(base), (
        "ventas_por_ciudad del reporte debe ser el resultado de ventas_por_ciudad()."
    )
    assert reporte["ventas_por_producto"] == reportar.ventas_por_producto(base), (
        "ventas_por_producto del reporte debe ser el resultado de "
        "ventas_por_producto()."
    )


def test_etapa_4_construir_reporte_con_tabla_vacia(conexion):
    llenar(conexion, [])

    reporte = reportar.construir_reporte(conexion, [])

    assert reporte["pedidos_cargados"] == 0, (
        "Con la tabla vacía, pedidos_cargados es 0."
    )
    assert reporte["ventas_totales"] == 0, (
        "Con la tabla vacía, ventas_totales debe ser 0 y fue "
        f"{reporte['ventas_totales']!r}. SUM() sobre cero filas devuelve None."
    )
    assert reporte["ventas_por_ciudad"] == [], (
        "Con la tabla vacía, ventas_por_ciudad es una lista vacía."
    )


# --- guardar_reporte ---


def test_etapa_4_guardar_reporte_escribe_json_legible(tmp_path):
    ruta = tmp_path / "salida" / "reporte.json"
    reporte = {"ventas_por_ciudad": [{"ciudad": "Mérida", "total": 2501.0}]}

    devuelto = reportar.guardar_reporte(ruta, reporte)

    assert ruta.exists(), (
        "No se creó reporte.json. La carpeta salida no existía: hay que crearla."
    )
    assert devuelto == ruta, (
        f"guardar_reporte() debe devolver la ruta del archivo. Devolvió {devuelto!r}."
    )
    texto = ruta.read_text(encoding="utf-8")
    assert json.loads(texto) == reporte, (
        "Al leer el archivo deben recuperarse los mismos datos del reporte."
    )
    assert "Mérida" in texto, (
        "Los acentos deben guardarse tal cual. El archivo contiene el texto "
        "escapado (\\u00e9) en lugar de 'Mérida'."
    )
    assert '\n  "ventas_por_ciudad"' in texto, (
        "El JSON debe guardarse con sangría de 2 espacios para que sea legible."
    )


def test_etapa_4_no_modifica_la_base(base):
    antes = base.execute("SELECT * FROM pedidos ORDER BY id_pedido").fetchall()

    reportar.construir_reporte(base, [])

    despues = base.execute("SELECT * FROM pedidos ORDER BY id_pedido").fetchall()
    assert antes == despues, "Reportar solo consulta: no debe cambiar la tabla pedidos."
    assert isinstance(base, sqlite3.Connection)
