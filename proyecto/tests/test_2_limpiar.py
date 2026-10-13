"""Pruebas de la etapa 2: limpiar. No modifiques este archivo."""

import pytest
from conftest import crear_crudo
from flujo_ventas import limpiar

# --- es_faltante ---


@pytest.mark.parametrize(
    "valor", [None, "", "   ", "N/D", " n/d ", "NA", "null", "Null"]
)
def test_etapa_2_es_faltante_reconoce_los_faltantes(valor):
    resultado = limpiar.es_faltante(valor)

    assert resultado is True, (
        f"Con valor={valor!r} se esperaba True y se obtuvo {resultado!r}."
    )


@pytest.mark.parametrize("valor", ["Puebla", "0", "nada", "n/a"])
def test_etapa_2_es_faltante_no_marca_valores_reales(valor):
    resultado = limpiar.es_faltante(valor)

    assert resultado is False, (
        f"Con valor={valor!r} se esperaba False y se obtuvo {resultado!r}. "
        "Solo cuentan los textos de la lista FALTANTES."
    )


# --- limpiar_fecha ---


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("2025-03-07", "2025-03-07"),
        (" 2025-03-07 ", "2025-03-07"),
        ("07/03/2025", "2025-03-07"),
        ("7/3/2025", "2025-03-07"),
        ("28/12/2024", "2024-12-28"),
        ("1/10/2025", "2025-10-01"),
    ],
)
def test_etapa_2_limpiar_fecha_devuelve_formato_iso(texto, esperado):
    resultado = limpiar.limpiar_fecha(texto)

    assert resultado == esperado, (
        f"Con texto={texto!r} se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "El formato con diagonales es día/mes/año, y día y mes llevan dos dígitos "
        "en el resultado."
    )


@pytest.mark.parametrize(
    "texto", ["", "N/D", "ayer", "2025/03", "7-3", "a/b/c", "40/13/2025"]
)
def test_etapa_2_limpiar_fecha_rechaza_lo_que_no_es_fecha(texto):
    with pytest.raises(ValueError) as error:
        limpiar.limpiar_fecha(texto)

    assert str(error.value) == "fecha inválida", (
        f"Con texto={texto!r} el mensaje del error debe ser 'fecha inválida' "
        f"y fue {str(error.value)!r}."
    )


# --- limpiar_ciudad ---


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("Puebla", "Puebla"),
        ("  CDMX ", "Ciudad de México"),
        ("ciudad de mexico", "Ciudad de México"),
        ("CIUDAD DE MÉXICO", "Ciudad de México"),
        ("gdl", "Guadalajara"),
        (" MTY", "Monterrey"),
        ("merida", "Mérida"),
        ("san luis potosí", "San Luis Potosí"),
        (" QUERÉTARO ", "Querétaro"),
    ],
)
def test_etapa_2_limpiar_ciudad_devuelve_el_nombre_oficial(texto, esperado):
    resultado = limpiar.limpiar_ciudad(texto)

    assert resultado == esperado, (
        f"Con texto={texto!r} se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "Busca primero en CIUDADES; si no está, usa el texto limpio con "
        "mayúscula inicial en cada palabra."
    )


@pytest.mark.parametrize("texto", ["", "  ", "N/D", "na"])
def test_etapa_2_limpiar_ciudad_rechaza_faltantes(texto):
    with pytest.raises(ValueError) as error:
        limpiar.limpiar_ciudad(texto)

    assert str(error.value) == "ciudad faltante", (
        f"Con texto={texto!r} el mensaje del error debe ser 'ciudad faltante' "
        f"y fue {str(error.value)!r}."
    )


# --- limpiar_pedido ---


def test_etapa_2_limpiar_pedido_convierte_todas_las_columnas():
    crudo = crear_crudo(
        id_pedido="1001",
        fecha="7/3/2025",
        cliente="  ana RUIZ ",
        ciudad="cdmx",
        producto=" CAFÉ DE OLLA ",
        cantidad="2",
        precio_unitario=" $1,250.50 ",
        estado=" Entregada ",
    )

    resultado = limpiar.limpiar_pedido(crudo)

    esperado = {
        "id_pedido": 1001,
        "fecha": "2025-03-07",
        "cliente": "Ana Ruiz",
        "ciudad": "Ciudad de México",
        "producto": "Café de olla",
        "cantidad": 2,
        "precio_unitario": 1250.5,
        "estado": "entregado",
        "total": 2501.0,
    }
    for clave, valor in esperado.items():
        assert clave in resultado, f"Al pedido limpio le falta la clave {clave!r}."
        assert resultado[clave] == valor, (
            f"En la clave {clave!r} se esperaba {valor!r} y se obtuvo "
            f"{resultado[clave]!r}. Revisa la regla de esa columna en el docstring."
        )
        assert type(resultado[clave]) is type(valor), (
            f"La clave {clave!r} debe ser de tipo {type(valor).__name__} y es "
            f"{type(resultado[clave]).__name__}."
        )
    assert list(resultado) == list(esperado), (
        f"Las claves deben ser {list(esperado)}, en ese orden, y fueron "
        f"{list(resultado)}."
    )


def test_etapa_2_limpiar_pedido_no_modifica_el_original():
    crudo = crear_crudo(ciudad=" cdmx ")
    copia = dict(crudo)

    limpiar.limpiar_pedido(crudo)

    assert crudo == copia, (
        "limpiar_pedido() cambió el diccionario que recibió. Construye uno nuevo."
    )


@pytest.mark.parametrize("cliente", ["", "N/D", "  "])
def test_etapa_2_limpiar_pedido_pone_sin_nombre_al_cliente_faltante(cliente):
    resultado = limpiar.limpiar_pedido(crear_crudo(cliente=cliente))

    assert resultado["cliente"] == "Sin nombre", (
        f"Con cliente={cliente!r} se esperaba 'Sin nombre' y se obtuvo "
        f"{resultado['cliente']!r}. Un cliente faltante no es motivo de rechazo."
    )


@pytest.mark.parametrize(
    ("estado", "esperado"),
    [
        ("entregado", "entregado"),
        (" ENVIADO ", "enviado"),
        ("en camino", "enviado"),
        ("Cancelada", "cancelado"),
        ("devuelto", "desconocido"),
        ("", "desconocido"),
    ],
)
def test_etapa_2_limpiar_pedido_normaliza_el_estado(estado, esperado):
    resultado = limpiar.limpiar_pedido(crear_crudo(estado=estado))

    assert resultado["estado"] == esperado, (
        f"Con estado={estado!r} se esperaba {esperado!r} y se obtuvo "
        f"{resultado['estado']!r}."
    )


def test_etapa_2_limpiar_pedido_redondea_el_total():
    resultado = limpiar.limpiar_pedido(
        crear_crudo(cantidad="3", precio_unitario="89.9")
    )

    assert resultado["total"] == 269.7, (
        f"3 por 89.9 debe dar 269.7 y se obtuvo {resultado['total']!r}. "
        "Redondea el total a 2 decimales."
    )


@pytest.mark.parametrize(
    ("cambios", "motivo"),
    [
        ({"id_pedido": "S/N"}, "id_pedido inválido"),
        ({"id_pedido": ""}, "id_pedido inválido"),
        ({"fecha": "ayer"}, "fecha inválida"),
        ({"ciudad": "N/D"}, "ciudad faltante"),
        ({"producto": "NA"}, "producto faltante"),
        ({"cantidad": "dos"}, "cantidad inválida"),
        ({"cantidad": "0"}, "cantidad inválida"),
        ({"cantidad": "-1"}, "cantidad inválida"),
        ({"cantidad": "2.5"}, "cantidad inválida"),
        ({"precio_unitario": "gratis"}, "precio inválido"),
        ({"precio_unitario": "$0.00"}, "precio inválido"),
        ({"precio_unitario": ""}, "precio inválido"),
    ],
)
def test_etapa_2_limpiar_pedido_rechaza_con_el_motivo_correcto(cambios, motivo):
    crudo = crear_crudo(**cambios)

    with pytest.raises(ValueError) as error:
        limpiar.limpiar_pedido(crudo)

    assert str(error.value) == motivo, (
        f"Con {cambios!r} el motivo debe ser {motivo!r} y fue {str(error.value)!r}."
    )


def test_etapa_2_limpiar_pedido_revisa_los_motivos_en_orden():
    crudo = crear_crudo(fecha="ayer", ciudad="", cantidad="0")

    with pytest.raises(ValueError) as error:
        limpiar.limpiar_pedido(crudo)

    assert str(error.value) == "fecha inválida", (
        "Si un pedido tiene varios problemas, se reporta el primero según el orden "
        f"del docstring. Se esperaba 'fecha inválida' y fue {str(error.value)!r}."
    )


# --- limpiar_pedidos ---


def test_etapa_2_limpiar_pedidos_con_lista_vacia():
    resultado = limpiar.limpiar_pedidos([])

    assert resultado == ([], []), (
        f"Con una lista vacía se esperaba ([], []) y se obtuvo {resultado!r}."
    )


def test_etapa_2_limpiar_pedidos_separa_limpios_y_rechazados():
    crudos = [
        crear_crudo(id_pedido="1"),
        crear_crudo(id_pedido="2", ciudad="N/D"),
        crear_crudo(id_pedido="3"),
        crear_crudo(id_pedido="4", cantidad="cero"),
    ]

    limpios, rechazados = limpiar.limpiar_pedidos(crudos)

    ids = [pedido["id_pedido"] for pedido in limpios]
    assert ids == [1, 3], (
        f"Los pedidos limpios deben ser el 1 y el 3, en ese orden, y fueron {ids}."
    )
    assert len(rechazados) == 2, (
        f"Deben rechazarse 2 pedidos y se rechazaron {len(rechazados)}."
    )
    assert rechazados[0] == {
        "fila": 2,
        "motivo": "ciudad faltante",
        "datos": crudos[1],
    }, (
        "El primer rechazado debe ser la fila 2, con motivo 'ciudad faltante' y los "
        f"datos crudos sin cambios. Se obtuvo {rechazados[0]!r}."
    )
    assert rechazados[1]["fila"] == 4, (
        f"El segundo rechazado es la fila 4 y se reportó {rechazados[1]['fila']!r}. "
        "Las filas se cuentan desde 1."
    )
    assert rechazados[1]["motivo"] == "cantidad inválida", (
        f"Motivo esperado 'cantidad inválida', obtenido {rechazados[1]['motivo']!r}."
    )


def test_etapa_2_limpiar_pedidos_rechaza_los_duplicados_y_conserva_el_primero():
    crudos = [
        crear_crudo(id_pedido="7", ciudad="Puebla"),
        crear_crudo(id_pedido="8"),
        crear_crudo(id_pedido="7", ciudad="Tijuana"),
    ]

    limpios, rechazados = limpiar.limpiar_pedidos(crudos)

    assert len(limpios) == 2, (
        f"Deben quedar 2 pedidos limpios y quedaron {len(limpios)}. "
        "El id_pedido 7 aparece dos veces."
    )
    assert limpios[0]["ciudad"] == "Puebla", (
        "Se conserva el primer pedido con ese id (el de Puebla). "
        f"Se conservó el de {limpios[0]['ciudad']!r}."
    )
    assert rechazados == [
        {"fila": 3, "motivo": "id_pedido duplicado", "datos": crudos[2]}
    ], f"El duplicado de la fila 3 debe rechazarse. Se obtuvo {rechazados!r}."


def test_etapa_2_limpiar_pedidos_un_rechazado_no_cuenta_como_visto():
    crudos = [
        crear_crudo(id_pedido="9", cantidad="0"),
        crear_crudo(id_pedido="9"),
    ]

    limpios, rechazados = limpiar.limpiar_pedidos(crudos)

    assert len(limpios) == 1, (
        "Si el primer pedido con un id fue rechazado, el siguiente con ese id sí "
        f"es válido. Se esperaba 1 pedido limpio y hubo {len(limpios)}."
    )
    assert rechazados[0]["motivo"] == "cantidad inválida", (
        f"Motivo esperado 'cantidad inválida', obtenido {rechazados[0]['motivo']!r}."
    )
