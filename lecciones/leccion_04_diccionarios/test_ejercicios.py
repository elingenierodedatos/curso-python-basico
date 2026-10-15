"""Pruebas de la lección 4. No modifiques este archivo."""

import copy

import pytest

from lecciones.leccion_04_diccionarios.ejercicios import (
    agregar_total,
    ciudades_unicas,
    contar_por_ciudad,
    crear_pedido,
    obtener_ciudad,
    pedido_mas_grande,
    ventas_por_producto,
)


def pedidos_de_ejemplo():
    """Devuelve una lista nueva de pedidos en cada llamada."""
    return [
        {
            "id_pedido": 1001,
            "ciudad": "Puebla",
            "producto": "Café de olla",
            "cantidad": 2,
            "precio_unitario": 185.0,
        },
        {
            "id_pedido": 1002,
            "ciudad": "Monterrey",
            "producto": "Prensa francesa",
            "cantidad": 1,
            "precio_unitario": 420.0,
        },
        {
            "id_pedido": 1003,
            "ciudad": "Puebla",
            "producto": "Taza de barro",
            "cantidad": 4,
            "precio_unitario": 95.5,
        },
        {
            "id_pedido": 1004,
            "ciudad": "Guadalajara",
            "producto": "Café de olla",
            "cantidad": 3,
            "precio_unitario": 185.0,
        },
        {
            "id_pedido": 1005,
            "ciudad": "Puebla",
            "producto": "Filtro de tela",
            "cantidad": 3,
            "precio_unitario": 35.1,
        },
    ]


# --- Ejercicio 1: crear_pedido ---


def test_ejercicio_1_devuelve_un_diccionario():
    resultado = crear_pedido(1001, "Café de olla", 2, 185.0)

    assert isinstance(resultado, dict), (
        "crear_pedido() debe devolver un diccionario (dict). "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}."
    )


def test_ejercicio_1_tiene_las_cuatro_claves():
    esperadas = ["cantidad", "id_pedido", "precio_unitario", "producto"]

    resultado = crear_pedido(1001, "Café de olla", 2, 185.0)

    assert sorted(resultado) == esperadas, (
        f"Se esperaban las claves {esperadas} y se obtuvieron {sorted(resultado)!r}. "
        "Las claves son textos y se llaman igual que los parámetros de la función."
    )


@pytest.mark.parametrize(
    ("id_pedido", "producto", "cantidad", "precio_unitario"),
    [
        (1001, "Café de olla", 2, 185.0),
        (1002, "Prensa francesa", 1, 420.0),
        (1003, "Taza de barro", 12, 95.5),
    ],
)
def test_ejercicio_1_guarda_cada_valor_en_su_clave(
    id_pedido, producto, cantidad, precio_unitario
):
    esperado = {
        "id_pedido": id_pedido,
        "producto": producto,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
    }

    resultado = crear_pedido(id_pedido, producto, cantidad, precio_unitario)

    assert resultado == esperado, (
        f"Con id_pedido={id_pedido}, producto={producto!r}, cantidad={cantidad} y "
        f"precio_unitario={precio_unitario} se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. Cada valor viene de un parámetro, no de un dato fijo."
    )


# --- Ejercicio 2: obtener_ciudad ---


@pytest.mark.parametrize("ciudad", ["Puebla", "Ciudad de México", "Mérida"])
def test_ejercicio_2_devuelve_la_ciudad_cuando_existe(ciudad):
    pedido = {"id_pedido": 1001, "ciudad": ciudad, "cantidad": 2}

    resultado = obtener_ciudad(pedido)

    assert resultado == ciudad, (
        f"Con pedido={pedido!r} se esperaba {ciudad!r} y se obtuvo {resultado!r}. "
        'Devuelve el valor guardado en la clave "ciudad".'
    )


def test_ejercicio_2_devuelve_sin_ciudad_cuando_falta_la_clave():
    pedido = {"id_pedido": 1002, "cantidad": 1}

    resultado = obtener_ciudad(pedido)

    assert resultado == "sin ciudad", (
        f"Con pedido={pedido!r}, que no tiene la clave 'ciudad', se esperaba "
        f"'sin ciudad' y se obtuvo {resultado!r}. Hay una forma de leer una clave "
        "que acepta un valor por defecto."
    )


def test_ejercicio_2_no_modifica_el_pedido():
    pedido = {"id_pedido": 1002, "cantidad": 1}

    obtener_ciudad(pedido)

    assert pedido == {"id_pedido": 1002, "cantidad": 1}, (
        "obtener_ciudad() solo debe leer. Se le pasó un pedido sin la clave "
        f"'ciudad' y después de llamarla el pedido quedó así: {pedido!r}."
    )


# --- Ejercicio 3: agregar_total ---


@pytest.mark.parametrize(
    ("cantidad", "precio_unitario", "esperado"),
    [
        (2, 185.0, 370.0),
        (4, 95.5, 382.0),
        (3, 35.1, 105.3),
        (0, 420.0, 0.0),
    ],
)
def test_ejercicio_3_calcula_el_total_redondeado(cantidad, precio_unitario, esperado):
    pedido = {
        "id_pedido": 1001,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
    }

    resultado = agregar_total(pedido)

    assert resultado["total"] == esperado, (
        f"Con cantidad={cantidad} y precio_unitario={precio_unitario} se esperaba "
        f"total={esperado} y se obtuvo {resultado['total']!r}. Multiplica y "
        "redondea a dos decimales."
    )


def test_ejercicio_3_conserva_las_demas_claves():
    pedido = {
        "id_pedido": 1003,
        "ciudad": "Puebla",
        "cantidad": 4,
        "precio_unitario": 95.5,
    }
    esperado = {
        "id_pedido": 1003,
        "ciudad": "Puebla",
        "cantidad": 4,
        "precio_unitario": 95.5,
        "total": 382.0,
    }

    resultado = agregar_total(pedido)

    assert resultado == esperado, (
        f"Se esperaba {esperado!r} y se obtuvo {resultado!r}. El resultado lleva "
        "todas las claves del pedido recibido y, además, la clave 'total'."
    )


def test_ejercicio_3_no_modifica_el_pedido_original():
    pedido = {"id_pedido": 1001, "cantidad": 2, "precio_unitario": 185.0}

    resultado = agregar_total(pedido)

    assert "total" in resultado and "total" not in pedido, (
        "El resultado debe tener la clave 'total' y el pedido original no. "
        f"Resultado: {resultado!r}. Original después de la llamada: {pedido!r}. "
        "Trabaja sobre una copia del pedido, no sobre el que recibes."
    )


# --- Ejercicio 4: contar_por_ciudad ---


def test_ejercicio_4_cuenta_los_pedidos_de_cada_ciudad():
    pedidos = pedidos_de_ejemplo()
    copia = copy.deepcopy(pedidos)
    esperado = {"Puebla": 3, "Monterrey": 1, "Guadalajara": 1}

    resultado = contar_por_ciudad(pedidos)

    assert resultado == esperado, (
        "Con cinco pedidos (tres de Puebla, uno de Monterrey y uno de Guadalajara) "
        f"se esperaba {esperado!r} y se obtuvo {resultado!r}. Cada pedido suma 1 "
        "a la cuenta de su ciudad."
    )
    assert pedidos == copia, (
        "La función no debe modificar la lista ni los diccionarios que recibe."
    )


def test_ejercicio_4_cuenta_una_ciudad_que_se_repite():
    pedidos = [{"ciudad": "Tijuana"}, {"ciudad": "Tijuana"}, {"ciudad": "Tijuana"}]

    resultado = contar_por_ciudad(pedidos)

    assert resultado == {"Tijuana": 3}, (
        f"Con tres pedidos de Tijuana se esperaba {{'Tijuana': 3}} y se obtuvo "
        f"{resultado!r}. La primera vez que aparece una ciudad su cuenta parte de 0."
    )


def test_ejercicio_4_devuelve_un_diccionario_vacio_si_no_hay_pedidos():
    resultado = contar_por_ciudad([])

    assert resultado == {}, (
        f"Con una lista vacía se esperaba {{}} y se obtuvo {resultado!r}. "
        "Si no hay pedidos, no hay nada que contar."
    )


# --- Ejercicio 5: ventas_por_producto ---


def test_ejercicio_5_suma_el_importe_de_cada_producto():
    pedidos = pedidos_de_ejemplo()
    copia = copy.deepcopy(pedidos)
    esperado = {
        "Café de olla": 925.0,
        "Prensa francesa": 420.0,
        "Taza de barro": 382.0,
        "Filtro de tela": 105.3,
    }

    resultado = ventas_por_producto(pedidos)

    assert resultado == esperado, (
        f"Con los cinco pedidos de ejemplo se esperaba {esperado!r} y se obtuvo "
        f"{resultado!r}. El importe de cada pedido es cantidad por precio "
        "unitario, y se acumula en la clave de su producto."
    )
    assert pedidos == copia, (
        "La función no debe modificar la lista ni los diccionarios que recibe."
    )


def test_ejercicio_5_redondea_cada_suma_a_dos_decimales():
    pedidos = [
        {"producto": "Filtro de tela", "cantidad": 1, "precio_unitario": 35.1},
        {"producto": "Filtro de tela", "cantidad": 2, "precio_unitario": 35.1},
    ]

    resultado = ventas_por_producto(pedidos)

    assert resultado == {"Filtro de tela": 105.3}, (
        "Con dos pedidos de Filtro de tela (1 y 2 piezas a 35.1) se esperaba "
        f"{{'Filtro de tela': 105.3}} y se obtuvo {resultado!r}. Si ves muchos "
        "decimales, falta redondear la suma."
    )


def test_ejercicio_5_devuelve_un_diccionario_vacio_si_no_hay_pedidos():
    resultado = ventas_por_producto([])

    assert resultado == {}, (
        f"Con una lista vacía se esperaba {{}} y se obtuvo {resultado!r}."
    )


# --- Ejercicio 6: ciudades_unicas ---


def test_ejercicio_6_devuelve_una_lista():
    pedidos = pedidos_de_ejemplo()
    copia = copy.deepcopy(pedidos)

    resultado = ciudades_unicas(pedidos)

    assert isinstance(resultado, list), (
        "ciudades_unicas() debe devolver una lista (list). "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}."
    )
    assert pedidos == copia, (
        "La función no debe modificar la lista ni los diccionarios que recibe."
    )


@pytest.mark.parametrize(
    ("ciudades", "esperado"),
    [
        (["Puebla", "Monterrey", "Puebla"], ["Monterrey", "Puebla"]),
        (["Tijuana", "Puebla", "Guadalajara"], ["Guadalajara", "Puebla", "Tijuana"]),
        (["Tijuana", "Tijuana", "Tijuana"], ["Tijuana"]),
        (
            ["Puebla", "Ciudad de México", "Tijuana", "Puebla", "Ciudad de México"],
            ["Ciudad de México", "Puebla", "Tijuana"],
        ),
    ],
)
def test_ejercicio_6_quita_repetidas_y_ordena(ciudades, esperado):
    pedidos = []
    for ciudad in ciudades:
        pedidos.append({"id_pedido": 1001, "ciudad": ciudad})

    resultado = ciudades_unicas(pedidos)

    assert resultado == esperado, (
        f"Con pedidos de las ciudades {ciudades!r} se esperaba {esperado!r} y se "
        f"obtuvo {resultado!r}. Cada ciudad aparece una sola vez y la lista va "
        "ordenada."
    )


def test_ejercicio_6_devuelve_una_lista_vacia_si_no_hay_pedidos():
    resultado = ciudades_unicas([])

    assert resultado == [], (
        f"Con una lista vacía se esperaba [] y se obtuvo {resultado!r}. "
        "Recuerda que el resultado es una lista, no un conjunto."
    )


# --- Ejercicio 7: pedido_mas_grande ---


def test_ejercicio_7_devuelve_el_pedido_de_mayor_importe():
    pedidos = pedidos_de_ejemplo()
    copia = copy.deepcopy(pedidos)

    resultado = pedido_mas_grande(pedidos)

    assert resultado == pedidos[3], (
        f"Con los cinco pedidos de ejemplo se esperaba el pedido 1004 "
        f"(3 piezas a 185.0, importe 555.0) y se obtuvo {resultado!r}. "
        "Se compara cantidad por precio unitario."
    )
    assert pedidos == copia, (
        "La función no debe modificar la lista ni los diccionarios que recibe."
    )


def test_ejercicio_7_compara_el_importe_y_no_solo_la_cantidad():
    pedidos = [
        {"id_pedido": 1001, "cantidad": 10, "precio_unitario": 35.0},
        {"id_pedido": 1002, "cantidad": 1, "precio_unitario": 420.0},
    ]

    resultado = pedido_mas_grande(pedidos)

    assert resultado == pedidos[1], (
        "Con un pedido de 10 piezas a 35.0 (importe 350.0) y otro de 1 pieza a "
        f"420.0 se esperaba el pedido 1002 y se obtuvo {resultado!r}. El más "
        "grande es el de mayor importe, no el de más piezas."
    )


@pytest.mark.parametrize(("cantidad", "precio_unitario"), [(1, 35.1), (0, 420.0)])
def test_ejercicio_7_devuelve_el_unico_pedido_de_la_lista(cantidad, precio_unitario):
    pedido = {
        "id_pedido": 1001,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
    }

    resultado = pedido_mas_grande([pedido])

    assert resultado == pedido, (
        f"Con una lista de un solo pedido, {pedido!r}, se esperaba ese mismo pedido "
        f"y se obtuvo {resultado!r}. Si la lista no está vacía siempre hay un pedido "
        "mayor, aunque su importe sea 0."
    )


def test_ejercicio_7_en_un_empate_devuelve_el_primero():
    pedidos = [
        {"id_pedido": 1001, "cantidad": 1, "precio_unitario": 95.5},
        {"id_pedido": 1002, "cantidad": 2, "precio_unitario": 185.0},
        {"id_pedido": 1003, "cantidad": 1, "precio_unitario": 370.0},
    ]

    resultado = pedido_mas_grande(pedidos)

    assert resultado == pedidos[1], (
        "Los pedidos 1002 y 1003 tienen el mismo importe (370.0). Se esperaba el "
        f"primero de ellos, el 1002, y se obtuvo {resultado!r}. Revisa si tu "
        "comparación reemplaza al mayor cuando el importe es igual."
    )


def test_ejercicio_7_un_empate_por_decimales_tambien_devuelve_el_primero():
    pedidos = [
        {"id_pedido": 1001, "cantidad": 1, "precio_unitario": 0.3},
        {"id_pedido": 1002, "cantidad": 3, "precio_unitario": 0.1},
    ]

    resultado = pedido_mas_grande(pedidos)

    assert resultado == pedidos[0], (
        "Los pedidos 1001 (1 × 0.3) y 1002 (3 × 0.1) valen lo mismo: 0.3. Se "
        f"esperaba el primero, el 1001, y se obtuvo {resultado!r}. Sin redondear, "
        "3 * 0.1 da 0.30000000000000004 y parece mayor. Redondea cada importe a "
        "dos decimales antes de comparar, como en los ejercicios anteriores."
    )


def test_ejercicio_7_devuelve_none_si_no_hay_pedidos():
    resultado = pedido_mas_grande([])

    assert resultado is None, (
        f"Con una lista vacía se esperaba None y se obtuvo {resultado!r}."
    )
