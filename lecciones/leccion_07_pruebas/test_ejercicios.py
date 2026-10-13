"""Pruebas de la lección 7. No modifiques este archivo."""

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

from lecciones.leccion_07_pruebas import funciones
from lecciones.leccion_07_pruebas.ejercicios import (
    casos_de_limpiar_precio,
    comprobar_contar_por_ciudad,
    comprobar_limites_de_clasificar_importe,
    comprobar_limpiar_precio,
    comprobar_validar_cantidad_rechaza_invalidos,
)

CARPETA = Path(__file__).resolve().parent
RAIZ = CARPETA.parent.parent
ARCHIVO_DE_EJERCICIOS = CARPETA / "ejercicios.py"
ARCHIVO_DEL_ALUMNO = CARPETA / "test_mis_pruebas.py"
FUNCIONES_A_PROBAR = [
    "limpiar_precio",
    "clasificar_importe",
    "validar_cantidad",
    "contar_por_ciudad",
]

# --- Apoyo: cómo evaluamos tus comprobaciones ---
#
# Cada comprobación tuya se llama varias veces. Con la función correcta de
# funciones.py debe terminar sin error. Con cada versión defectuosa (están
# definidas más abajo, junto a su ejercicio) debe fallar algún assert.


def revisar_que_funciones_py_este_intacto():
    """Avisa si funciones.py quedó modificado después de provocar el error."""
    pedidos = [{"ciudad": " Puebla"}, {"ciudad": "PUEBLA"}, {"ciudad": "Mérida"}]
    try:
        intacto = (
            funciones.limpiar_precio(" $1,250.50 ") == 1250.5
            and funciones.clasificar_importe(499.99) == "bajo"
            and funciones.clasificar_importe(500) == "medio"
            and funciones.clasificar_importe(1999.99) == "medio"
            and funciones.clasificar_importe(2000) == "alto"
            and funciones.validar_cantidad("3") == 3
            and funciones.contar_por_ciudad(pedidos) == {"puebla": 2, "mérida": 1}
            and funciones.contar_por_ciudad([]) == {}
        )
        for texto in ["0", "-1", "tres", "2.5"]:
            with pytest.raises(ValueError):
                funciones.validar_cantidad(texto)
    except (Exception, pytest.fail.Exception):
        intacto = False

    if not intacto:
        pytest.fail(
            "El archivo funciones.py ya no se comporta como al inicio de la "
            "lección. Si lo cambiaste para provocar el error, deshaz ese cambio "
            "antes de evaluarte. Si no recuerdas qué cambiaste, el comando "
            "git restore lecciones/leccion_07_pruebas/funciones.py lo devuelve "
            "a su último commit.",
            pytrace=False,
        )


def llamar_con_la_funcion_correcta(comprobacion, funcion_correcta):
    """Llama a la comprobación del alumno con la función que sí funciona."""
    revisar_que_funciones_py_este_intacto()
    try:
        comprobacion(funcion_correcta)
    except (AssertionError, pytest.fail.Exception) as fallo:
        pytest.fail(
            f"Tu comprobación {comprobacion.__name__}() falló con "
            f"{funcion_correcta.__name__}() de funciones.py, que funciona bien. "
            "Entonces lo equivocado es la comprobación: revisa el valor que "
            f"esperas en el assert que falló. Detalle del fallo: {fallo}"
        )
    except NotImplementedError:
        raise
    except Exception as error:
        pytest.fail(
            f"Tu comprobación {comprobacion.__name__}() terminó con un error que "
            f"no viene de un assert: {type(error).__name__}: {error}. Pasó al "
            f"llamarla con {funcion_correcta.__name__}() de funciones.py, que "
            "funciona bien. Revisa cómo llamas a la función que recibes; si "
            "esperas que lance un error, la llamada va dentro de pytest.raises."
        )


def llamar_con_una_version_defectuosa(comprobacion, funcion_correcta, defectuosa):
    """Llama a la comprobación del alumno con una función que tiene un defecto."""
    # Una comprobación que falla siempre no detecta nada: primero debe pasar
    # con la función correcta. Aquí también falla si aún no está escrita.
    llamar_con_la_funcion_correcta(comprobacion, funcion_correcta)
    try:
        comprobacion(defectuosa)
    except (AssertionError, pytest.fail.Exception):
        # Es lo que queremos: algún assert (o pytest.raises) detectó el defecto.
        return
    except Exception as error:
        pytest.fail(
            f"Tu comprobación {comprobacion.__name__}() terminó con un error que "
            f"no viene de un assert: {type(error).__name__}: {error}. Una "
            "comprobación avisa de un defecto cuando falla un assert o un "
            "pytest.raises. Revisa cómo llamas a la función que recibes."
        )

    pytest.fail(
        f"A tu comprobación {comprobacion.__name__}() se le escapó un defecto. "
        f"Recibió una versión defectuosa ({defectuosa.__doc__}) y terminó sin "
        "que fallara ningún assert. Piensa con qué entrada se notaría ese "
        "defecto y agrega una comprobación para ella.",
        pytrace=False,
    )


def leer_arbol(ruta):
    """Lee un archivo de Python y devuelve su estructura para inspeccionarla."""
    codigo = ruta.read_text(encoding="utf-8")
    try:
        return ast.parse(codigo)
    except SyntaxError as error:
        pytest.fail(
            f"El archivo {ruta.name} tiene un error de sintaxis en la línea "
            f"{error.lineno}: {error.msg}. Corrígelo y vuelve a correr las pruebas.",
            pytrace=False,
        )


def buscar_funciones(arbol, prefijo):
    """Devuelve las funciones del archivo cuyo nombre empieza con el prefijo."""
    encontradas = []
    for nodo in arbol.body:
        if isinstance(nodo, ast.FunctionDef) and nodo.name.startswith(prefijo):
            encontradas.append(nodo)
    return encontradas


def usa_pytest_raises(funcion):
    """Dice si dentro de la función hay un bloque `with pytest.raises(...)`."""
    for nodo in ast.walk(funcion):
        if isinstance(nodo, ast.With):
            for elemento in nodo.items:
                llamada = elemento.context_expr
                if (
                    isinstance(llamada, ast.Call)
                    and isinstance(llamada.func, ast.Attribute)
                    and llamada.func.attr == "raises"
                ):
                    return True
    return False


def comprueba_algo(funcion):
    """Dice si la función tiene al menos un `assert` o un `pytest.raises`."""
    for nodo in ast.walk(funcion):
        if isinstance(nodo, ast.Assert):
            return True
    return usa_pytest_raises(funcion)


def esta_parametrizada(funcion):
    """Dice si la función lleva encima la etiqueta `@pytest.mark.parametrize`."""
    for etiqueta in funcion.decorator_list:
        if isinstance(etiqueta, ast.Call):
            etiqueta = etiqueta.func
        if isinstance(etiqueta, ast.Attribute) and etiqueta.attr == "parametrize":
            return True
    return False


def nombres_usados(funcion):
    """Devuelve los nombres que aparecen en el código de la función."""
    nombres = set()
    for nodo in ast.walk(funcion):
        if isinstance(nodo, ast.Name):
            nombres.add(nodo.id)
        elif isinstance(nodo, ast.Attribute):
            nombres.add(nodo.attr)
    return nombres


# --- Ejercicio 1: comprobar_limpiar_precio ---


def limpiar_precio_que_pierde_los_centavos(texto):
    """descarta los centavos del precio"""
    return float(int(funciones.limpiar_precio(texto)))


def limpiar_precio_que_corta_en_la_primera_coma(texto):
    """ignora todo lo que sigue a la primera coma de miles"""
    sin_simbolos = texto.strip().replace("$", "")
    return float(sin_simbolos.split(",")[0])


def limpiar_precio_que_borra_el_punto_decimal(texto):
    """quita el punto decimal junto con las comas"""
    sin_simbolos = texto.strip().replace("$", "").replace(",", "")
    return float(sin_simbolos.replace(".", ""))


def limpiar_precio_que_devuelve_texto(texto):
    """limpia el texto pero no lo convierte en número"""
    return texto.strip().replace("$", "").replace(",", "")


DEFECTUOSAS_DE_LIMPIAR_PRECIO = [
    pytest.param(limpiar_precio_que_pierde_los_centavos, id="pierde_los_centavos"),
    pytest.param(
        limpiar_precio_que_corta_en_la_primera_coma, id="corta_en_la_primera_coma"
    ),
    pytest.param(
        limpiar_precio_que_borra_el_punto_decimal, id="borra_el_punto_decimal"
    ),
    pytest.param(limpiar_precio_que_devuelve_texto, id="devuelve_texto"),
]


def test_ejercicio_1_pasa_con_la_funcion_correcta():
    llamar_con_la_funcion_correcta(comprobar_limpiar_precio, funciones.limpiar_precio)


@pytest.mark.parametrize("defectuosa", DEFECTUOSAS_DE_LIMPIAR_PRECIO)
def test_ejercicio_1_atrapa_la_version_que(defectuosa):
    llamar_con_una_version_defectuosa(
        comprobar_limpiar_precio, funciones.limpiar_precio, defectuosa
    )


# --- Ejercicio 2: comprobar_limites_de_clasificar_importe ---


def clasificar_importe_que_deja_el_500_fuera_de_medio(importe):
    """usa > en lugar de >= en el límite de 500"""
    if importe > 2000 or importe == 2000:
        return "alto"
    if importe > 500:
        return "medio"
    return "bajo"


def clasificar_importe_que_deja_el_2000_fuera_de_alto(importe):
    """usa > en lugar de >= en el límite de 2000"""
    if importe > 2000:
        return "alto"
    if importe >= 500:
        return "medio"
    return "bajo"


def clasificar_importe_que_ignora_los_centavos_en_500(importe):
    """compara con > 499 en el límite de 500, como si no existieran los centavos"""
    if importe >= 2000:
        return "alto"
    if importe > 499:
        return "medio"
    return "bajo"


def clasificar_importe_que_ignora_los_centavos_en_2000(importe):
    """compara con > 1999 en el límite de 2000, como si no existieran los centavos"""
    if importe > 1999:
        return "alto"
    if importe >= 500:
        return "medio"
    return "bajo"


DEFECTUOSAS_DE_CLASIFICAR_IMPORTE = [
    pytest.param(
        clasificar_importe_que_deja_el_500_fuera_de_medio,
        id="deja_el_500_fuera_de_medio",
    ),
    pytest.param(
        clasificar_importe_que_deja_el_2000_fuera_de_alto,
        id="deja_el_2000_fuera_de_alto",
    ),
    pytest.param(
        clasificar_importe_que_ignora_los_centavos_en_500,
        id="ignora_los_centavos_en_500",
    ),
    pytest.param(
        clasificar_importe_que_ignora_los_centavos_en_2000,
        id="ignora_los_centavos_en_2000",
    ),
]


def test_ejercicio_2_pasa_con_la_funcion_correcta():
    llamar_con_la_funcion_correcta(
        comprobar_limites_de_clasificar_importe, funciones.clasificar_importe
    )


@pytest.mark.parametrize("defectuosa", DEFECTUOSAS_DE_CLASIFICAR_IMPORTE)
def test_ejercicio_2_atrapa_la_version_que(defectuosa):
    llamar_con_una_version_defectuosa(
        comprobar_limites_de_clasificar_importe,
        funciones.clasificar_importe,
        defectuosa,
    )


# --- Ejercicio 3: comprobar_validar_cantidad_rechaza_invalidos ---


def validar_cantidad_que_acepta_el_cero(texto):
    """acepta el cero como cantidad válida"""
    cantidad = int(texto)
    if cantidad < 0:
        raise ValueError(f"La cantidad debe ser mayor que cero: {cantidad}")
    return cantidad


def validar_cantidad_que_acepta_negativos(texto):
    """acepta cantidades negativas"""
    cantidad = int(texto)
    if cantidad == 0:
        raise ValueError(f"La cantidad debe ser mayor que cero: {cantidad}")
    return cantidad


def validar_cantidad_que_devuelve_cero_si_no_es_numero(texto):
    """devuelve 0, sin lanzar error, cuando el texto no es un número"""
    try:
        cantidad = int(texto)
    except ValueError:
        return 0
    if cantidad <= 0:
        raise ValueError(f"La cantidad debe ser mayor que cero: {cantidad}")
    return cantidad


def validar_cantidad_que_recorta_los_decimales(texto):
    """acepta textos con decimales y les recorta la parte decimal"""
    cantidad = int(float(texto))
    if cantidad <= 0:
        raise ValueError(f"La cantidad debe ser mayor que cero: {cantidad}")
    return cantidad


DEFECTUOSAS_DE_VALIDAR_CANTIDAD = [
    pytest.param(validar_cantidad_que_acepta_el_cero, id="acepta_el_cero"),
    pytest.param(validar_cantidad_que_acepta_negativos, id="acepta_negativos"),
    pytest.param(
        validar_cantidad_que_devuelve_cero_si_no_es_numero,
        id="devuelve_cero_si_no_es_numero",
    ),
    pytest.param(
        validar_cantidad_que_recorta_los_decimales, id="recorta_los_decimales"
    ),
]


def test_ejercicio_3_pasa_con_la_funcion_correcta():
    llamar_con_la_funcion_correcta(
        comprobar_validar_cantidad_rechaza_invalidos, funciones.validar_cantidad
    )


def test_ejercicio_3_usa_pytest_raises():
    # Primero se llama, para que una comprobación sin escribir no pase esta prueba.
    comprobar_validar_cantidad_rechaza_invalidos(funciones.validar_cantidad)
    nombre = "comprobar_validar_cantidad_rechaza_invalidos"
    comprobacion = buscar_funciones(leer_arbol(ARCHIVO_DE_EJERCICIOS), nombre)[0]

    assert usa_pytest_raises(comprobacion), (
        f"En {nombre}() no se encontró ningún bloque with pytest.raises(...). "
        "Para comprobar que una función lanza un error, la llamada va dentro "
        "de ese bloque. Repasa el concepto 4 de la guía."
    )


@pytest.mark.parametrize("defectuosa", DEFECTUOSAS_DE_VALIDAR_CANTIDAD)
def test_ejercicio_3_atrapa_la_version_que(defectuosa):
    llamar_con_una_version_defectuosa(
        comprobar_validar_cantidad_rechaza_invalidos,
        funciones.validar_cantidad,
        defectuosa,
    )


# --- Ejercicio 4: comprobar_contar_por_ciudad ---


def contar_por_ciudad_que_distingue_mayusculas(pedidos):
    """distingue mayúsculas de minúsculas en el nombre de la ciudad"""
    conteo = {}
    for pedido in pedidos:
        ciudad = pedido["ciudad"].strip()
        conteo[ciudad] = conteo.get(ciudad, 0) + 1
    return conteo


def contar_por_ciudad_que_no_quita_espacios(pedidos):
    """no quita los espacios de los extremos del nombre de la ciudad"""
    conteo = {}
    for pedido in pedidos:
        ciudad = pedido["ciudad"].lower()
        conteo[ciudad] = conteo.get(ciudad, 0) + 1
    return conteo


def contar_por_ciudad_que_cuenta_uno_por_ciudad(pedidos):
    """anota 1 en cada ciudad, sin importar cuántos pedidos tenga"""
    conteo = {}
    for pedido in pedidos:
        ciudad = pedido["ciudad"].strip().lower()
        conteo[ciudad] = 1
    return conteo


def contar_por_ciudad_que_olvida_el_ultimo_pedido(pedidos):
    """no cuenta el último pedido de la lista"""
    return funciones.contar_por_ciudad(pedidos[:-1])


def contar_por_ciudad_que_devuelve_none_con_lista_vacia(pedidos):
    """devuelve None, y no un diccionario vacío, cuando la lista está vacía"""
    if not pedidos:
        return None
    return funciones.contar_por_ciudad(pedidos)


DEFECTUOSAS_DE_CONTAR_POR_CIUDAD = [
    pytest.param(contar_por_ciudad_que_distingue_mayusculas, id="distingue_mayusculas"),
    pytest.param(contar_por_ciudad_que_no_quita_espacios, id="no_quita_espacios"),
    pytest.param(
        contar_por_ciudad_que_cuenta_uno_por_ciudad, id="cuenta_uno_por_ciudad"
    ),
    pytest.param(
        contar_por_ciudad_que_olvida_el_ultimo_pedido, id="olvida_el_ultimo_pedido"
    ),
    pytest.param(
        contar_por_ciudad_que_devuelve_none_con_lista_vacia,
        id="devuelve_none_con_lista_vacia",
    ),
]


def test_ejercicio_4_pasa_con_la_funcion_correcta():
    llamar_con_la_funcion_correcta(
        comprobar_contar_por_ciudad, funciones.contar_por_ciudad
    )


@pytest.mark.parametrize("defectuosa", DEFECTUOSAS_DE_CONTAR_POR_CIUDAD)
def test_ejercicio_4_atrapa_la_version_que(defectuosa):
    llamar_con_una_version_defectuosa(
        comprobar_contar_por_ciudad, funciones.contar_por_ciudad, defectuosa
    )


# --- Ejercicio 5: casos_de_limpiar_precio ---


def trae_simbolo_de_pesos(texto, esperado):
    """con el símbolo $"""
    return "$" in texto


def trae_comas_de_miles(texto, esperado):
    """con comas de miles"""
    return "," in texto


def trae_espacios_en_los_extremos(texto, esperado):
    """con espacios al inicio o al final"""
    return texto != texto.strip()


def trae_centavos(texto, esperado):
    """con centavos, es decir, con decimales distintos de cero"""
    return esperado != int(esperado)


def pedir_casos_con_buena_forma():
    """Pide los casos al alumno y revisa que sean una lista de tuplas válidas."""
    revisar_que_funciones_py_este_intacto()
    casos = casos_de_limpiar_precio()

    assert isinstance(casos, list), (
        "casos_de_limpiar_precio() debe devolver una lista. "
        f"Devolvió {casos!r}, que es de tipo {type(casos).__name__}."
    )
    for caso in casos:
        assert isinstance(caso, tuple) and len(caso) == 2, (
            f"Cada caso debe ser una tupla de dos elementos, (texto, esperado). "
            f"Se encontró {caso!r}."
        )
        texto, esperado = caso
        assert isinstance(texto, str), (
            f"En el caso {caso!r}, el primer elemento debe ser el texto que "
            f"recibe limpiar_precio(). Se encontró {texto!r}, que es de tipo "
            f"{type(texto).__name__}."
        )
        es_numero = isinstance(esperado, (int, float)) and not isinstance(
            esperado, bool
        )
        assert es_numero, (
            f"En el caso {caso!r}, el segundo elemento debe ser el número "
            f"esperado. Se encontró {esperado!r}, que es de tipo "
            f"{type(esperado).__name__}."
        )
    return casos


def test_ejercicio_5_devuelve_al_menos_cuatro_casos_distintos():
    casos = pedir_casos_con_buena_forma()
    textos = []
    for texto, _ in casos:
        if texto not in textos:
            textos.append(texto)

    assert len(textos) >= 4, (
        f"Se esperaban al menos 4 casos con textos distintos y se encontraron "
        f"{len(textos)}: {textos!r}. Repetir el mismo texto no agrega información."
    )


def test_ejercicio_5_cada_esperado_es_el_resultado_correcto():
    casos = pedir_casos_con_buena_forma()

    assert casos, "La lista de casos está vacía. Agrega al menos cuatro."
    for texto, esperado in casos:
        resultado = funciones.limpiar_precio(texto)

        assert resultado == esperado, (
            f"En el caso ({texto!r}, {esperado!r}) el valor esperado no es "
            f"correcto: limpiar_precio({texto!r}) devuelve {resultado!r}, y esa "
            "función sí funciona bien. Corrige el esperado de ese caso."
        )


@pytest.mark.parametrize(
    "caracteristica",
    [
        pytest.param(trae_simbolo_de_pesos, id="simbolo_de_pesos"),
        pytest.param(trae_comas_de_miles, id="comas_de_miles"),
        pytest.param(trae_espacios_en_los_extremos, id="espacios_en_los_extremos"),
        pytest.param(trae_centavos, id="centavos"),
    ],
)
def test_ejercicio_5_incluye_un_caso_con(caracteristica):
    casos = pedir_casos_con_buena_forma()
    casos_que_cumplen = []
    for texto, esperado in casos:
        if caracteristica(texto, esperado):
            casos_que_cumplen.append((texto, esperado))

    assert casos_que_cumplen, (
        f"Entre tus casos {casos!r} no hay ningún precio "
        f"{caracteristica.__doc__}. Los datos reales llegan así, y un caso "
        "que no pruebas es un caso que puede fallar sin que te enteres."
    )


@pytest.mark.parametrize("defectuosa", DEFECTUOSAS_DE_LIMPIAR_PRECIO)
def test_ejercicio_5_los_casos_atrapan_la_version_que(defectuosa):
    casos = pedir_casos_con_buena_forma()
    casos_que_la_atrapan = []
    for texto, esperado in casos:
        # Un caso con el esperado equivocado no cuenta como detección.
        if funciones.limpiar_precio(texto) != esperado:
            continue
        try:
            resultado = defectuosa(texto)
        except ValueError:
            resultado = None
        if resultado != esperado:
            casos_que_la_atrapan.append((texto, esperado))

    assert casos_que_la_atrapan, (
        f"A tus casos {casos!r} se les escapó un defecto. Una versión "
        f"defectuosa de limpiar_precio() ({defectuosa.__doc__}) devuelve lo "
        "esperado en todos ellos. Piensa qué texto haría visible ese defecto "
        "y agrégalo."
    )


# --- Ejercicio 6: tu archivo test_mis_pruebas.py ---


def buscar_pruebas_del_alumno():
    """Devuelve las funciones test_ que el alumno escribió en su archivo."""
    assert ARCHIVO_DEL_ALUMNO.exists(), (
        f"No se encontró el archivo {ARCHIVO_DEL_ALUMNO.name} en la carpeta de "
        "la lección. Debe llamarse exactamente así para que pytest lo descubra."
    )
    return buscar_funciones(leer_arbol(ARCHIVO_DEL_ALUMNO), "test_")


def test_ejercicio_6_tiene_al_menos_tres_pruebas():
    pruebas = buscar_pruebas_del_alumno()
    nombres = []
    for prueba in pruebas:
        nombres.append(prueba.name)

    assert len(pruebas) >= 3, (
        f"En {ARCHIVO_DEL_ALUMNO.name} se esperaban al menos 3 funciones cuyo "
        f"nombre empiece con test_ y se encontraron {len(pruebas)}: {nombres!r}. "
        "pytest solo descubre las funciones que siguen esa convención."
    )


def test_ejercicio_6_cada_prueba_comprueba_algo():
    pruebas = buscar_pruebas_del_alumno()
    sin_comprobacion = []
    for prueba in pruebas:
        if not comprueba_algo(prueba):
            sin_comprobacion.append(prueba.name)

    assert pruebas, (
        f"Todavía no hay funciones test_ en {ARCHIVO_DEL_ALUMNO.name}. "
        "Escribe la primera siguiendo el concepto 2 de la guía."
    )
    assert not sin_comprobacion, (
        f"Estas pruebas no tienen ningún assert ni pytest.raises: "
        f"{sin_comprobacion!r}. Una prueba que no comprueba nada pasa siempre, "
        "aunque el código esté mal."
    )


def test_ejercicio_6_al_menos_una_prueba_esta_parametrizada():
    pruebas = buscar_pruebas_del_alumno()
    parametrizadas = []
    for prueba in pruebas:
        if esta_parametrizada(prueba):
            parametrizadas.append(prueba.name)

    assert parametrizadas, (
        f"Ninguna de las {len(pruebas)} pruebas de {ARCHIVO_DEL_ALUMNO.name} "
        "lleva encima la etiqueta @pytest.mark.parametrize. Elige una prueba "
        "con varios casos de la misma lógica y conviértela, como en el "
        "concepto 5 de la guía."
    )


def test_ejercicio_6_las_pruebas_usan_al_menos_tres_funciones():
    pruebas = buscar_pruebas_del_alumno()
    usadas = []
    for nombre in FUNCIONES_A_PROBAR:
        for prueba in pruebas:
            if nombre in nombres_usados(prueba) and nombre not in usadas:
                usadas.append(nombre)

    assert len(usadas) >= 3, (
        f"Tus pruebas deben usar al menos 3 de las 4 funciones de funciones.py "
        f"({FUNCIONES_A_PROBAR!r}) y usan {len(usadas)}: {usadas!r}. "
        "Agrega pruebas para alguna de las que faltan."
    )


def test_ejercicio_6_todas_tus_pruebas_pasan():
    revisar_que_funciones_py_este_intacto()
    pruebas = buscar_pruebas_del_alumno()
    assert pruebas, (
        f"Todavía no hay funciones test_ en {ARCHIVO_DEL_ALUMNO.name}, así que "
        "no hay nada que correr."
    )
    entorno = dict(os.environ)
    entorno["PYTHONUTF8"] = "1"

    proceso = subprocess.run(
        [sys.executable, "-m", "pytest", str(ARCHIVO_DEL_ALUMNO), "-q"],
        cwd=RAIZ,
        env=entorno,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    if proceso.returncode != 0:
        pytest.fail(
            f"Al correr pytest sobre {ARCHIVO_DEL_ALUMNO.name} no pasaron todas "
            "tus pruebas. Como funciones.py funciona bien, revisa qué espera "
            "cada prueba que falla. Esto respondió pytest:\n\n"
            + proceso.stdout[-3000:],
            pytrace=False,
        )
