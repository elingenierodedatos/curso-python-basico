# Lección 6: Archivos y manejo de errores

Hasta ahora tus datos vivían dentro del código. Los datos reales viven en archivos: alguien exporta los pedidos del mes, tú los lees, los limpias y guardas el resultado. En esta lección aprendes a leer y escribir archivos de texto, CSV y JSON, y a decidir qué hacer cuando algo falla: el archivo no está, o una cantidad dice `"dos"` en lugar de `2`.

**Tiempo estimado:** 120 minutos.
**Antes de empezar:** completa la [lección 5](../leccion_05_funciones_y_modulos/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Armar rutas con `pathlib.Path` que funcionan igual en Windows, macOS y Linux.
- Leer y escribir archivos de texto indicando siempre la codificación.
- Leer los errores `FileNotFoundError` y `ValueError`, y manejarlos con `try-except`.
- Rechazar datos inválidos con `raise` y un mensaje claro.
- Leer y escribir archivos CSV como listas de diccionarios.
- Guardar y cargar datos en JSON, y saber cuándo conviene cada formato.

## Por qué importa en datos

Un flujo de datos casi siempre empieza leyendo un archivo y termina escribiendo otro. En medio, lo que más tiempo consume no es el caso normal, sino lo inesperado: un archivo que no llegó, una fila con un faltante, un acento que se convirtió en `Ã©`.

Hay dos formas de fallar. Un programa que se detiene con un error es molesto, pero honesto: sabes que algo anda mal. Un programa que ignora el problema y sigue adelante entrega un total equivocado sin avisar, y alguien toma decisiones con esa cifra. Aquí aprendes a elegir, en cada caso, entre detenerte, usar un valor por defecto o rechazar el dato, y a que esa elección quede a la vista.

La lógica de `leer_csv` y `escribir_csv` que escribas en esta lección es la entrada y la salida del proyecto final, aunque allí las funciones tengan otros nombres: `leer_pedidos` lee el archivo crudo y `guardar_rechazados` escribe los pedidos que no pasaron la limpieza.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. No los copies y pegues: teclearlos es parte del aprendizaje.
2. Varios ejemplos leen el archivo `datos/pedidos_ejemplo.csv` de esta carpeta. Ábrelo primero en tu editor y míralo: tiene un encabezado, nueve pedidos y varios valores sucios.
3. Para probar los ejemplos crea un archivo `prueba.py` **dentro de esta carpeta** y córrelo con `python lecciones/leccion_06_archivos_y_errores/prueba.py`. En esta lección no uses el intérprete interactivo: la variable `__file__`, que vas a necesitar, solo existe cuando corres un archivo.
4. Corre `python lecciones/leccion_06_archivos_y_errores/ejemplos.py` y cambia valores para ver qué pasa.
5. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno.
6. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

## Conceptos

### 1. Rutas con `pathlib`

Una ruta es la dirección de un archivo o de una carpeta. El problema es que cada sistema la escribe distinto: Windows separa las carpetas con `\` y macOS y Linux con `/`. Un programa que arma la ruta pegando textos funciona en tu computadora y falla en la de tu colega.

Python resuelve esto con `Path`, del módulo `pathlib`. Las partes de la ruta se unen con el operador `/`, y `Path` pone el separador correcto en cada sistema.

```python
from pathlib import Path

ruta = Path("datos") / "pedidos_ejemplo.csv"
print(ruta.name)
print(ruta.parent)
```

```text
pedidos_ejemplo.csv
datos
```

| Qué pides | Qué devuelve | Con `Path("datos") / "pedidos_ejemplo.csv"` |
| --- | --- | --- |
| `ruta.name` | El nombre del archivo, como texto | `'pedidos_ejemplo.csv'` |
| `ruta.parent` | La carpeta que lo contiene, como `Path` | `Path('datos')` |
| `ruta.exists()` | `True` si el archivo o la carpeta existe | Depende de dónde corras el programa |

Dos reglas para todo el curso:

- **Nunca escribas `\` en una ruta.** Además de fallar fuera de Windows, dentro de un texto de Python la diagonal invertida tiene un significado especial: `"datos\nuevos.csv"` contiene un salto de línea, porque `\n` es "línea nueva".
- **Nunca armes una ruta sumando textos**, como `carpeta + "/" + nombre`. Usa `Path` y el operador `/`.

### 2. Rutas relativas, rutas absolutas y `Path(__file__).parent`

Una ruta **absoluta** empieza desde la raíz del disco, por ejemplo `C:\Users\ana\curso\datos` o `/home/ana/curso/datos`. Solo sirve en esa computadora.

Una ruta **relativa**, como `Path("datos") / "pedidos_ejemplo.csv"`, se completa a partir de la carpeta desde donde corres el comando en la terminal. Esa es la trampa: si corres el mismo archivo desde otra carpeta, la ruta apunta a otro lugar y el archivo "desaparece".

La solución es ubicar los datos a partir del propio archivo de código. Python guarda en la variable `__file__` la ruta del archivo que se está ejecutando; su `.parent` es la carpeta donde vive.

```python
from pathlib import Path

carpeta_leccion = Path(__file__).parent
ruta = carpeta_leccion / "datos" / "pedidos_ejemplo.csv"
print(ruta.exists())
```

```text
True
```

Con este truco el programa encuentra el archivo sin importar desde qué carpeta lo corras ni en qué computadora esté.

### 3. Leer un archivo de texto

`read_text()` devuelve el contenido completo del archivo como un solo texto. `splitlines()` lo parte en una lista, con un elemento por línea.

```python
texto = ruta.read_text(encoding="utf-8")
lineas = texto.splitlines()

print(len(lineas))
print(lineas[0])
print(lineas[1])
```

```text
10
id_pedido,fecha,cliente,ciudad,producto,cantidad,precio_unitario,estado
1001,2024-03-01,Ana López,Mérida,Café de olla,2,45.50,entregado
```

Son 10 líneas: el encabezado y nueve pedidos.

Un método pariente es `split()`, que parte un texto usando el separador que le indiques:

```python
campos = lineas[1].split(",")
print(campos)
```

```text
['1001', '2024-03-01', 'Ana López', 'Mérida', 'Café de olla', '2', '45.50', 'entregado']
```

Parece que con esto ya se puede leer un CSV. Más adelante verás por qué no es buena idea y qué usar en su lugar.

### 4. Por qué siempre `encoding="utf-8"`

Un archivo no guarda letras: guarda números. La **codificación** es la tabla que dice qué números representan cada letra. UTF-8 es la más usada hoy y la que usamos en todo el curso. En UTF-8, la `é` ocupa dos números.

Si no indicas la codificación, Python usa la que tenga configurada el sistema operativo, y no es la misma en todos: en muchas instalaciones de Windows es una tabla más antigua llamada `cp1252`. Leer un archivo UTF-8 con la tabla equivocada no produce un error. Produce algo peor: texto dañado.

Provócalo a propósito, leyendo el archivo con la tabla incorrecta:

```python
texto_danado = ruta.read_text(encoding="cp1252")
print(texto_danado.splitlines()[1])
```

```text
1001,2024-03-01,Ana LÃ³pez,MÃ©rida,CafÃ© de olla,2,45.50,entregado
```

Cada letra acentuada se convirtió en dos caracteres extraños. Aprende a reconocer ese patrón: cuando veas `MÃ©rida` o `PeÃ±a`, alguien leyó un archivo UTF-8 con otra codificación. Y fíjate en la consecuencia para los datos: `"MÃ©rida"` y `"Mérida"` son textos distintos, así que al contar pedidos por ciudad aparecerían como dos ciudades.

Por eso la regla no tiene excepciones: **cada vez que leas o escribas un archivo, indica `encoding="utf-8"`**. Así tu programa se comporta igual en cualquier computadora.

### 5. Escribir un archivo de texto

`write_text()` crea el archivo y escribe el texto que le pases.

```python
ruta_nota = Path(__file__).parent / "nota.txt"
ruta_nota.write_text("Primer pedido: Café de olla\n", encoding="utf-8")
ruta_nota.write_text("Segundo pedido: Taza de barro\n", encoding="utf-8")
print(ruta_nota.read_text(encoding="utf-8"))
```

```text
Segundo pedido: Taza de barro
```

El primer pedido ya no está. **`write_text()` sobrescribe sin avisar:** si el archivo existía, su contenido anterior se pierde, sin pregunta y sin papelera. Antes de escribir, revisa a qué ruta apuntas. Nunca escribas sobre tus datos originales: guarda los resultados en otro archivo. (Borra `nota.txt` cuando termines de probar.)

Para escribir dentro de una carpeta que tal vez no existe, créala primero:

```python
carpeta_salida = Path(__file__).parent / "salida" / "marzo"
carpeta_salida.mkdir(parents=True, exist_ok=True)
```

- `parents=True` crea también las carpetas intermedias (aquí, `salida`).
- `exist_ok=True` evita un error si la carpeta ya existía.

Con esos dos argumentos puedes llamar a `mkdir` siempre, exista o no la carpeta.

### 6. Todo lo que se lee es texto

En un archivo de texto no hay números: hay caracteres. La cantidad del primer pedido llega como `"2"`, no como `2`.

```python
cantidad = campos[5]
print(cantidad * 2)
print(int(cantidad) * 2)
```

```text
22
4
```

El primer resultado no es un error, y por eso es peligroso: Python repitió el texto `"2"` dos veces. Antes de hacer cuentas con un dato leído de un archivo, conviértelo con `int()` o `float()`, como en la lección 1.

### 7. Provoca los dos errores de esta lección

A los errores que ocurren mientras el programa corre, Python los llama **excepciones**. Cuando ocurre una y nadie la atiende, el programa se detiene y muestra el *traceback* que ya sabes leer de abajo hacia arriba.

**Primer error: el archivo no existe.**

```python
from pathlib import Path

ruta = Path("datos") / "no_existe.csv"
texto = ruta.read_text(encoding="utf-8")
```

```text
Traceback (most recent call last):
  File "prueba.py", line 4, in <module>
    texto = ruta.read_text(encoding="utf-8")
  ...
FileNotFoundError: [Errno 2] No such file or directory: 'datos/no_existe.csv'
```

- **Última línea:** `FileNotFoundError`, "archivo no encontrado", seguido de la ruta que Python buscó. En Windows la verás con el separador de ese sistema. Compara siempre esa ruta con la que tú creías estar usando: casi siempre el problema es una ruta relativa o un nombre mal escrito.
- **En medio** aparecen varias líneas de archivos que no son tuyos (`pathlib`). Es el código interno de Python. Sáltalas y busca la línea que menciona **tu** archivo: ahí está la instrucción que falló.

**Segundo error: el contenido no sirve.**

```python
cantidad = int("dos")
```

```text
Traceback (most recent call last):
  File "prueba.py", line 1, in <module>
    cantidad = int("dos")
ValueError: invalid literal for int() with base 10: 'dos'
```

Es el mismo `ValueError` de la lección 1: el tipo es correcto (es un texto), pero su contenido no se puede convertir. El mensaje termina mostrando el valor culpable, `'dos'`.

### 8. `try-except`: decidir qué hacer cuando algo falla

Con `try-except` le dices a Python: "intenta esto; si ocurre este error en particular, haz esto otro en lugar de detenerte".

```python
for cantidad_cruda in ["3", "dos", "N/D"]:
    try:
        cantidad = int(cantidad_cruda)
    except ValueError:
        print(f"'{cantidad_cruda}' no es un número entero")
    else:
        print(f"'{cantidad_cruda}' se convirtió en el número {cantidad}")
```

```text
'3' se convirtió en el número 3
'dos' no es un número entero
'N/D' no es un número entero
```

Cada bloque tiene su papel:

| Bloque | Cuándo se ejecuta | Qué va ahí |
| --- | --- | --- |
| `try:` | Siempre | Solo la instrucción que puede fallar |
| `except ValueError:` | Si dentro del `try` ocurrió un `ValueError` | Lo que haces ante ese error |
| `else:` | Si el `try` terminó sin error | Lo que depende de que todo haya salido bien |

El `else` es opcional. Sirve para dejar dentro del `try` únicamente la línea riesgosa, y así saber con certeza qué error estás atendiendo.

Lo mismo funciona con un archivo que puede no estar:

```python
ruta = Path(__file__).parent / "datos" / "no_existe.csv"

try:
    texto = ruta.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"No se encontró el archivo: {ruta.name}")
```

```text
No se encontró el archivo: no_existe.csv
```

#### Atrapa solo el error que esperas

Python permite escribir `except:` sin nombre de error, y eso atrapa **cualquier** cosa. No lo hagas nunca. Mira lo que pasa al sumar las piezas de los nueve pedidos del archivo de ejemplo (en la sección 11 verás cómo se cargan en la lista `pedidos`), con un error de dedo en el nombre de la columna:

```python
total = 0
for pedido in pedidos:
    try:
        total += int(pedido["cantida"])
    except:
        pass

print(total)
```

```text
0
```

`pass` significa "no hagas nada". La clave `"cantida"` no existe, así que las nueve filas fallaron con `KeyError`; el `except:` vacío se tragó los nueve errores y el programa entregó `0` con toda tranquilidad. Si ese número va a un reporte, nadie se entera de que está mal.

Con `except ValueError:` el resultado es distinto: el `KeyError` no es el error esperado, nadie lo atrapa, y el programa se detiene señalando la línea exacta:

```text
KeyError: 'cantida'
```

Ese error es una buena noticia: lo ves, lo corriges en un minuto y sigues.

Aun atrapando el error correcto, **callar no es manejar**. Si una fila no se puede usar, que quede registro:

```python
total = 0
rechazados = []
for pedido in pedidos:
    try:
        cantidad = int(pedido["cantidad"])
    except ValueError:
        rechazados.append(pedido["id_pedido"])
    else:
        total += cantidad

print(total)
print(rechazados)
```

```text
18
['1005', '1007']
```

Ahora el total viene acompañado de su letra pequeña: 18 piezas, sin contar dos pedidos cuya cantidad no se pudo leer. Quien reciba la cifra sabe qué tan completa está.

### 9. `raise`: rechazar un dato inválido

A veces el dato sí se puede convertir, pero no tiene sentido: una cantidad de `-4` piezas, un precio negativo. Python no lo va a notar; te toca a ti. Con `raise` lanzas tu propia excepción, con un mensaje que explique el problema.

```python
def validar_precio(precio):
    if precio < 0:
        raise ValueError(f"El precio no puede ser negativo: {precio}")
    return precio


print(validar_precio(45.5))
print(validar_precio(-45.5))
```

```text
45.5
Traceback (most recent call last):
  File "prueba.py", line 8, in <module>
    print(validar_precio(-45.5))
  File "prueba.py", line 3, in validar_precio
    raise ValueError(f"El precio no puede ser negativo: {precio}")
ValueError: El precio no puede ser negativo: -45.5
```

Al llegar a `raise`, la función termina en ese punto: el `return` ya no se ejecuta. Quien llamó a la función decide si atrapa el error con `try-except` o deja que el programa se detenga.

Un buen mensaje de error dice **qué** está mal e incluye **el valor** que lo causó. "Dato inválido" no ayuda a nadie; "El precio no puede ser negativo: -45.5" se corrige solo.

#### Cambiar un error por otro más claro

El mensaje `invalid literal for int() with base 10: 'dos'` es exacto, pero no dice que hablamos de la cantidad de un pedido. Puedes atrapar el error original y lanzar uno con mejor mensaje:

```python
def leer_precio(texto):
    try:
        precio = float(texto)
    except ValueError as error:
        raise ValueError(f"El precio no es un número: {texto}") from error
    return precio


leer_precio("N/D")
```

```text
ValueError: El precio no es un número: N/D
```

Dos piezas nuevas:

- `except ValueError as error` guarda la excepción atrapada en la variable `error`, por si la necesitas.
- `raise ... from error` lanza el error nuevo y le deja anotado cuál fue el original. En el *traceback* aparecen los dos, unidos por la frase `The above exception was the direct cause of the following exception`. Así no se pierde información.

### 10. `with`: abrir un archivo y asegurar que se cierre

`read_text()` y `write_text()` abren el archivo, hacen su trabajo y lo cierran. Para leer o escribir fila por fila necesitas mantenerlo abierto un rato, y eso se hace con `ruta.open()` dentro de un bloque `with`:

```python
with ruta.open(encoding="utf-8") as archivo:
    primera_linea = archivo.readline()

print(primera_linea.strip())
```

```text
id_pedido,fecha,cliente,ciudad,producto,cantidad,precio_unitario,estado
```

Se lee: "abre la ruta, llama `archivo` a lo abierto y, al terminar el bloque, ciérralo". El cierre ocurre siempre, incluso si dentro del bloque hay un error. Un archivo que se queda abierto puede quedar a medio escribir o bloqueado para otros programas; con `with` no tienes que acordarte de cerrarlo.

Para escribir, el primer argumento de `open` es `"w"` (de *write*). Igual que `write_text()`, sobrescribe sin avisar.

### 11. CSV con el módulo `csv`

Un archivo CSV es una tabla en texto: una línea por fila, columnas separadas por comas y, casi siempre, una primera línea con los nombres de las columnas.

¿Por qué no leerlo con `split(",")`? Mira el segundo pedido del archivo:

```python
print(lineas[2].split(","))
```

```text
['1002', '2024-03-01', '  josé pérez ', 'GUADALAJARA', 'Molinillo manual', '1', '"$1', '250.50"', 'enviado']
```

El precio `"$1,250.50"` trae una coma, y `split` lo partió en dos: la fila quedó con nueve columnas en lugar de ocho. El formato CSV resuelve ese caso encerrando el valor entre comillas, y el módulo `csv` de la biblioteca estándar conoce esa regla y varias más. Úsalo siempre.

#### Leer: `csv.DictReader`

```python
import csv
from pathlib import Path

ruta = Path(__file__).parent / "datos" / "pedidos_ejemplo.csv"

pedidos = []
with ruta.open(encoding="utf-8", newline="") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        pedidos.append(fila)

print(len(pedidos))
print(pedidos[0])
print(pedidos[1]["precio_unitario"])
```

```text
9
{'id_pedido': '1001', 'fecha': '2024-03-01', 'cliente': 'Ana López', 'ciudad': 'Mérida', 'producto': 'Café de olla', 'cantidad': '2', 'precio_unitario': '45.50', 'estado': 'entregado'}
$1,250.50
```

- `DictReader` toma la primera línea como encabezado y entrega cada fila como un **diccionario**: las claves son los nombres de las columnas. El resultado es la lista de diccionarios que conoces desde la lección 4.
- **Todos los valores son texto**, también `'2'` y `'45.50'`. Convertirlos es tu trabajo.
- Un valor faltante llega como texto vacío: `pedidos[5]["ciudad"]` es `''`.
- El lector solo funciona mientras el archivo está abierto. Por eso las filas se guardan en una lista **dentro** del `with`, y la lista se usa después.

#### Por qué `newline=""`

Windows marca el fin de línea con dos caracteres y macOS y Linux con uno. Al abrir un archivo de texto, Python traduce esos finales de línea por su cuenta, y el módulo `csv` también los maneja por la suya. Si los dos lo hacen a la vez, al escribir en Windows cada fila termina con un fin de línea de más y el archivo queda con **una línea en blanco entre fila y fila**. `newline=""` le dice a Python que no traduzca y deje ese trabajo al módulo `csv`.

La regla práctica: **con el módulo `csv`, abre siempre el archivo con `encoding="utf-8", newline=""`**, tanto para leer como para escribir.

#### Escribir: `csv.DictWriter`

```python
filas = [
    {"id_pedido": "1001", "cliente": "Ana López", "ciudad": "Mérida"},
    {"id_pedido": "1007", "cliente": "Ana López", "ciudad": "Mérida"},
]
columnas = ["id_pedido", "cliente", "ciudad"]
ruta_salida = Path(__file__).parent / "salida" / "pedidos_merida.csv"
ruta_salida.parent.mkdir(parents=True, exist_ok=True)

with ruta_salida.open("w", encoding="utf-8", newline="") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(filas)

print(ruta_salida.read_text(encoding="utf-8"))
```

```text
id_pedido,cliente,ciudad
1001,Ana López,Mérida
1007,Ana López,Mérida
```

- `fieldnames` es la lista de columnas, y define su **orden** en el archivo.
- `writeheader()` escribe la línea del encabezado.
- `writerows(filas)` escribe todas las filas de la lista. Para escribir una sola existe `writerow(fila)`.

(Borra la carpeta `salida` cuando termines de probar. En `ejemplos.py` verás cómo escribir en una carpeta temporal que se borra sola.)

### 12. JSON

JSON es un formato de texto para guardar estructuras: diccionarios, listas, textos, números, `true`/`false` y `null`, anidados como haga falta. Se parece tanto a los diccionarios y listas de Python que la conversión es directa. El módulo `json` trabaja con dos funciones:

| Función | Qué hace |
| --- | --- |
| `json.dumps(datos)` | Convierte datos de Python en un texto JSON |
| `json.loads(texto)` | Convierte un texto JSON en datos de Python |

```python
import json

resumen = {
    "ciudad": "Mérida",
    "pedidos": 2,
    "productos": ["Café de olla", "Taza de barro"],
}

print(json.dumps(resumen))
```

```text
{"ciudad": "M\u00e9rida", "pedidos": 2, "productos": ["Caf\u00e9 de olla", "Taza de barro"]}
```

Funciona, pero es incómodo de leer: todo en una línea y los acentos convertidos en códigos como `\u00e9`. Dos argumentos lo arreglan:

```python
texto = json.dumps(resumen, ensure_ascii=False, indent=2)
print(texto)
```

```text
{
  "ciudad": "Mérida",
  "pedidos": 2,
  "productos": [
    "Café de olla",
    "Taza de barro"
  ]
}
```

- `ensure_ascii=False` deja los acentos y la ñ tal cual.
- `indent=2` pone cada dato en su línea, con sangría de 2 espacios por nivel.

`dumps` solo produce el texto. Para guardarlo y recuperarlo usas lo que ya sabes:

```python
ruta_json = Path(__file__).parent / "salida" / "resumen.json"
ruta_json.write_text(texto, encoding="utf-8")

datos = json.loads(ruta_json.read_text(encoding="utf-8"))
print(datos["productos"][0])
print(type(datos["pedidos"]))
```

```text
Café de olla
<class 'int'>
```

A diferencia de CSV, JSON sí distingue números de textos: `2` regresa como `int`.

Si el texto no es JSON válido, `json.loads` lanza `json.JSONDecodeError`. Por ejemplo, JSON exige comillas dobles:

```python
json.loads("{'ciudad': 'Mérida'}")
```

```text
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

`JSONDecodeError` es un tipo particular de `ValueError`: un `except ValueError:` también lo atrapa.

### 13. ¿CSV o JSON?

| | CSV | JSON |
| --- | --- | --- |
| Forma de los datos | Una tabla: todas las filas con las mismas columnas | Estructuras anidadas: diccionarios con listas y otros diccionarios |
| Tipos | Todo es texto | Distingue texto, números, verdadero/falso y vacío |
| Se abre en una hoja de cálculo | Sí | No |
| Uso típico | Pedidos, clientes, cualquier listado grande | Resúmenes, reportes, configuración |

La regla corta: **si cabe en una tabla, CSV; si tiene niveles, JSON.** En el proyecto final los pedidos limpios se guardan en CSV y el reporte de calidad, que tiene totales, listas y conteos por ciudad, en JSON.

## Ejercicios

Abre `ejercicios.py`. Cada función tiene un docstring con lo que debe hacer y un ejemplo. Borra la línea `raise NotImplementedError(...)` y escribe tu código. Los módulos `csv`, `json` y `Path` ya están importados al inicio del archivo.

Tres recordatorios para todos los ejercicios:

- Las funciones que reciben una ruta deben aceptar un `Path` o un texto. Empieza cada una con `ruta = Path(ruta)`: si ya era un `Path`, queda igual; si era texto, se convierte.
- Indica `encoding="utf-8"` cada vez que leas o escribas. Las pruebas usan archivos con acentos y ñ.
- La función debe **devolver** el resultado con `return`. Usar `print()` no cuenta.

Las pruebas crean sus propios archivos en una carpeta temporal; no tocan tu repositorio. Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_06_archivos_y_errores -k ejercicio_1
```

### Ejercicio 1. `contar_lineas(ruta)`

Devuelve cuántas líneas no vacías tiene un archivo de texto. Una línea que solo tiene espacios cuenta como vacía. Es la primera revisión que se le hace a un archivo recién llegado: ¿trae lo que esperaba?

| Contenido del archivo | Resultado |
| --- | --- |
| `"Mérida\nPuebla\nTijuana\n"` | `3` |
| `"Mérida\n\nPuebla\n   \n"` | `2` |
| `""` (archivo vacío) | `0` |

Paso a paso:

1. Convierte la ruta con `Path(ruta)` y lee el contenido completo del archivo.
2. Parte el texto en una lista de líneas.
3. Recorre las líneas con un acumulador que cuente solo las que tienen algo además de espacios.
4. Devuelve el contador.

<details>
<summary>Pista 1</summary>

Los pasos 1 y 2 están resueltos en la sección "Leer un archivo de texto". El paso 3 es el patrón de acumulador de la lección 2.

</details>

<details>
<summary>Pista 2</summary>

¿Cómo saber si una línea solo tiene espacios? Piensa en qué queda de ella después de aplicarle el método de la lección 1 que quita los espacios de los extremos.

</details>

### Ejercicio 2. `a_entero(texto, por_defecto=0)`

Convierte un texto en entero. Si no se puede, devuelve el valor por defecto en lugar de detener el programa.

| Entrada | Resultado |
| --- | --- |
| `a_entero("12")` | `12` |
| `a_entero("N/D")` | `0` |
| `a_entero("dos", por_defecto=-1)` | `-1` |
| `a_entero("7", por_defecto=-1)` | `7` |

Paso a paso:

1. Intenta convertir el texto con `int()`.
2. Si ocurre un `ValueError`, devuelve `por_defecto`.
3. Si no ocurre, devuelve el entero.

<details>
<summary>Pista 1</summary>

Es la estructura `try-except` de la sección 8, con un `return` en lugar de cada `print()`.

</details>

<details>
<summary>Pista 2</summary>

Si alguna prueba recibe siempre `0`, revisa que devuelvas el parámetro `por_defecto` y no un cero fijo.

</details>

> Una advertencia de oficio: un valor por defecto es una decisión, no un truco para que nada falle. Convertir `"N/D"` en `0` piezas cambia los totales. Úsalo cuando el cero tenga sentido para tu análisis; cuando no, rechaza el dato, como harás en el ejercicio 7.

### Ejercicio 3. `leer_csv(ruta)`

Lee un archivo CSV y devuelve una lista de diccionarios, uno por fila. Si el archivo no existe, lanza `FileNotFoundError` con un mensaje en español que incluya la ruta.

Con un archivo que contiene:

```text
id_pedido,ciudad,cantidad
1001,Mérida,2
1002,Tijuana,N/D
```

| Entrada | Resultado |
| --- | --- |
| `leer_csv(ruta)` | `[{'id_pedido': '1001', 'ciudad': 'Mérida', 'cantidad': '2'}, {'id_pedido': '1002', 'ciudad': 'Tijuana', 'cantidad': 'N/D'}]` |
| `leer_csv(Path("no_existe.csv"))` | `FileNotFoundError: No se encontró el archivo: no_existe.csv` |
| Archivo con solo el encabezado | `[]` |

Paso a paso:

1. Convierte la ruta con `Path(ruta)`.
2. Si el archivo no existe, lanza `FileNotFoundError` con el mensaje `No se encontró el archivo: ` seguido de la ruta.
3. Crea una lista vacía.
4. Abre el archivo con `with`, con la codificación y el `newline` que pide el módulo `csv`.
5. Crea el lector y agrega cada fila a la lista.
6. Devuelve la lista. No conviertas los valores: se quedan como texto.

<details>
<summary>Pista 1</summary>

Para el paso 2 necesitas dos cosas que ya viste: el método de `Path` que dice si algo existe, y `raise` con un f-string como mensaje. `FileNotFoundError` se lanza igual que `ValueError`.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba se queja de que devolviste algo que no es una lista, o aparece `ValueError: I/O operation on closed file`, estás usando el lector después de que el `with` cerró el archivo. Llena la lista dentro del bloque.

</details>

### Ejercicio 4. `escribir_csv(ruta, filas, columnas)`

Escribe una lista de diccionarios en un archivo CSV: primero el encabezado y luego las filas, con las columnas en el orden indicado. Crea la carpeta de destino si no existe y devuelve el número de filas escritas.

Con `filas = [{"id_pedido": "1001", "ciudad": "Mérida"}, {"id_pedido": "1002", "ciudad": "Tijuana"}]`:

| Entrada | Resultado | Contenido del archivo |
| --- | --- | --- |
| `escribir_csv(ruta, filas, ["id_pedido", "ciudad"])` | `2` | `id_pedido,ciudad` / `1001,Mérida` / `1002,Tijuana` |
| `escribir_csv(ruta, filas, ["ciudad", "id_pedido"])` | `2` | `ciudad,id_pedido` / `Mérida,1001` / `Tijuana,1002` |
| `escribir_csv(ruta, [], ["id_pedido", "ciudad"])` | `0` | `id_pedido,ciudad` |

Paso a paso:

1. Convierte la ruta con `Path(ruta)`.
2. Crea la carpeta que contiene al archivo, de modo que no falle si ya existe ni si faltan carpetas intermedias.
3. Abre el archivo para escritura con `with`, con la codificación y el `newline` que pide el módulo `csv`.
4. Crea el escritor con las columnas recibidas, escribe el encabezado y luego las filas.
5. Devuelve cuántas filas escribiste.

<details>
<summary>Pista 1</summary>

La carpeta que contiene al archivo es `ruta.parent`. Los dos argumentos de `mkdir` que necesitas están en la sección 5.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba de las líneas en blanco falla en tu computadora, revisa los argumentos de `open`. Si falla la del orden de columnas, revisa qué lista le pasaste al escritor.

</details>

<details>
<summary>Pista 3</summary>

El número de filas escritas es el tamaño de la lista que recibiste. No hace falta contarlas una por una.

</details>

### Ejercicio 5. `guardar_json(ruta, datos)`

Guarda datos en un archivo JSON, con sangría de 2 espacios y sin escapar los acentos. No devuelve nada.

| Entrada | Resultado |
| --- | --- |
| `guardar_json(ruta, {"pais": "México", "pedidos": 9})` | `None`, y el archivo queda como se muestra abajo |
| `guardar_json(ruta, ["Café de olla", "Taza de barro"])` | `None`, y el archivo contiene la lista, un producto por línea |

Con el primer ejemplo, el archivo debe verse exactamente así:

```text
{
  "pais": "México",
  "pedidos": 9
}
```

Paso a paso:

1. Convierte los datos en un texto JSON, con los dos argumentos que lo hacen legible.
2. Escribe ese texto en la ruta, en UTF-8.

<details>
<summary>Pista 1</summary>

Son dos líneas, y las dos están en la sección 12. Recuerda convertir la ruta con `Path()`, porque un texto no tiene el método para escribir.

</details>

<details>
<summary>Pista 2</summary>

Si el archivo dice `M\u00e9xico`, te falta uno de los dos argumentos de `json.dumps`.

</details>

### Ejercicio 6. `leer_json(ruta)`

Lee un archivo JSON y devuelve los datos. Si el contenido no es JSON válido, lanza `ValueError` con un mensaje en español que incluya la ruta.

| Contenido del archivo | Resultado |
| --- | --- |
| `{"pais": "México", "pedidos": 9}` | `{'pais': 'México', 'pedidos': 9}` |
| `esto no es JSON` | `ValueError: El archivo no contiene JSON válido: roto.json` |
| El archivo no existe | `FileNotFoundError` (el de Python, sin cambios) |

Paso a paso:

1. Convierte la ruta con `Path(ruta)` y lee el texto del archivo.
2. Intenta convertir el texto con `json.loads`.
3. Si ocurre un `json.JSONDecodeError`, lanza un `ValueError` con el mensaje `El archivo no contiene JSON válido: ` seguido de la ruta, conservando el error original.
4. Devuelve los datos.

<details>
<summary>Pista 1</summary>

Es el patrón "cambiar un error por otro más claro" de la sección 9: `except ... as error` y `raise ... from error`.

</details>

<details>
<summary>Pista 2</summary>

Deja la lectura del archivo fuera del `try`. Así, si el archivo no existe, el `FileNotFoundError` sale tal cual y no se confunde con un problema de contenido.

</details>

### Ejercicio 7. `validar_cantidad(texto)`

Convierte la cantidad de un pedido en entero y rechaza las que no sirven. A diferencia de `a_entero`, esta función no disimula: si el dato es inválido, lanza un error que explica por qué.

| Entrada | Resultado |
| --- | --- |
| `validar_cantidad("3")` | `3` |
| `validar_cantidad(" 10 ")` | `10` |
| `validar_cantidad("dos")` | `ValueError: La cantidad no es un número entero: dos` |
| `validar_cantidad("2.5")` | `ValueError: La cantidad no es un número entero: 2.5` |
| `validar_cantidad("0")` | `ValueError: La cantidad debe ser mayor que cero: 0` |
| `validar_cantidad("-4")` | `ValueError: La cantidad debe ser mayor que cero: -4` |

Paso a paso:

1. Intenta convertir el texto con `int()`.
2. Si ocurre un `ValueError`, lanza otro con el mensaje `La cantidad no es un número entero: ` seguido del texto recibido.
3. Si el entero es menor o igual a cero, lanza un `ValueError` con el mensaje `La cantidad debe ser mayor que cero: ` seguido de la cantidad.
4. Devuelve el entero.

<details>
<summary>Pista 1</summary>

Hay dos motivos de rechazo y cada uno usa una herramienta distinta: el primero es el patrón de la sección 9 para cambiar un error por otro; el segundo es un `if` con `raise`, como en `validar_precio`.

</details>

<details>
<summary>Pista 2</summary>

La revisión de "mayor que cero" va después del `try-except`, no adentro. Dentro del `try` deja solo la conversión.

</details>

## Evalúate

Cuando termines los siete ejercicios, corre la lección completa:

```bash
pytest lecciones/leccion_06_archivos_y_errores
```

Debes ver `63 passed`. Si una prueba falla, lee la línea que empieza con `E`: te dice con qué valores se probó, qué se esperaba y qué devolvió tu función.

Revisa también el estilo de tu código:

```bash
ruff check lecciones/leccion_06_archivos_y_errores
```

Antes de guardar, borra los archivos que hayas creado al practicar (`prueba.py`, `nota.txt`, la carpeta `salida`). Después:

```bash
git add .
git commit -m "Completa la lección 6"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Por qué se arma una ruta con `Path` y `/` en lugar de sumar textos?
2. ¿Qué problema resuelve `Path(__file__).parent`?
3. Abres un archivo y ves `MÃ©rida`. ¿Qué pasó y cómo se evita?
4. ¿Qué le pasa al contenido anterior de un archivo cuando usas `write_text()`?
5. ¿Qué diferencia hay entre `except ValueError:` y `except:` sin nombre, y por qué el segundo es peligroso al calcular un total?
6. ¿De qué tipo son los valores que entrega `csv.DictReader`? ¿Y para qué sirve `newline=""`?
7. De la lección 4: ¿qué devuelve `pedido.get("ciudad")` si la clave no existe, y qué pasa con `pedido["ciudad"]` en el mismo caso?
8. De la lección 5: ¿qué significa que un parámetro tenga valor por defecto, como en `a_entero(texto, por_defecto=0)`?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. Casi siempre trae la respuesta.
2. Si el error es `FileNotFoundError`, imprime la ruta con `print(ruta)` y `print(ruta.exists())` antes de la línea que falla, y compárala con lo que ves en tu explorador de archivos.
3. Prueba tu función a mano en un archivo `prueba.py`, con el archivo de ejemplo de la carpeta `datos`.
4. Revisa los ejemplos resueltos de `ejemplos.py`.
5. Abre las pistas del ejercicio, una a la vez.
6. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 10, "Files and Exceptions": `pathlib` con `read_text` y `write_text`, `try-except-else`, `FileNotFoundError` y guardar datos en JSON.
- Bill Lubanovic, *Introducing Python*, capítulo 8, "Data Has to Go Somewhere": archivos de texto, CSV y JSON.
- Reuven Lerner, *Python Workout*, 2.ª ed., capítulo 6, "Files": ejercicios de lectura y escritura de archivos.
- Felienne Hermans, *The Programmer's Brain*, capítulo 3, "How to learn programming syntax quickly": por qué intentar recordar antes de buscar y por qué conviene repasar espaciado.
