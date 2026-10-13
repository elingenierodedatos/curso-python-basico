"""Pruebas de la etapa 1: extraer. No modifiques este archivo."""

import pytest
from conftest import COLUMNAS, RUTA_DATOS, crear_crudo, escribir_csv
from flujo_ventas import extraer


def test_etapa_1_devuelve_una_lista_de_diccionarios(tmp_path):
    ruta = escribir_csv(tmp_path / "pedidos.csv", [crear_crudo(), crear_crudo()])

    pedidos = extraer.leer_pedidos(ruta)

    assert isinstance(pedidos, list), (
        f"leer_pedidos() debe devolver una lista y devolvió {type(pedidos).__name__}."
    )
    assert len(pedidos) == 2, (
        f"El archivo tiene 2 filas de datos y se obtuvieron {len(pedidos)}. "
        "El encabezado no cuenta como fila."
    )
    assert pedidos[0] == crear_crudo(), (
        f"Cada fila debe ser un diccionario columna -> texto. Se obtuvo {pedidos[0]!r}."
    )


def test_etapa_1_no_corrige_nada(tmp_path):
    crudo = crear_crudo(ciudad="  CDMX ", precio_unitario=" $1,250.50 ")
    ruta = escribir_csv(tmp_path / "pedidos.csv", [crudo])

    pedidos = extraer.leer_pedidos(ruta)

    assert pedidos[0]["ciudad"] == "  CDMX ", (
        f"Extraer no limpia: la ciudad debe llegar tal cual, '  CDMX ', "
        f"y se obtuvo {pedidos[0]['ciudad']!r}."
    )
    assert pedidos[0]["precio_unitario"] == " $1,250.50 ", (
        "Extraer no convierte: el precio debe seguir siendo el texto original. "
        f"Se obtuvo {pedidos[0]['precio_unitario']!r}."
    )


def test_etapa_1_conserva_los_acentos(tmp_path):
    ruta = escribir_csv(
        tmp_path / "pedidos.csv", [crear_crudo(cliente="Lucía Ibáñez", ciudad="Mérida")]
    )

    pedidos = extraer.leer_pedidos(ruta)

    assert pedidos[0]["cliente"] == "Lucía Ibáñez", (
        f"Se esperaba 'Lucía Ibáñez' y se obtuvo {pedidos[0]['cliente']!r}. "
        "Indica la codificación UTF-8 al abrir el archivo."
    )


def test_etapa_1_acepta_la_ruta_como_texto(tmp_path):
    ruta = escribir_csv(tmp_path / "pedidos.csv", [crear_crudo()])

    pedidos = extraer.leer_pedidos(str(ruta))

    assert len(pedidos) == 1, (
        "leer_pedidos() debe funcionar también cuando la ruta llega como texto. "
        "Conviértela a Path al inicio de la función."
    )


def test_etapa_1_avisa_si_el_archivo_no_existe(tmp_path):
    ruta = tmp_path / "no_existe.csv"

    with pytest.raises(FileNotFoundError) as error:
        extraer.leer_pedidos(ruta)

    assert str(error.value) == f"No se encontró el archivo: {ruta}", (
        f"El mensaje debe ser 'No se encontró el archivo: {ruta}' "
        f"y fue {str(error.value)!r}."
    )


def test_etapa_1_avisa_si_faltan_columnas(tmp_path):
    columnas = [c for c in COLUMNAS if c not in ("ciudad", "estado")]
    fila = {columna: "x" for columna in columnas}
    ruta = escribir_csv(tmp_path / "incompleto.csv", [fila], columnas)

    with pytest.raises(ValueError) as error:
        extraer.leer_pedidos(ruta)

    assert str(error.value) == "Faltan columnas en el archivo: ciudad, estado", (
        "Al archivo le faltan las columnas ciudad y estado. El mensaje debe ser "
        "'Faltan columnas en el archivo: ciudad, estado' "
        f"y fue {str(error.value)!r}."
    )


def test_etapa_1_lee_el_archivo_del_proyecto():
    pedidos = extraer.leer_pedidos(RUTA_DATOS)

    assert len(pedidos) == 63, (
        f"proyecto/datos/pedidos_crudos.csv tiene 63 pedidos y se leyeron "
        f"{len(pedidos)}. Si modificaste el archivo, recupéralo con: "
        "git restore proyecto/datos/pedidos_crudos.csv"
    )
    assert list(pedidos[0]) == COLUMNAS, (
        f"Las columnas deben ser {COLUMNAS} y fueron {list(pedidos[0])}."
    )
