"""Pruebas de la lección 6. No modifiques este archivo."""

import builtins
import csv
import json
import pathlib
from pathlib import Path

import pytest

from lecciones.leccion_06_archivos_y_errores.ejercicios import (
    a_entero,
    contar_lineas,
    escribir_csv,
    guardar_json,
    leer_csv,
    leer_json,
    validar_cantidad,
)

CSV_PEDIDOS = (
    "id_pedido,cliente,ciudad,cantidad,precio_unitario\n"
    "1001,Ana López,Mérida,2,45.50\n"
    '1002,Sofía Peña,Ciudad de México,1,"$1,250.50"\n'
    "1003,Diego Castañeda,Tijuana,N/D,85\n"
)

FILAS = [
    {"id_pedido": "1001", "cliente": "Ana López", "ciudad": "Mérida"},
    {"id_pedido": "1002", "cliente": "Sofía Peña", "ciudad": "Ciudad de México"},
    {"id_pedido": "1003", "cliente": "Diego Castañeda", "ciudad": "Tijuana"},
]
COLUMNAS = ["id_pedido", "cliente", "ciudad"]


def aperturas_de_archivo_durante(monkeypatch, accion):
    """Corre accion() y anota cada vez que se abre un archivo.

    Espía tanto open(...) como ruta.open(...) y devuelve una lista de
    tuplas (ruta, modo, newline) con lo que recibió cada apertura.
    """
    aperturas = []
    open_original = builtins.open
    path_open_original = pathlib.Path.open

    def valor(args, kwargs, nombre, posicion, por_defecto):
        if nombre in kwargs:
            return kwargs[nombre]
        if len(args) > posicion:
            return args[posicion]
        return por_defecto

    def open_espia(*args, **kwargs):
        aperturas.append(
            (
                Path(valor(args, kwargs, "file", 0, "")),
                valor(args, kwargs, "mode", 1, "r"),
                valor(args, kwargs, "newline", 5, None),
            )
        )
        return open_original(*args, **kwargs)

    def path_open_espia(self, *args, **kwargs):
        aperturas.append(
            (
                Path(self),
                valor(args, kwargs, "mode", 0, "r"),
                valor(args, kwargs, "newline", 4, None),
            )
        )
        return path_open_original(self, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", open_espia)
    monkeypatch.setattr(pathlib.Path, "open", path_open_espia)
    accion()
    monkeypatch.undo()
    return aperturas


# --- Ejercicio 1: contar_lineas ---


@pytest.mark.parametrize(
    ("contenido", "esperado"),
    [
        ("Mérida\nPuebla\nTijuana\n", 3),
        ("Mérida\n\nPuebla\n\n\nTijuana\n", 3),
        ("Mérida\n   \nPuebla\n\t\n", 2),
        ("Café de olla", 1),
        ("", 0),
        ("\n\n\n", 0),
    ],
)
def test_ejercicio_1_cuenta_solo_las_lineas_no_vacias(tmp_path, contenido, esperado):
    ruta = tmp_path / "notas.txt"
    ruta.write_text(contenido, encoding="utf-8")

    resultado = contar_lineas(ruta)

    assert resultado == esperado, (
        f"Con un archivo cuyo contenido es {contenido!r} se esperaba {esperado} "
        f"y se obtuvo {resultado!r}. Una línea vacía, o que solo tiene espacios, "
        "no se cuenta."
    )


def test_ejercicio_1_lee_un_archivo_con_acentos_y_enie(tmp_path):
    ruta = tmp_path / "clientes.txt"
    ruta.write_text("Núñez\nPeña\nLópez\nCastañeda\n", encoding="utf-8")

    resultado = contar_lineas(ruta)

    assert resultado == 4, (
        "Con un archivo UTF-8 de cuatro apellidos con acentos y ñ se esperaba 4 "
        f"y se obtuvo {resultado!r}. Indica la codificación al leer el archivo."
    )


def test_ejercicio_1_acepta_la_ruta_como_texto(tmp_path):
    ruta = tmp_path / "notas.txt"
    ruta.write_text("uno\ndos\n", encoding="utf-8")

    resultado = contar_lineas(str(ruta))

    assert resultado == 2, (
        "Al pasar la ruta como texto (str) en lugar de Path se esperaba 2 "
        f"y se obtuvo {resultado!r}. Convierte la ruta con Path() al inicio."
    )


# --- Ejercicio 2: a_entero ---


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("5", 5),
        ("120", 120),
        (" 12 ", 12),
        ("-3", -3),
        ("0", 0),
    ],
)
def test_ejercicio_2_convierte_textos_validos(texto, esperado):
    resultado = a_entero(texto)

    assert resultado == esperado, (
        f"Con texto={texto!r} se esperaba {esperado!r} y se obtuvo {resultado!r}. "
        "Si el texto sí representa un entero, la función devuelve ese entero."
    )


@pytest.mark.parametrize("texto", ["", "N/D", "NA", "dos", "3.5", "1,250"])
def test_ejercicio_2_devuelve_cero_si_no_se_puede_convertir(texto):
    resultado = a_entero(texto)

    assert resultado == 0, (
        f"Con texto={texto!r} y sin indicar por_defecto se esperaba 0 "
        f"y se obtuvo {resultado!r}. Atrapa el error que produce int() "
        "y devuelve el valor por defecto."
    )


@pytest.mark.parametrize("por_defecto", [-1, None, 99])
def test_ejercicio_2_usa_el_valor_por_defecto_indicado(por_defecto):
    resultado = a_entero("N/D", por_defecto=por_defecto)

    assert resultado == por_defecto, (
        f"Con texto='N/D' y por_defecto={por_defecto!r} se esperaba "
        f"{por_defecto!r} y se obtuvo {resultado!r}. Devuelve el parámetro "
        "por_defecto, no un valor fijo."
    )


def test_ejercicio_2_no_usa_el_valor_por_defecto_si_el_texto_es_valido():
    resultado = a_entero("7", por_defecto=-1)

    assert resultado == 7, (
        "Con texto='7' y por_defecto=-1 se esperaba 7 "
        f"y se obtuvo {resultado!r}. El valor por defecto solo se usa "
        "cuando la conversión falla."
    )


# --- Ejercicio 3: leer_csv ---


def test_ejercicio_3_devuelve_una_lista_con_un_diccionario_por_fila(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    ruta.write_text(CSV_PEDIDOS, encoding="utf-8")

    resultado = leer_csv(ruta)

    assert isinstance(resultado, list) and len(resultado) == 3, (
        "Con un archivo de encabezado y 3 filas se esperaba una lista de 3 "
        f"diccionarios y se obtuvo {resultado!r}. El encabezado no es una fila "
        "de datos, y lo que se devuelve es una lista, no el lector."
    )


def test_ejercicio_3_usa_los_encabezados_como_claves(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    ruta.write_text(CSV_PEDIDOS, encoding="utf-8")
    esperado = {
        "id_pedido": "1001",
        "cliente": "Ana López",
        "ciudad": "Mérida",
        "cantidad": "2",
        "precio_unitario": "45.50",
    }

    resultado = leer_csv(ruta)

    assert resultado[0] == esperado, (
        f"Para la primera fila se esperaba {esperado!r} y se obtuvo "
        f"{resultado[0]!r}. Revisa que leas con csv.DictReader, con "
        "codificación UTF-8, y que no conviertas los valores: llegan como texto."
    )


def test_ejercicio_3_conserva_acentos_y_enie(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    ruta.write_text(CSV_PEDIDOS, encoding="utf-8")

    resultado = leer_csv(ruta)
    clientes = []
    for fila in resultado:
        clientes.append(fila["cliente"])

    assert clientes == ["Ana López", "Sofía Peña", "Diego Castañeda"], (
        "Se esperaban los clientes ['Ana López', 'Sofía Peña', 'Diego Castañeda'] "
        f"y se obtuvo {clientes!r}. Si ves letras extrañas, falta indicar "
        "la codificación al abrir el archivo."
    )


def test_ejercicio_3_respeta_las_comas_dentro_de_comillas(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    ruta.write_text(CSV_PEDIDOS, encoding="utf-8")

    resultado = leer_csv(ruta)
    precio = resultado[1]["precio_unitario"]

    assert precio == "$1,250.50", (
        "En la segunda fila se esperaba precio_unitario='$1,250.50' "
        f"y se obtuvo {precio!r}. Deja que el módulo csv separe las columnas; "
        "no partas las líneas a mano."
    )


def test_ejercicio_3_un_archivo_con_solo_encabezado_da_lista_vacia(tmp_path):
    ruta = tmp_path / "vacio.csv"
    ruta.write_text("id_pedido,cliente,ciudad\n", encoding="utf-8")

    resultado = leer_csv(ruta)

    assert resultado == [], (
        "Con un archivo que solo tiene el encabezado se esperaba [] "
        f"y se obtuvo {resultado!r}."
    )


def test_ejercicio_3_acepta_la_ruta_como_texto(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    ruta.write_text(CSV_PEDIDOS, encoding="utf-8")

    resultado = leer_csv(str(ruta))

    assert len(resultado) == 3, (
        "Al pasar la ruta como texto (str) en lugar de Path se esperaban 3 filas "
        f"y se obtuvo {resultado!r}. Convierte la ruta con Path() al inicio."
    )


def test_ejercicio_3_avisa_en_espanol_si_el_archivo_no_existe(tmp_path):
    ruta = tmp_path / "no_existe.csv"

    with pytest.raises(FileNotFoundError, match="No se encontró el archivo") as info:
        leer_csv(ruta)

    assert str(ruta) in str(info.value), (
        f"Con la ruta {str(ruta)!r} se esperaba que el mensaje del error la "
        f"incluyera, y el mensaje fue {str(info.value)!r}. Arma el mensaje "
        "con un f-string que termine con la ruta."
    )


# --- Ejercicio 4: escribir_csv ---


def test_ejercicio_4_devuelve_el_numero_de_filas_escritas(tmp_path):
    ruta = tmp_path / "pedidos.csv"

    resultado = escribir_csv(ruta, FILAS, COLUMNAS)

    assert resultado == 3, (
        f"Con 3 filas se esperaba que la función devolviera 3 y devolvió "
        f"{resultado!r}. El encabezado no se cuenta."
    )


def test_ejercicio_4_lo_escrito_se_puede_volver_a_leer(tmp_path):
    ruta = tmp_path / "pedidos.csv"

    escribir_csv(ruta, FILAS, COLUMNAS)
    with ruta.open(encoding="utf-8", newline="") as archivo:
        leidas = list(csv.DictReader(archivo))

    assert leidas == FILAS, (
        f"Después de escribir {FILAS!r} y leer el archivo con csv.DictReader "
        f"se obtuvo {leidas!r}. Revisa que escribas el encabezado y todas "
        "las filas, con codificación UTF-8."
    )


def test_ejercicio_4_escribe_el_encabezado_en_el_orden_de_columnas(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    columnas = ["ciudad", "id_pedido", "cliente"]

    escribir_csv(ruta, FILAS, columnas)
    lineas = ruta.read_text(encoding="utf-8").splitlines()

    assert lineas[:2] == ["ciudad,id_pedido,cliente", "Mérida,1001,Ana López"], (
        f"Con columnas={columnas!r} se esperaba que las dos primeras líneas "
        "fueran ['ciudad,id_pedido,cliente', 'Mérida,1001,Ana López'] "
        f"y se obtuvo {lineas[:2]!r}. El orden lo define el parámetro columnas, "
        "no el orden de las claves de cada diccionario."
    )


def test_ejercicio_4_no_deja_lineas_en_blanco_entre_filas(tmp_path):
    ruta = tmp_path / "pedidos.csv"

    escribir_csv(ruta, FILAS, COLUMNAS)
    contenido = ruta.read_bytes()
    lineas = contenido.decode("utf-8").splitlines()

    assert b"\r\r\n" not in contenido, (
        "El archivo tiene finales de línea dobles (\\r\\r\\n): es la marca de "
        "haber abierto el archivo sin newline=''. En Windows eso deja una línea "
        "en blanco entre fila y fila. Revisa el argumento newline al abrir."
    )
    assert len(lineas) == 4 and "" not in lineas, (
        "Con encabezado y 3 filas se esperaban 4 líneas, ninguna vacía, "
        f"y se obtuvo {lineas!r}. Revisa el argumento newline al abrir el archivo."
    )


def test_ejercicio_4_abre_el_archivo_con_newline_vacio(tmp_path, monkeypatch):
    # En macOS y Linux el archivo sale bien aunque falte newline="", así que la
    # prueba anterior no lo nota. Aquí se revisa con qué valor se abrió el
    # archivo, para que el mismo código funcione también en Windows.
    ruta = tmp_path / "pedidos.csv"

    aperturas = aperturas_de_archivo_durante(
        monkeypatch, lambda: escribir_csv(ruta, FILAS, COLUMNAS)
    )
    escrituras = [
        newline
        for destino, modo, newline in aperturas
        if destino == ruta and any(letra in modo for letra in "wax")
    ]

    assert escrituras, (
        "escribir_csv() no abrió el archivo para escribir. Ábrelo con "
        "open(ruta, 'w', ...) o ruta.open('w', ...)."
    )
    assert all(newline == "" for newline in escrituras), (
        "escribir_csv() abrió el archivo sin newline='' (se recibió "
        f"newline={escrituras[0]!r}). Sin él, en Windows el módulo csv y Python "
        "traducen los finales de línea por separado y el archivo queda con una "
        "línea en blanco entre fila y fila. Abre siempre el archivo con "
        "encoding='utf-8', newline='' cuando uses el módulo csv."
    )


def test_ejercicio_4_guarda_acentos_y_enie_en_utf8(tmp_path):
    ruta = tmp_path / "pedidos.csv"

    escribir_csv(ruta, FILAS, COLUMNAS)
    contenido = ruta.read_bytes()

    assert "Castañeda".encode() in contenido and "Mérida".encode() in contenido, (
        "Se esperaba encontrar 'Castañeda' y 'Mérida' guardados en UTF-8 "
        f"y el archivo contiene {contenido!r}. Indica encoding al abrir "
        "el archivo para escribir."
    )


def test_ejercicio_4_crea_la_carpeta_de_destino_si_no_existe(tmp_path):
    ruta = tmp_path / "salida" / "marzo" / "pedidos.csv"

    escribir_csv(ruta, FILAS, COLUMNAS)

    assert ruta.exists(), (
        "Se pidió escribir en salida/marzo/pedidos.csv, dentro de carpetas que "
        "aún no existían, y el archivo no se creó. Crea la carpeta que contiene "
        "al archivo antes de abrirlo."
    )


def test_ejercicio_4_funciona_si_la_carpeta_ya_existe(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    escribir_csv(ruta, FILAS, COLUMNAS)

    resultado = escribir_csv(ruta, FILAS[:1], COLUMNAS)
    lineas = ruta.read_text(encoding="utf-8").splitlines()

    assert resultado == 1 and len(lineas) == 2, (
        "Al escribir por segunda vez en el mismo archivo, ahora con 1 fila, "
        f"se esperaba que devolviera 1 y dejara 2 líneas; devolvió {resultado!r} "
        f"y el archivo tiene {lineas!r}. El archivo se sobrescribe completo "
        "y la carpeta existente no debe causar un error."
    )


def test_ejercicio_4_sin_filas_escribe_solo_el_encabezado(tmp_path):
    ruta = tmp_path / "vacio.csv"

    resultado = escribir_csv(ruta, [], COLUMNAS)
    lineas = ruta.read_text(encoding="utf-8").splitlines()

    assert resultado == 0 and lineas == ["id_pedido,cliente,ciudad"], (
        "Con filas=[] se esperaba que devolviera 0 y que el archivo tuviera solo "
        f"el encabezado; devolvió {resultado!r} y el archivo tiene {lineas!r}."
    )


def test_ejercicio_4_acepta_la_ruta_como_texto_y_no_modifica_las_filas(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    filas = [{"id_pedido": "1001", "cliente": "Ana López", "ciudad": "Mérida"}]

    escribir_csv(str(ruta), filas, COLUMNAS)

    assert ruta.exists() and filas == [FILAS[0]], (
        "Al pasar la ruta como texto (str) se esperaba que el archivo se creara "
        f"y que la lista de filas quedara intacta; la lista quedó como {filas!r}. "
        "Convierte la ruta con Path() al inicio y no cambies los diccionarios."
    )


# --- Ejercicio 5: guardar_json ---


def test_ejercicio_5_guarda_los_acentos_sin_escapar(tmp_path):
    ruta = tmp_path / "resumen.json"

    guardar_json(ruta, {"pais": "México", "cliente": "Sofía Peña"})
    contenido = ruta.read_bytes().decode("utf-8")

    assert "México" in contenido and "Peña" in contenido, (
        "Se esperaba que el archivo contuviera literalmente 'México' y 'Peña' "
        f"y su contenido es {contenido!r}. Revisa el argumento de json.dumps "
        "que evita escapar los acentos, y la codificación al escribir."
    )


def test_ejercicio_5_usa_sangria_de_dos_espacios(tmp_path):
    ruta = tmp_path / "resumen.json"
    esperado = '{\n  "pais": "México",\n  "pedidos": 9\n}'

    guardar_json(ruta, {"pais": "México", "pedidos": 9})
    contenido = ruta.read_text(encoding="utf-8")

    assert contenido == esperado, (
        f"Con datos={{'pais': 'México', 'pedidos': 9}} se esperaba el texto "
        f"{esperado!r} y se obtuvo {contenido!r}. Cada nivel lleva una sangría "
        "de 2 espacios."
    )


def test_ejercicio_5_lo_guardado_se_puede_volver_a_cargar(tmp_path):
    ruta = tmp_path / "reporte.json"
    datos = {
        "ciudades": ["Mérida", "Tijuana"],
        "totales": {"entregado": 5, "cancelado": 1},
        "promedio": 45.5,
        "responsable": None,
    }

    guardar_json(ruta, datos)
    cargados = json.loads(ruta.read_text(encoding="utf-8"))

    assert cargados == datos, (
        f"Después de guardar {datos!r} y cargar el archivo con json.loads "
        f"se obtuvo {cargados!r}. Guarda los datos completos, sin cambiarlos."
    )


def test_ejercicio_5_acepta_la_ruta_como_texto(tmp_path):
    ruta = tmp_path / "lista.json"

    guardar_json(str(ruta), ["Café de olla", "Taza de barro"])

    assert ruta.exists(), (
        "Al pasar la ruta como texto (str) se esperaba que el archivo se creara "
        "y no existe. Convierte la ruta con Path() antes de escribir."
    )


# --- Ejercicio 6: leer_json ---


def test_ejercicio_6_devuelve_los_datos_del_archivo(tmp_path):
    ruta = tmp_path / "resumen.json"
    ruta.write_text('{"pais": "México", "pedidos": 9}', encoding="utf-8")

    resultado = leer_json(ruta)

    assert resultado == {"pais": "México", "pedidos": 9}, (
        'Con un archivo que contiene {"pais": "México", "pedidos": 9} se '
        f"esperaba el diccionario {{'pais': 'México', 'pedidos': 9}} y se obtuvo "
        f"{resultado!r}. Lee el texto en UTF-8 y conviértelo con el módulo json."
    )


def test_ejercicio_6_lee_listas_con_acentos_y_enie(tmp_path):
    ruta = tmp_path / "clientes.json"
    ruta.write_text('[\n  "Núñez",\n  "Castañeda"\n]', encoding="utf-8")

    resultado = leer_json(str(ruta))

    assert resultado == ["Núñez", "Castañeda"], (
        'Con un archivo que contiene la lista ["Núñez", "Castañeda"] y la '
        f"ruta como texto se esperaba ['Núñez', 'Castañeda'] y se obtuvo "
        f"{resultado!r}. Indica la codificación al leer."
    )


@pytest.mark.parametrize(
    "contenido",
    ["", "esto no es JSON", '{"pais": "México",}', "{'pais': 'México'}"],
)
def test_ejercicio_6_rechaza_contenido_que_no_es_json(tmp_path, contenido):
    ruta = tmp_path / "roto.json"
    ruta.write_text(contenido, encoding="utf-8")

    with pytest.raises(ValueError, match="El archivo no contiene JSON válido") as info:
        leer_json(ruta)

    assert str(ruta) in str(info.value), (
        f"Con un archivo cuyo contenido es {contenido!r} se esperaba que el "
        f"mensaje del error incluyera la ruta {str(ruta)!r}, y el mensaje fue "
        f"{str(info.value)!r}. Arma el mensaje con un f-string."
    )


def test_ejercicio_6_no_esconde_el_error_de_archivo_inexistente(tmp_path):
    ruta = tmp_path / "no_existe.json"

    with pytest.raises(FileNotFoundError):
        leer_json(ruta)


# --- Ejercicio 7: validar_cantidad ---


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("3", 3),
        ("1", 1),
        (" 10 ", 10),
        ("250", 250),
    ],
)
def test_ejercicio_7_devuelve_el_entero_si_es_valido(texto, esperado):
    resultado = validar_cantidad(texto)

    assert resultado == esperado and isinstance(resultado, int), (
        f"Con texto={texto!r} se esperaba el entero {esperado!r} "
        f"y se obtuvo {resultado!r}. Una cantidad válida se devuelve como int."
    )


@pytest.mark.parametrize("texto", ["dos", "", "N/D", "NA", "2.5"])
def test_ejercicio_7_rechaza_lo_que_no_es_un_numero_entero(texto):
    with pytest.raises(ValueError, match="La cantidad no es un número entero") as info:
        validar_cantidad(texto)

    assert str(info.value).endswith(f": {texto}"), (
        f"Con texto={texto!r} se esperaba que el mensaje terminara con ': ' "
        f"seguido del texto recibido, y el mensaje fue {str(info.value)!r}."
    )


@pytest.mark.parametrize("texto", ["0", "-4", " -1 "])
def test_ejercicio_7_rechaza_cantidades_menores_o_iguales_a_cero(texto):
    with pytest.raises(ValueError, match="La cantidad debe ser mayor que cero"):
        validar_cantidad(texto)
