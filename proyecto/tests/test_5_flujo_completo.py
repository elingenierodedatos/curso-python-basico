"""Pruebas del flujo completo. No modifiques este archivo."""

import csv
import json
import sqlite3

import pytest
from conftest import COLUMNAS, RUTA_DATOS
from flujo_ventas import principal


def leer_filas(ruta):
    with ruta.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


# --- guardar_rechazados ---


def test_flujo_guardar_rechazados_escribe_motivo_y_datos(tmp_path):
    ruta = tmp_path / "salida" / "rechazados.csv"
    datos = {columna: f"valor de {columna}" for columna in COLUMNAS}
    datos["ciudad"] = "N/D"
    rechazados = [{"fila": 4, "motivo": "ciudad faltante", "datos": datos}]

    escritos = principal.guardar_rechazados(ruta, rechazados)

    assert escritos == 1, f"Debe devolver cuántos escribió: 1. Devolvió {escritos!r}."
    assert ruta.exists(), "No se creó rechazados.csv. Hay que crear la carpeta."
    filas = leer_filas(ruta)
    assert list(filas[0]) == ["fila", "motivo", *COLUMNAS], (
        f"Las columnas deben ser fila, motivo y luego las del archivo original. "
        f"Fueron {list(filas[0])}."
    )
    assert filas[0]["fila"] == "4", f"La fila debe ser 4 y fue {filas[0]['fila']!r}."
    assert filas[0]["motivo"] == "ciudad faltante", (
        f"El motivo debe ser 'ciudad faltante' y fue {filas[0]['motivo']!r}."
    )
    assert filas[0]["ciudad"] == "N/D", (
        "Los datos crudos se guardan tal como llegaron, sin limpiar."
    )


def test_flujo_guardar_rechazados_sin_rechazados_deja_solo_el_encabezado(tmp_path):
    ruta = tmp_path / "rechazados.csv"

    escritos = principal.guardar_rechazados(ruta, [])

    assert escritos == 0, f"Sin rechazados debe devolver 0 y devolvió {escritos!r}."
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    assert lineas == [",".join(["fila", "motivo", *COLUMNAS])], (
        f"El archivo debe tener solo el encabezado. Contiene: {lineas!r}."
    )


# --- ejecutar_flujo con un archivo pequeño ---


def test_flujo_devuelve_el_reporte(csv_pequeno, tmp_path):
    reporte = principal.ejecutar_flujo(csv_pequeno, tmp_path / "salida")

    assert isinstance(reporte, dict), (
        f"ejecutar_flujo() debe devolver el reporte y devolvió {reporte!r}."
    )
    esperado = {
        "pedidos_cargados": 3,
        "pedidos_rechazados": 3,
        "pedidos_cancelados": 1,
        "ventas_totales": 2871.0,
        "motivos_de_rechazo": {
            "ciudad faltante": 1,
            "id_pedido duplicado": 1,
            "cantidad inválida": 1,
        },
    }
    for clave, valor in esperado.items():
        assert reporte[clave] == valor, (
            f"En {clave!r} se esperaba {valor!r} y se obtuvo {reporte[clave]!r}. "
            "El archivo de prueba tiene 6 filas: 3 válidas (una cancelada), "
            "2 con errores y 1 duplicada."
        )
    assert reporte["ventas_por_ciudad"] == [
        {"ciudad": "Ciudad de México", "pedidos": 1, "total": 2501.0},
        {"ciudad": "Mérida", "pedidos": 1, "total": 370.0},
    ], f"ventas_por_ciudad no coincide. Se obtuvo {reporte['ventas_por_ciudad']!r}."


def test_flujo_crea_los_tres_archivos_de_salida(csv_pequeno, tmp_path):
    salida = tmp_path / "salida"

    reporte = principal.ejecutar_flujo(csv_pequeno, salida)

    for nombre in ("ventas.db", "reporte.json", "rechazados.csv"):
        assert (salida / nombre).exists(), f"Falta el archivo de salida {nombre}."
    guardado = json.loads((salida / "reporte.json").read_text(encoding="utf-8"))
    assert guardado == reporte, (
        "reporte.json debe contener el mismo reporte que devuelve ejecutar_flujo()."
    )
    assert len(leer_filas(salida / "rechazados.csv")) == 3, (
        "rechazados.csv debe tener los 3 pedidos rechazados."
    )


def test_flujo_guarda_los_pedidos_limpios_en_la_base(csv_pequeno, tmp_path):
    salida = tmp_path / "salida"

    principal.ejecutar_flujo(csv_pequeno, salida)

    conexion = sqlite3.connect(salida / "ventas.db")
    try:
        filas = conexion.execute(
            "SELECT id_pedido, ciudad, producto, total FROM pedidos ORDER BY id_pedido"
        ).fetchall()
    finally:
        conexion.close()
    assert filas == [
        (1, "Ciudad de México", "Café de olla", 2501.0),
        (3, "Puebla", "Café de olla", 370.0),
        (5, "Mérida", "Taza de barro", 370.0),
    ], f"La tabla pedidos no tiene los datos limpios esperados. Tiene: {filas!r}."


def test_flujo_se_puede_correr_dos_veces(csv_pequeno, tmp_path):
    salida = tmp_path / "salida"

    primero = principal.ejecutar_flujo(csv_pequeno, salida)
    segundo = principal.ejecutar_flujo(csv_pequeno, salida)

    assert primero == segundo, (
        "Correr el flujo dos veces debe dar el mismo reporte. La segunda corrida "
        f"dio pedidos_cargados={segundo['pedidos_cargados']!r}."
    )


def test_flujo_cierra_la_conexion(csv_pequeno, tmp_path):
    salida = tmp_path / "salida"

    principal.ejecutar_flujo(csv_pequeno, salida)

    try:
        (salida / "ventas.db").unlink()
    except PermissionError:
        pytest.fail(
            "No se pudo borrar ventas.db: la conexión sigue abierta. "
            "Ciérrala al terminar el flujo."
        )


# --- ejecutar_flujo con los datos del proyecto ---


def test_flujo_con_los_datos_del_proyecto(tmp_path):
    reporte = principal.ejecutar_flujo(RUTA_DATOS, tmp_path / "salida")

    esperado = {
        "pedidos_cargados": 50,
        "pedidos_rechazados": 13,
        "pedidos_cancelados": 12,
        "ventas_totales": 44707.2,
    }
    for clave, valor in esperado.items():
        assert reporte[clave] == valor, (
            f"Con proyecto/datos/pedidos_crudos.csv, en {clave!r} se esperaba "
            f"{valor!r} y se obtuvo {reporte[clave]!r}."
        )
    assert reporte["motivos_de_rechazo"] == {
        "ciudad faltante": 2,
        "cantidad inválida": 3,
        "id_pedido duplicado": 3,
        "precio inválido": 2,
        "fecha inválida": 1,
        "producto faltante": 1,
        "id_pedido inválido": 1,
    }, f"Los motivos de rechazo no coinciden: {reporte['motivos_de_rechazo']!r}."
    primera = reporte["ventas_por_ciudad"][0]
    assert primera == {"ciudad": "Monterrey", "pedidos": 10, "total": 12171.2}, (
        f"La ciudad con más ventas es Monterrey, con 12171.2. Se obtuvo {primera!r}."
    )
    ciudades = sorted(fila["ciudad"] for fila in reporte["ventas_por_ciudad"])
    assert ciudades == sorted(
        [
            "Ciudad de México",
            "Guadalajara",
            "Monterrey",
            "Mérida",
            "Puebla",
            "San Luis Potosí",
            "Tijuana",
        ]
    ), f"Deben aparecer 7 ciudades, cada una escrita de una sola forma: {ciudades!r}."
