"""Pruebas de la lección 2. No modifiques este archivo."""

import pytest

from lecciones.leccion_02_listas_y_bucles.ejercicios import (
    calcular_totales,
    importe_promedio,
    limpiar_ciudades,
    los_mas_altos,
    primero_y_ultimo,
    sumar_importes,
)

# --- Ejercicio 1: primero_y_ultimo ---


def test_ejercicio_1_devuelve_una_tupla():
    resultado = primero_y_ultimo([1001, 1002, 1003])

    assert isinstance(resultado, tuple), (
        "primero_y_ultimo() debe devolver una tupla. "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}. "
        "Una tupla se escribe con paréntesis o separando los valores con coma."
    )


@pytest.mark.parametrize(
    ("valores", "esperado"),
    [
        ([1001, 1002, 1003], (1001, 1003)),
        (["Puebla", "Mérida"], ("Puebla", "Mérida")),
        ([450.0, 1250.5, 89.9, 780.0, 320.0], (450.0, 320.0)),
        (["Café de olla"], ("Café de olla", "Café de olla")),
    ],
)
def test_ejercicio_1_toma_el_primer_y_el_ultimo_elemento(valores, esperado):
    resultado = primero_y_ultimo(valores)

    assert resultado == esperado, (
        f"Con valores={valores!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. La función debe servir para listas de cualquier "
        "longitud: usa el índice que cuenta desde el final."
    )


# --- Ejercicio 2: sumar_importes ---


@pytest.mark.parametrize(
    ("importes", "esperado"),
    [
        ([100, 250.5, 49.5], 400.0),
        ([45.5], 45.5),
        ([0.1, 0.1, 0.1], 0.3),
        ([19.99, 19.99, 19.99], 59.97),
        ([500, 500, 500, 500], 2000),
    ],
)
def test_ejercicio_2_suma_y_redondea(importes, esperado):
    resultado = sumar_importes(importes)

    assert resultado == esperado, (
        f"Con importes={importes!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Acumula todos los importes y redondea el total a dos "
        "decimales después del bucle, no dentro."
    )


def test_ejercicio_2_con_lista_vacia_devuelve_cero():
    resultado = sumar_importes([])

    assert resultado == 0, (
        f"Con una lista vacía se esperaba 0 y se obtuvo {resultado!r}. "
        "Revisa con qué valor empieza tu acumulador antes del bucle."
    )


# --- Ejercicio 3: limpiar_ciudades ---


@pytest.mark.parametrize(
    ("ciudades", "esperado"),
    [
        (["  puebla ", "MÉRIDA"], ["Puebla", "Mérida"]),
        (
            [" ciudad de méxico", "tijuana  ", "Monterrey"],
            ["Ciudad De México", "Tijuana", "Monterrey"],
        ),
        (
            ["puebla", " PUEBLA ", "Puebla"],
            ["Puebla", "Puebla", "Puebla"],
        ),
        ([], []),
    ],
)
def test_ejercicio_3_limpia_cada_ciudad(ciudades, esperado):
    resultado = limpiar_ciudades(ciudades)

    assert resultado == esperado, (
        f"Con ciudades={ciudades!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Cada texto va sin espacios en los extremos y con "
        "mayúscula inicial por palabra, en el mismo orden y sin quitar repetidos."
    )


def test_ejercicio_3_no_modifica_la_lista_original():
    ciudades = ["  puebla ", "MÉRIDA"]

    resultado = limpiar_ciudades(ciudades)

    assert ciudades == ["  puebla ", "MÉRIDA"], (
        "limpiar_ciudades() no debe cambiar la lista que recibe. Se le pasó "
        f"['  puebla ', 'MÉRIDA'] y después de llamarla quedó como {ciudades!r}. "
        "Guarda los textos limpios en una lista nueva."
    )
    assert resultado is not ciudades, (
        "limpiar_ciudades() devolvió la misma lista que recibió. "
        "Debe devolver una lista nueva, que empieza vacía y se llena en el bucle."
    )


# --- Ejercicio 4: calcular_totales ---


@pytest.mark.parametrize(
    ("cantidades", "precios", "esperado"),
    [
        ([2, 1], [45.5, 1250.0], [91.0, 1250.0]),
        ([2, 1, 3], [45.5, 1250.0, 19.99], [91.0, 1250.0, 59.97]),
        ([3], [0.1], [0.3]),
        ([0, 5], [320.0, 89.9], [0.0, 449.5]),
        ([], [], []),
    ],
)
def test_ejercicio_4_multiplica_posicion_por_posicion(cantidades, precios, esperado):
    resultado = calcular_totales(cantidades, precios)

    assert resultado == esperado, (
        f"Con cantidades={cantidades!r} y precios={precios!r} se esperaba "
        f"{esperado!r} y se obtuvo {resultado!r}. Cada total es la cantidad por "
        "el precio de la misma posición, redondeado a dos decimales."
    )


def test_ejercicio_4_no_modifica_las_listas_originales():
    cantidades = [2, 1, 3]
    precios = [45.5, 1250.0, 19.99]

    calcular_totales(cantidades, precios)

    assert cantidades == [2, 1, 3], (
        "calcular_totales() no debe cambiar la lista de cantidades. Se le pasó "
        f"[2, 1, 3] y después de llamarla quedó como {cantidades!r}. "
        "Guarda los totales en una lista nueva."
    )
    assert precios == [45.5, 1250.0, 19.99], (
        "calcular_totales() no debe cambiar la lista de precios. Se le pasó "
        f"[45.5, 1250.0, 19.99] y después de llamarla quedó como {precios!r}. "
        "Guarda los totales en una lista nueva."
    )


# --- Ejercicio 5: los_mas_altos ---


@pytest.mark.parametrize(
    ("importes", "n", "esperado"),
    [
        ([450.0, 1250.5, 89.9, 780.0], 2, [1250.5, 780.0]),
        ([450.0, 1250.5, 89.9, 780.0, 320.0], 3, [1250.5, 780.0, 450.0]),
        ([450.0, 1250.5, 89.9], 1, [1250.5]),
        ([500, 200, 500, 100], 2, [500, 500]),
        ([89.9, 450.0, 1250.5], 3, [1250.5, 450.0, 89.9]),
        ([89.9, 450.0], 5, [450.0, 89.9]),
        ([450.0, 1250.5, 89.9], 0, []),
    ],
)
def test_ejercicio_5_devuelve_los_n_mas_altos_de_mayor_a_menor(importes, n, esperado):
    resultado = los_mas_altos(importes, n)

    assert resultado == esperado, (
        f"Con importes={importes!r} y n={n} se esperaba {esperado!r} y se "
        f"obtuvo {resultado!r}. Ordena de mayor a menor y quédate con los "
        "primeros n elementos."
    )


def test_ejercicio_5_no_modifica_la_lista_original():
    importes = [450.0, 1250.5, 89.9, 780.0]

    los_mas_altos(importes, 2)

    assert importes == [450.0, 1250.5, 89.9, 780.0], (
        "los_mas_altos() no debe cambiar la lista que recibe. Se le pasó "
        f"[450.0, 1250.5, 89.9, 780.0] y después de llamarla quedó como "
        f"{importes!r}. Una de las dos formas de ordenar cambia la lista "
        "original y la otra devuelve una nueva."
    )


# --- Ejercicio 6: importe_promedio ---


@pytest.mark.parametrize(
    ("importes", "esperado"),
    [
        ([100, 200, 300], 200.0),
        ([10, 20.5], 15.25),
        ([100, 100, 101], 100.33),
        ([0.1, 0.1, 0.1], 0.1),
        ([45.5], 45.5),
    ],
)
def test_ejercicio_6_calcula_el_promedio_y_redondea(importes, esperado):
    resultado = importe_promedio(importes)

    assert resultado == esperado, (
        f"Con importes={importes!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. El promedio es la suma entre la cantidad de elementos, "
        "redondeado a dos decimales."
    )


def test_ejercicio_6_no_modifica_la_lista_original():
    importes = [100, 200, 300]

    importe_promedio(importes)

    assert importes == [100, 200, 300], (
        "importe_promedio() no debe cambiar la lista que recibe. Se le pasó "
        f"[100, 200, 300] y después de llamarla quedó como {importes!r}."
    )
