"""Lección 7: un archivo de pruebas completo, ya resuelto.

Como su nombre no empieza con `test_`, pytest no lo descubre solo. Para
correrlo hay que nombrarlo:

    pytest lecciones/leccion_07_pruebas/ejemplos_de_pruebas.py -v

En un proyecto real, las funciones vivirían en su propio módulo y aquí solo
estarían las pruebas. Están juntas para que puedas leer todo de corrido.
"""

import json

import pytest

# --- Las funciones que se prueban ---


def calcular_total(cantidad, precio_unitario):
    """Multiplica cantidad por precio unitario y redondea a dos decimales."""
    if cantidad < 0:
        raise ValueError(f"La cantidad no puede ser negativa: {cantidad}")
    return round(cantidad * precio_unitario, 2)


def sumar_entregados(pedidos):
    """Suma el importe de los pedidos cuyo estado es "entregado"."""
    suma = 0.0
    for pedido in pedidos:
        if pedido["estado"] == "entregado":
            suma = suma + pedido["cantidad"] * pedido["precio_unitario"]
    return round(suma, 2)


def guardar_resumen(ruta, resumen):
    """Escribe el diccionario `resumen` como JSON en la ruta indicada."""
    texto = json.dumps(resumen, ensure_ascii=False, indent=2)
    ruta.write_text(texto, encoding="utf-8")


# --- Una prueba simple: preparar, actuar, comprobar ---


def test_calcular_total_multiplica_cantidad_por_precio():
    # Preparar
    cantidad = 2
    precio_unitario = 50.0

    # Actuar
    total = calcular_total(cantidad, precio_unitario)

    # Comprobar
    assert total == 100.0


# --- Un error esperado ---


def test_calcular_total_rechaza_cantidad_negativa():
    with pytest.raises(ValueError, match="no puede ser negativa"):
        calcular_total(-1, 50.0)


# --- Muchos casos, una sola lógica ---


@pytest.mark.parametrize(
    ("cantidad", "precio_unitario", "esperado"),
    [
        (3, 19.99, 59.97),
        (3, 0.1, 0.3),
        (0, 99.9, 0.0),
    ],
    ids=["caso_normal", "redondeo", "cantidad_cero"],
)
def test_calcular_total_redondea_a_dos_decimales(cantidad, precio_unitario, esperado):
    total = calcular_total(cantidad, precio_unitario)

    assert total == esperado


# --- Una fixture propia: datos de ejemplo para varias pruebas ---


@pytest.fixture
def pedidos_de_ejemplo():
    """Tres pedidos pequeños: dos entregados y uno cancelado."""
    return [
        {"cantidad": 2, "precio_unitario": 45.5, "estado": "entregado"},
        {"cantidad": 1, "precio_unitario": 320.0, "estado": "cancelado"},
        {"cantidad": 3, "precio_unitario": 60.0, "estado": "entregado"},
    ]


def test_sumar_entregados_ignora_los_cancelados(pedidos_de_ejemplo):
    suma = sumar_entregados(pedidos_de_ejemplo)

    assert suma == 271.0


def test_sumar_entregados_sin_entregados_devuelve_cero(pedidos_de_ejemplo):
    # Esta prueba modifica su lista. No afecta a la prueba anterior: cada
    # prueba recibe una lista nueva, recién creada por la fixture.
    for pedido in pedidos_de_ejemplo:
        pedido["estado"] = "cancelado"

    suma = sumar_entregados(pedidos_de_ejemplo)

    assert suma == 0.0


def test_sumar_entregados_con_lista_vacia_devuelve_cero():
    suma = sumar_entregados([])

    assert suma == 0.0


# --- tmp_path: una fixture incorporada para probar con archivos ---


def test_guardar_resumen_escribe_un_json_que_se_puede_leer(tmp_path):
    ruta = tmp_path / "resumen.json"
    resumen = {"ciudad": "Mérida", "pedidos": 2}

    guardar_resumen(ruta, resumen)

    leido = json.loads(ruta.read_text(encoding="utf-8"))
    assert leido == resumen
