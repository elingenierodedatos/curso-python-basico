"""Pruebas de la lección 3. No modifiques este archivo."""

import pytest

from lecciones.leccion_03_condicionales.ejercicios import (
    clasificar_importe,
    contar_faltantes,
    es_cantidad_valida,
    es_faltante,
    filtrar_mayores,
    normalizar_estado,
    posicion_del_primer_faltante,
)

# --- Ejercicio 1: es_cantidad_valida ---


@pytest.mark.parametrize("cantidad", [1, 3, 250])
def test_ejercicio_1_acepta_enteros_mayores_que_cero(cantidad):
    resultado = es_cantidad_valida(cantidad)

    assert resultado is True, (
        f"Con cantidad={cantidad!r} se esperaba True y se obtuvo {resultado!r}. "
        "Un entero mayor que cero es una cantidad válida."
    )


@pytest.mark.parametrize("cantidad", [0, -2])
def test_ejercicio_1_rechaza_cero_y_negativos(cantidad):
    resultado = es_cantidad_valida(cantidad)

    assert resultado is False, (
        f"Con cantidad={cantidad!r} se esperaba False y se obtuvo {resultado!r}. "
        "La cantidad debe ser mayor que cero; el cero no cuenta."
    )


@pytest.mark.parametrize("cantidad", ["3", 2.5, None])
def test_ejercicio_1_rechaza_lo_que_no_es_entero(cantidad):
    resultado = es_cantidad_valida(cantidad)

    assert resultado is False, (
        f"Con cantidad={cantidad!r} se esperaba False y se obtuvo {resultado!r}. "
        "Pregunta primero si el valor es un entero y solo después compáralo "
        "con cero."
    )


@pytest.mark.parametrize("cantidad", [True, False])
def test_ejercicio_1_rechaza_booleanos(cantidad):
    resultado = es_cantidad_valida(cantidad)

    assert resultado is False, (
        f"Con cantidad={cantidad!r} se esperaba False y se obtuvo {resultado!r}. "
        "Para Python, True y False también son enteros. Revisa al final del "
        "concepto 4 cómo excluirlos."
    )


# --- Ejercicio 2: clasificar_importe ---


@pytest.mark.parametrize(
    ("importe", "esperado"),
    [
        (0, "bajo"),
        (120.5, "bajo"),
        (1250.5, "medio"),
        (8900, "alto"),
    ],
)
def test_ejercicio_2_clasifica_importes_dentro_de_cada_rango(importe, esperado):
    resultado = clasificar_importe(importe)

    assert resultado == esperado, (
        f"Con importe={importe!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Revisa el orden de tus condiciones: solo corre el primer "
        "bloque verdadero."
    )


@pytest.mark.parametrize(
    ("importe", "esperado"),
    [
        (499.99, "bajo"),
        (500, "medio"),
        (1999.99, "medio"),
        (2000, "alto"),
    ],
)
def test_ejercicio_2_clasifica_los_limites_exactos(importe, esperado):
    resultado = clasificar_importe(importe)

    assert resultado == esperado, (
        f"Con importe={importe!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Los límites 500 y 2000 pertenecen al rango de arriba: "
        "revisa si te toca usar < o <=."
    )


# --- Ejercicio 3: es_faltante ---


def test_ejercicio_3_none_es_faltante():
    resultado = es_faltante(None)

    assert resultado is True, (
        f"Con valor=None se esperaba True y se obtuvo {resultado!r}. "
        "Pregunta primero si el valor es None, antes de usar métodos de texto."
    )


@pytest.mark.parametrize(
    "valor",
    ["", "   ", "N/D", "n/d", "NA", " na ", "null", "NULL", "\tN/D\n"],
)
def test_ejercicio_3_reconoce_los_textos_de_faltante(valor):
    resultado = es_faltante(valor)

    assert resultado is True, (
        f"Con valor={valor!r} se esperaba True y se obtuvo {resultado!r}. "
        "Limpia el texto (espacios y mayúsculas) antes de buscarlo entre los "
        "faltantes."
    )


@pytest.mark.parametrize("valor", ["Puebla", "0", "Nadia", "canal", "n/a"])
def test_ejercicio_3_un_dato_real_no_es_faltante(valor):
    resultado = es_faltante(valor)

    assert resultado is False, (
        f"Con valor={valor!r} se esperaba False y se obtuvo {resultado!r}. "
        "El texto limpio debe ser exactamente uno de los faltantes, no solo "
        "parecerse a uno o contenerlo."
    )


# --- Ejercicio 4: normalizar_estado ---


@pytest.mark.parametrize(
    ("estado", "esperado"),
    [
        ("entregado", "entregado"),
        ("  ENTREGADO ", "entregado"),
        ("Enviado", "enviado"),
        ("cancelado\n", "cancelado"),
    ],
)
def test_ejercicio_4_limpia_mayusculas_y_espacios(estado, esperado):
    resultado = normalizar_estado(estado)

    assert resultado == esperado, (
        f"Con estado={estado!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Quita los espacios de los extremos y pasa a minúsculas "
        "antes de comparar."
    )


@pytest.mark.parametrize(
    ("estado", "esperado"),
    [
        ("Entregada", "entregado"),
        ("en camino", "enviado"),
        ("  EN CAMINO ", "enviado"),
        ("CANCELADA", "cancelado"),
    ],
)
def test_ejercicio_4_acepta_sinonimos(estado, esperado):
    resultado = normalizar_estado(estado)

    assert resultado == esperado, (
        f"Con estado={estado!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Cada estado tiene más de una forma de escribirse; "
        "revisa la tabla de sinónimos del README."
    )


@pytest.mark.parametrize("estado", ["devuelto", "", "pendiente de pago", "enviados"])
def test_ejercicio_4_otro_valor_es_desconocido(estado):
    resultado = normalizar_estado(estado)

    assert resultado == "desconocido", (
        f"Con estado={estado!r} se esperaba 'desconocido' y se obtuvo "
        f"{resultado!r}. Todo lo que no coincida exactamente con un estado "
        "conocido cae en el último caso."
    )


# --- Ejercicio 5: filtrar_mayores ---


@pytest.mark.parametrize(
    ("importes", "minimo", "esperado"),
    [
        ([450.0, 1200.0, 380.0, 2500.0], 1000, [1200.0, 2500.0]),
        ([2500.0, 99.0, 1200.0], 100, [2500.0, 1200.0]),
        ([450.0, 380.0], 1000, []),
        ([300, 300, 150, 300], 300, [300, 300, 300]),
        ([], 500, []),
    ],
)
def test_ejercicio_5_conserva_los_importes_que_alcanzan_el_minimo(
    importes, minimo, esperado
):
    resultado = filtrar_mayores(importes, minimo)

    assert resultado == esperado, (
        f"Con importes={importes!r} y minimo={minimo!r} se esperaba {esperado!r} "
        f"y se obtuvo {resultado!r}. Se conservan, en el mismo orden, los "
        "importes mayores o iguales al mínimo."
    )


def test_ejercicio_5_incluye_el_importe_igual_al_minimo():
    resultado = filtrar_mayores([499.99, 500, 500.01], 500)

    assert resultado == [500, 500.01], (
        "Con importes=[499.99, 500, 500.01] y minimo=500 se esperaba "
        f"[500, 500.01] y se obtuvo {resultado!r}. Un importe igual al mínimo "
        "también se conserva."
    )


def test_ejercicio_5_no_modifica_la_lista_original():
    importes = [450.0, 1200.0, 380.0]

    resultado = filtrar_mayores(importes, 400)

    assert importes == [450.0, 1200.0, 380.0], (
        "La lista recibida cambió: quedó como "
        f"{importes!r}. Crea una lista nueva y agrégale elementos; no quites "
        "nada de la original."
    )
    assert resultado is not importes, (
        "filtrar_mayores() devolvió la misma lista que recibió. "
        "Debe devolver una lista nueva."
    )


# --- Ejercicio 6: contar_faltantes ---


@pytest.mark.parametrize(
    ("valores", "esperado"),
    [
        (["Puebla", "", "N/D", "Mérida", None], 3),
        (["Puebla", "Mérida", "Tijuana"], 0),
        ([None, None, " na ", "NULL"], 4),
        ([], 0),
    ],
)
def test_ejercicio_6_cuenta_los_faltantes(valores, esperado):
    resultado = contar_faltantes(valores)

    assert resultado == esperado, (
        f"Con valores={valores!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Empieza un contador en cero y súmale uno por cada "
        "elemento que es_faltante() reconozca."
    )


def test_ejercicio_6_no_modifica_la_lista_original():
    valores = ["Puebla", "", "N/D"]

    contar_faltantes(valores)

    assert valores == ["Puebla", "", "N/D"], (
        f"La lista recibida cambió: quedó como {valores!r}. "
        "Para contar basta con recorrerla; no hace falta quitarle nada."
    )


# --- Ejercicio 7: posicion_del_primer_faltante ---


@pytest.mark.parametrize(
    ("valores", "esperado"),
    [
        (["Puebla", "Mérida", "NA", ""], 2),
        ([None, "Puebla"], 0),
        (["Puebla", "Mérida", " n/d "], 2),
        (["", "", ""], 0),
    ],
)
def test_ejercicio_7_devuelve_el_indice_del_primer_faltante(valores, esperado):
    resultado = posicion_del_primer_faltante(valores)

    assert resultado == esperado, (
        f"Con valores={valores!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Los índices empiezan en cero y el bucle debe detenerse "
        "en el primer faltante que encuentre."
    )


@pytest.mark.parametrize("valores", [["Puebla", "Mérida"], []])
def test_ejercicio_7_devuelve_menos_uno_si_no_hay_faltantes(valores):
    resultado = posicion_del_primer_faltante(valores)

    assert resultado == -1, (
        f"Con valores={valores!r} se esperaba -1 y se obtuvo {resultado!r}. "
        "Si el bucle termina sin encontrar un faltante, la respuesta es -1."
    )


def test_ejercicio_7_no_modifica_la_lista_original():
    valores = ["Puebla", "NA", "Mérida"]

    posicion_del_primer_faltante(valores)

    assert valores == ["Puebla", "NA", "Mérida"], (
        f"La lista recibida cambió: quedó como {valores!r}. "
        "Avanza con un contador de posición; no quites elementos de la lista."
    )
