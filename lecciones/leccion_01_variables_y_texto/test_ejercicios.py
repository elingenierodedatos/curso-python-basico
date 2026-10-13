"""Pruebas de la lección 1. No modifiques este archivo."""

import pytest

from lecciones.leccion_01_variables_y_texto.ejercicios import (
    aplicar_descuento,
    calcular_total,
    formatear_importe,
    limpiar_texto,
    nombre_completo,
    precio_a_numero,
)

# --- Ejercicio 1: nombre_completo ---


def test_ejercicio_1_une_nombre_y_apellido_con_un_espacio():
    resultado = nombre_completo("Ana", "López")

    assert resultado == "Ana López", (
        f"Se esperaba 'Ana López' y se obtuvo {resultado!r}. "
        "Entre el nombre y el apellido va exactamente un espacio."
    )


@pytest.mark.parametrize(
    ("nombre", "apellido", "esperado"),
    [
        ("ana", "lópez", "Ana López"),
        ("JOSÉ", "PÉREZ", "José Pérez"),
        ("maría", "DE LA O", "María De La O"),
    ],
)
def test_ejercicio_1_pone_mayuscula_inicial(nombre, apellido, esperado):
    resultado = nombre_completo(nombre, apellido)

    assert resultado == esperado, (
        f"Con nombre={nombre!r} y apellido={apellido!r} se esperaba {esperado!r} "
        f"y se obtuvo {resultado!r}. Busca el método de texto que deja "
        "mayúscula solo al inicio de cada palabra."
    )


# --- Ejercicio 2: limpiar_texto ---


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("  Monterrey ", "monterrey"),
        ("GUADALAJARA", "guadalajara"),
        ("\tciudad de méxico\n", "ciudad de méxico"),
        ("puebla", "puebla"),
    ],
)
def test_ejercicio_2_quita_espacios_y_pasa_a_minusculas(texto, esperado):
    resultado = limpiar_texto(texto)

    assert resultado == esperado, (
        f"Con texto={texto!r} se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "Hay que quitar los espacios de los extremos y pasar a minúsculas."
    )


def test_ejercicio_2_conserva_los_espacios_de_en_medio():
    resultado = limpiar_texto("  San Luis Potosí  ")

    assert resultado == "san luis potosí", (
        f"Se esperaba 'san luis potosí' y se obtuvo {resultado!r}. "
        "Solo se quitan los espacios de los extremos, no los que separan palabras."
    )


# --- Ejercicio 3: precio_a_numero ---


def test_ejercicio_3_devuelve_un_numero_con_decimales():
    resultado = precio_a_numero("45")

    assert isinstance(resultado, float), (
        "precio_a_numero() debe devolver un número con decimales (float). "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}."
    )


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("45.5", 45.5),
        ("$45.50", 45.5),
        ("$1,250.50", 1250.5),
        (" $1,250.50 ", 1250.5),
        ("$1,000,000", 1000000.0),
    ],
)
def test_ejercicio_3_convierte_precios_con_simbolos(texto, esperado):
    resultado = precio_a_numero(texto)

    assert resultado == esperado, (
        f"Con texto={texto!r} se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "Antes de convertir, quita los espacios, el símbolo $ y las comas."
    )


# --- Ejercicio 4: calcular_total ---


@pytest.mark.parametrize(
    ("cantidad", "precio_unitario", "esperado"),
    [
        (2, 50.0, 100.0),
        (3, 19.99, 59.97),
        (3, 0.1, 0.3),
        (0, 99.9, 0.0),
    ],
)
def test_ejercicio_4_multiplica_y_redondea(cantidad, precio_unitario, esperado):
    resultado = calcular_total(cantidad, precio_unitario)

    assert resultado == esperado, (
        f"Con cantidad={cantidad} y precio_unitario={precio_unitario} se esperaba "
        f"{esperado} y se obtuvo {resultado!r}. Multiplica y después redondea "
        "a dos decimales."
    )


# --- Ejercicio 5: aplicar_descuento ---


@pytest.mark.parametrize(
    ("total", "porcentaje", "esperado"),
    [
        (200, 15, 170.0),
        (59.97, 10, 53.97),
        (100, 0, 100.0),
        (80, 100, 0.0),
    ],
)
def test_ejercicio_5_resta_el_porcentaje(total, porcentaje, esperado):
    resultado = aplicar_descuento(total, porcentaje)

    assert resultado == esperado, (
        f"Con total={total} y porcentaje={porcentaje} se esperaba {esperado} "
        f"y se obtuvo {resultado!r}. El descuento es total * porcentaje / 100, "
        "y el resultado se redondea a dos decimales."
    )


# --- Ejercicio 6: formatear_importe ---


def test_ejercicio_6_devuelve_un_texto():
    resultado = formatear_importe(10)

    assert isinstance(resultado, str), (
        "formatear_importe() debe devolver un texto (str). "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}."
    )


@pytest.mark.parametrize(
    ("importe", "esperado"),
    [
        (1250.5, "$1,250.50 MXN"),
        (45, "$45.00 MXN"),
        (0, "$0.00 MXN"),
        (1000000, "$1,000,000.00 MXN"),
        (19.999, "$20.00 MXN"),
    ],
)
def test_ejercicio_6_formatea_con_miles_decimales_y_moneda(importe, esperado):
    resultado = formatear_importe(importe)

    assert resultado == esperado, (
        f"Con importe={importe} se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "Revisa el símbolo $, las comas de miles, los dos decimales "
        "y el espacio antes de MXN."
    )
