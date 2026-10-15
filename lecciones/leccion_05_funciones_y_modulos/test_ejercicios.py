"""Pruebas de la lección 5. No modifiques este archivo."""

import inspect

import pytest

from lecciones.leccion_05_funciones_y_modulos import limpieza
from lecciones.leccion_05_funciones_y_modulos.ejercicios import (
    es_pedido_valido,
    limpiar_pedido,
    separar_validos,
)

CLAVES_DE_PEDIDO = [
    "id_pedido",
    "ciudad",
    "producto",
    "cantidad",
    "precio_unitario",
    "estado",
]


def obtener_funcion(nombre):
    """Busca en limpieza.py la función pedida; si no existe, la prueba falla."""
    funcion = getattr(limpieza, nombre, None)
    if funcion is None:
        pytest.fail(
            f"Todavía no existe la función {nombre}() en limpieza.py. "
            "Escríbela completa: la línea def con ese nombre exacto, "
            "su docstring, el cuerpo y el return."
        )
    return funcion


def comprobar_docstring(nombre):
    funcion = obtener_funcion(nombre)

    docstring = funcion.__doc__

    assert docstring is not None and docstring.strip() != "", (
        f"La función {nombre}() existe, pero no tiene docstring. "
        "Escribe, justo debajo de la línea def y entre comillas triples, "
        "una frase que diga qué hace."
    )


def crear_pedido_crudo():
    return {
        "id_pedido": " 1001 ",
        "ciudad": "  GUADALAJARA ",
        "producto": " prensa francesa",
        "cantidad": "2",
        "precio_unitario": " $1,250.50 ",
        "estado": " Entregado ",
    }


def crear_pedido_limpio():
    return {
        "id_pedido": 1001,
        "ciudad": "Guadalajara",
        "producto": "Prensa Francesa",
        "cantidad": 2,
        "precio_unitario": 1250.5,
        "estado": "entregado",
    }


def crear_pedido_con(clave, valor):
    pedido = crear_pedido_limpio()
    pedido[clave] = valor
    return pedido


# --- Ejercicio 1: limpiar_texto ---


def test_ejercicio_1_la_funcion_existe_y_tiene_docstring():
    comprobar_docstring("limpiar_texto")


def test_ejercicio_1_devuelve_el_resultado_con_return():
    limpiar_texto = obtener_funcion("limpiar_texto")

    resultado = limpiar_texto(" Puebla ")

    assert resultado is not None, (
        "Con texto=' Puebla ' se esperaba 'puebla' y se obtuvo None. "
        "Una función sin return devuelve None: revisa que entregues "
        "el resultado con return y no con print()."
    )


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("  Monterrey ", "monterrey"),
        ("GUADALAJARA", "guadalajara"),
        ("\tCiudad de México\n", "ciudad de méxico"),
        ("tijuana", "tijuana"),
    ],
)
def test_ejercicio_1_quita_espacios_y_pasa_a_minusculas(texto, esperado):
    limpiar_texto = obtener_funcion("limpiar_texto")

    resultado = limpiar_texto(texto)

    assert resultado == esperado, (
        f"Con texto={texto!r} se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "Hay que quitar los espacios de los extremos y pasar a minúsculas."
    )


# --- Ejercicio 2: limpiar_precio ---


def test_ejercicio_2_la_funcion_existe_y_tiene_docstring():
    comprobar_docstring("limpiar_precio")


def test_ejercicio_2_el_parametro_simbolo_tiene_valor_por_defecto():
    limpiar_precio = obtener_funcion("limpiar_precio")

    parametros = inspect.signature(limpiar_precio).parameters
    nombres = list(parametros)

    assert nombres == ["texto", "simbolo"], (
        "limpiar_precio() debe tener dos parámetros, texto y simbolo, en ese "
        f"orden. Los parámetros que tiene ahora son {nombres!r}."
    )
    por_defecto = parametros["simbolo"].default
    assert por_defecto == "$", (
        "El parámetro simbolo debe tener '$' como valor por defecto y ahora "
        f"tiene {por_defecto!r}. Si ves algo con la palabra 'empty', todavía "
        "no tiene ninguno: el valor por defecto se escribe en la línea def."
    )


def test_ejercicio_2_devuelve_un_numero_con_decimales():
    limpiar_precio = obtener_funcion("limpiar_precio")

    resultado = limpiar_precio("45")

    assert isinstance(resultado, float), (
        "Con texto='45', limpiar_precio() debe devolver un número con decimales "
        f"(float). Devolvió {resultado!r}, que es de tipo "
        f"{type(resultado).__name__}."
    )


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("45.5", 45.5),
        ("$45.50", 45.5),
        (" $1,250.50 ", 1250.5),
        ("$1,000,000", 1000000.0),
    ],
)
def test_ejercicio_2_usa_el_simbolo_de_pesos_por_defecto(texto, esperado):
    limpiar_precio = obtener_funcion("limpiar_precio")

    resultado = limpiar_precio(texto)

    assert resultado == esperado, (
        f"Con texto={texto!r} y sin indicar simbolo se esperaba {esperado!r} "
        f"y se obtuvo {resultado!r}. Antes de convertir, quita los espacios, "
        "el símbolo y las comas."
    )


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("1,250.50 MXN", 1250.5),
        ("MXN 89.90", 89.9),
    ],
)
def test_ejercicio_2_acepta_otro_simbolo_por_nombre(texto, esperado):
    limpiar_precio = obtener_funcion("limpiar_precio")

    resultado = limpiar_precio(texto, simbolo="MXN")

    assert resultado == esperado, (
        f"Con texto={texto!r} y simbolo='MXN' se esperaba {esperado!r} "
        f"y se obtuvo {resultado!r}. Dentro de la función, quita el texto "
        "que llega en el parámetro simbolo, no un '$' fijo."
    )


def test_ejercicio_2_acepta_otro_simbolo_por_posicion():
    limpiar_precio = obtener_funcion("limpiar_precio")

    resultado = limpiar_precio("USD 2,100.00", "USD")

    assert resultado == 2100.0, (
        "Con texto='USD 2,100.00' y 'USD' como segundo argumento se esperaba "
        f"2100.0 y se obtuvo {resultado!r}. El segundo parámetro debe ser simbolo."
    )


# --- Ejercicio 3: es_faltante ---


def test_ejercicio_3_la_funcion_existe_y_tiene_docstring():
    comprobar_docstring("es_faltante")


@pytest.mark.parametrize(
    "valor",
    [None, "", "   ", "n/d", "N/D", " NA ", "null", "NULL"],
)
def test_ejercicio_3_reconoce_los_faltantes(valor):
    es_faltante = obtener_funcion("es_faltante")

    resultado = es_faltante(valor)

    assert resultado is True, (
        f"Con valor={valor!r} se esperaba True y se obtuvo {resultado!r}. "
        "Atiende primero el caso de None; después limpia el texto y compáralo "
        "con las formas de escribir un faltante."
    )


@pytest.mark.parametrize("valor", ["Puebla", "nada", "0", " Nayarit "])
def test_ejercicio_3_no_confunde_un_dato_real_con_un_faltante(valor):
    es_faltante = obtener_funcion("es_faltante")

    resultado = es_faltante(valor)

    assert resultado is False, (
        f"Con valor={valor!r} se esperaba False y se obtuvo {resultado!r}. "
        "El texto limpio debe ser exactamente uno de los faltantes, no solo "
        "parecerse. Si obtuviste None, algún camino de tu función termina "
        "sin return."
    )


# --- Ejercicio 4: limpiar_pedido ---


def test_ejercicio_4_devuelve_un_diccionario_con_las_seis_claves():
    resultado = limpiar_pedido(crear_pedido_crudo())

    assert isinstance(resultado, dict), (
        "limpiar_pedido() debe devolver un diccionario. "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}."
    )
    claves = sorted(resultado)
    assert claves == sorted(CLAVES_DE_PEDIDO), (
        f"Se esperaban las claves {sorted(CLAVES_DE_PEDIDO)!r} y se obtuvieron "
        f"{claves!r}. El diccionario nuevo lleva las mismas seis claves que "
        "el pedido crudo."
    )


@pytest.mark.parametrize(
    ("clave", "esperado"),
    [
        ("id_pedido", 1001),
        ("ciudad", "Guadalajara"),
        ("producto", "Prensa Francesa"),
        ("cantidad", 2),
        ("precio_unitario", 1250.5),
        ("estado", "entregado"),
    ],
)
def test_ejercicio_4_limpia_cada_campo(clave, esperado):
    pedido_crudo = crear_pedido_crudo()

    resultado = limpiar_pedido(pedido_crudo)

    assert resultado[clave] == esperado, (
        f"Con {clave}={pedido_crudo[clave]!r} en el pedido crudo se esperaba "
        f"{esperado!r} y se obtuvo {resultado[clave]!r}. Revisa qué función "
        "de limpieza o qué conversión le toca a ese campo."
    )


@pytest.mark.parametrize(
    ("clave", "tipo"),
    [("id_pedido", int), ("cantidad", int), ("precio_unitario", float)],
)
def test_ejercicio_4_convierte_los_numeros_al_tipo_correcto(clave, tipo):
    pedido_crudo = crear_pedido_crudo()

    resultado = limpiar_pedido(pedido_crudo)

    assert type(resultado[clave]) is tipo, (
        f"Con {clave}={pedido_crudo[clave]!r} en el pedido crudo se esperaba "
        f"un valor de tipo {tipo.__name__} y se obtuvo {resultado[clave]!r}, "
        f"de tipo {type(resultado[clave]).__name__}."
    )


def test_ejercicio_4_limpia_otro_pedido_distinto():
    pedido_crudo = {
        "id_pedido": "1002",
        "ciudad": "ciudad de méxico",
        "producto": "  FILTRO DE TELA  ",
        "cantidad": " 10 ",
        "precio_unitario": "60",
        "estado": "CANCELADO",
    }
    esperado = {
        "id_pedido": 1002,
        "ciudad": "Ciudad De México",
        "producto": "Filtro De Tela",
        "cantidad": 10,
        "precio_unitario": 60.0,
        "estado": "cancelado",
    }

    resultado = limpiar_pedido(pedido_crudo)

    assert resultado == esperado, (
        f"Con pedido_crudo={pedido_crudo!r} se esperaba {esperado!r} "
        f"y se obtuvo {resultado!r}. Usa los valores del parámetro, "
        "no valores fijos."
    )


def test_ejercicio_4_no_modifica_el_pedido_original():
    pedido_crudo = crear_pedido_crudo()

    resultado = limpiar_pedido(pedido_crudo)

    assert pedido_crudo == crear_pedido_crudo(), (
        "limpiar_pedido() cambió el diccionario que recibió: ahora vale "
        f"{pedido_crudo!r}. Crea un diccionario nuevo y deja intacto el original."
    )
    assert resultado is not pedido_crudo, (
        "limpiar_pedido() devolvió el mismo diccionario que recibió. "
        "Debe devolver uno nuevo."
    )


# --- Ejercicio 5: es_pedido_valido ---


def test_ejercicio_5_acepta_un_pedido_completo():
    pedido = crear_pedido_limpio()

    resultado = es_pedido_valido(pedido)

    assert resultado is True, (
        f"Con pedido={pedido!r} se esperaba True y se obtuvo {resultado!r}. "
        "Tiene ciudad, cantidad mayor que 0 y precio mayor que 0."
    )


@pytest.mark.parametrize(
    ("clave", "valor"),
    [
        ("ciudad", ""),
        ("ciudad", "N/D"),
        ("ciudad", "Na"),
        ("cantidad", 0),
        ("cantidad", -1),
        ("precio_unitario", 0.0),
    ],
)
def test_ejercicio_5_rechaza_un_pedido_con_un_dato_malo(clave, valor):
    pedido = crear_pedido_con(clave, valor)

    resultado = es_pedido_valido(pedido)

    assert resultado is False, (
        f"Con {clave}={valor!r} en el pedido se esperaba False y se obtuvo "
        f"{resultado!r}. Basta una condición incumplida para rechazarlo. "
        "Para la ciudad, reutiliza limpieza.es_faltante()."
    )


# --- Ejercicio 6: separar_validos ---


def test_ejercicio_6_devuelve_una_tupla_con_dos_listas():
    resultado = separar_validos([crear_pedido_limpio()])

    assert isinstance(resultado, tuple) and len(resultado) == 2, (
        "separar_validos() debe devolver una tupla con dos elementos y devolvió "
        f"{resultado!r}. Para devolver dos valores, sepáralos con una coma "
        "en el return."
    )
    validos, rechazados = resultado
    assert isinstance(validos, list) and isinstance(rechazados, list), (
        f"Los dos elementos de la tupla deben ser listas y se obtuvo {resultado!r}."
    )


def test_ejercicio_6_reparte_los_pedidos_y_conserva_el_orden():
    bueno_1 = crear_pedido_limpio()
    malo_1 = crear_pedido_con("ciudad", "N/D")
    bueno_2 = crear_pedido_con("id_pedido", 1003)
    malo_2 = crear_pedido_con("cantidad", 0)
    pedidos = [bueno_1, malo_1, bueno_2, malo_2]

    validos, rechazados = separar_validos(pedidos)

    assert validos == [bueno_1, bueno_2], (
        "Con cuatro pedidos (válido, sin ciudad, válido, cantidad 0) se "
        f"esperaban como válidos el primero y el tercero y se obtuvo {validos!r}. "
        "La primera lista de la tupla es la de válidos, en el orden de llegada."
    )
    assert rechazados == [malo_1, malo_2], (
        "Con cuatro pedidos (válido, sin ciudad, válido, cantidad 0) se "
        f"esperaban como rechazados el segundo y el cuarto y se obtuvo "
        f"{rechazados!r}. Todo pedido que no es válido va a la segunda lista."
    )


def test_ejercicio_6_con_lista_vacia_devuelve_dos_listas_vacias():
    resultado = separar_validos([])

    assert resultado == ([], []), (
        f"Con pedidos=[] se esperaba ([], []) y se obtuvo {resultado!r}. "
        "Las dos listas empiezan vacías, antes del bucle."
    )


def test_ejercicio_6_si_todos_son_validos_no_hay_rechazados():
    pedidos = [crear_pedido_limpio(), crear_pedido_con("id_pedido", 1002)]

    validos, rechazados = separar_validos(pedidos)

    assert len(validos) == 2 and rechazados == [], (
        "Con dos pedidos válidos se esperaban 2 válidos y 0 rechazados y se "
        f"obtuvieron {len(validos)} válidos y {len(rechazados)} rechazados."
    )


def test_ejercicio_6_no_modifica_la_lista_original():
    pedidos = [crear_pedido_limpio(), crear_pedido_con("cantidad", 0)]

    separar_validos(pedidos)

    assert pedidos == [crear_pedido_limpio(), crear_pedido_con("cantidad", 0)], (
        "separar_validos() cambió la lista que recibió: ahora vale "
        f"{pedidos!r}. Agrega cada pedido a una lista nueva sin quitarlo "
        "de la original."
    )
