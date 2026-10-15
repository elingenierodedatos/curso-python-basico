# Lección 7: Pruebas con pytest

Llevas seis lecciones corriendo pruebas que escribimos nosotros y leyendo sus fallos. En esta lección cambias de lado: las pruebas las escribes tú, y nosotros evaluamos qué tan bien cuidan el código.

**Tiempo estimado:** 140 minutos.
**Antes de empezar:** completa la [lección 6](../leccion_06_archivos_y_errores/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Explicar qué es una prueba unitaria y cómo las encuentra pytest.
- Escribir pruebas con `assert`, con la estructura preparar, actuar, comprobar.
- Leer una prueba fallida línea por línea y decidir qué se arregla: el código o la prueba.
- Probar errores esperados con `pytest.raises` y muchos casos con `parametrize`.
- Elegir qué casos probar: el normal, los límites, lo vacío y lo inválido.
- Usar las opciones de pytest que más ahorran tiempo y entender la configuración de este repositorio.

## Por qué importa en datos

En datos, un error casi nunca avisa. Un programa que se detiene con un mensaje rojo es el caso fácil: alguien lo ve y lo arregla. El caso difícil es el que termina sin quejarse y entrega una cifra equivocada: un precio que perdió los centavos, un pedido de 500 pesos clasificado en la categoría que no le toca, una ciudad contada dos veces porque llegó escrita de dos formas. Esa cifra acaba en un reporte y alguien decide con ella.

Las pruebas son la red de seguridad contra ese tipo de error. Fijan por escrito qué debe devolver cada función, y lo vuelven a revisar cada vez que cambias algo. Saber escribirlas es lo que separa un script que funcionó una vez de un trabajo de ingeniería que otros pueden usar con confianza.

En el proyecto final vas a escribir las pruebas de tu propio flujo de datos con lo que practiques aquí.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. En esta lección los escribes dentro de `test_mis_pruebas.py`, tu propio archivo de pruebas, que irá creciendo.
2. Corre `python lecciones/leccion_07_pruebas/ejemplos.py` para ver las piezas sueltas, y `pytest lecciones/leccion_07_pruebas/ejemplos_de_pruebas.py -v` para ver un archivo de pruebas completo.
3. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno.
4. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

Los archivos de la carpeta tienen papeles distintos:

| Archivo | Qué es | ¿Lo editas? |
| --- | --- | --- |
| `funciones.py` | Cuatro funciones del negocio, ya resueltas y correctas | No, salvo en el concepto 3 |
| `ejercicios.py` | El calentamiento del ejercicio 0 y las comprobaciones de los ejercicios 1 a 5 | Sí |
| `test_mis_pruebas.py` | Tu archivo de pruebas, ejercicio 6 | Sí |
| `test_ejercicios.py` | Nuestras pruebas, que evalúan las tuyas | No |
| `ejemplos.py`, `ejemplos_de_pruebas.py` | Ejemplos resueltos | Si quieres experimentar |

Antes de seguir, abre `funciones.py` y lee los cuatro docstrings. Son las funciones que vas a cuidar: `limpiar_precio`, `clasificar_importe`, `validar_cantidad` y `contar_por_ciudad`.

## Conceptos

### 0. Antes de empezar: las funciones también son valores

En esta lección vas a escribir funciones que reciben otra función como argumento. Para eso hace falta una idea que en la lección 5 no necesitabas: el nombre de una función, **sin paréntesis**, se refiere a la función misma. Con paréntesis, la llama.

| Escribes | Qué es |
| --- | --- |
| `limpiar_precio("$45")` | El resultado de llamar a la función: un número. |
| `limpiar_precio` | La función, sin ejecutarla. |

Como es un valor, una función se puede guardar en una variable y se puede enviar como argumento a otra función, que decide cuándo llamarla:

```python
from lecciones.leccion_07_pruebas.funciones import limpiar_precio


def mostrar_de_cada_uno(textos, funcion):
    """Imprime el resultado de llamar funcion(texto) con cada texto."""
    for texto in textos:
        print(funcion(texto))


mostrar_de_cada_uno(["$45", " 1,250.50 "], limpiar_precio)
```

```text
45.0
1250.5
```

Dentro de `mostrar_de_cada_uno`, el parámetro `funcion` es un nombre más para `limpiar_precio`, y `funcion(texto)` la llama. El mismo bucle sirve para cualquier función que reciba un texto. En `ejemplos.py` hay otro caso, `funcion_elegida = calcular_total`, y las comprobaciones de los ejercicios 1 a 5 se apoyan en esta misma idea: reciben la función que deben revisar. El ejercicio 0 es un calentamiento para practicarla antes de escribir pruebas.

### 1. Qué es una prueba unitaria

Una prueba unitaria es una función pequeña que llama a otra función con una entrada conocida y comprueba que el resultado sea el esperado. "Unitaria" porque revisa una sola unidad de código, normalmente una función, y un solo comportamiento a la vez.

pytest no necesita que le digas dónde están tus pruebas. Las encuentra por su nombre, con dos convenciones:

- Busca **archivos** cuyo nombre empiece con `test_`, como `test_mis_pruebas.py`.
- Dentro de ellos, toma como prueba cada **función** cuyo nombre empiece con `test_`.

A esto se le llama descubrimiento. Si un archivo se llama `pruebas.py`, o una función se llama `prueba_precio`, pytest pasa de largo sin avisar. Es el primer lugar donde mirar cuando una prueba "no corre".

### 2. Tu primera prueba

Abre `test_mis_pruebas.py`. Ya trae los imports. Debajo de la última línea escribe:

```python
def test_clasificar_importe_de_500_exactos_es_medio():
    importe = 500

    categoria = clasificar_importe(importe)

    assert categoria == "medio"
```

Córrela:

```bash
pytest lecciones/leccion_07_pruebas/test_mis_pruebas.py
```

```text
lecciones/leccion_07_pruebas/test_mis_pruebas.py .                       [100%]

============================== 1 passed in 0.02s ===============================
```

Tres ideas caben en esas cinco líneas.

**`assert` comprueba una condición.** Si la condición es verdadera, no pasa nada y la prueba sigue. Si es falsa, Python lanza un `AssertionError` y pytest marca la prueba como fallida. Una prueba pasa cuando llega al final sin que nada falle.

**La prueba tiene tres partes**, separadas por líneas en blanco:

| Parte | Qué hace | En el ejemplo |
| --- | --- | --- |
| Preparar | Deja listos los datos de entrada | `importe = 500` |
| Actuar | Llama a la función que se prueba, una sola vez | `categoria = clasificar_importe(importe)` |
| Comprobar | Compara el resultado con lo esperado | `assert categoria == "medio"` |

Brian Okken las llama *Given, When, Then*: dado esto, cuando pasa esto, entonces espero esto. Si una prueba tuya no se deja dividir así, casi siempre es porque intenta comprobar dos cosas y conviene partirla en dos pruebas.

**El nombre es largo a propósito.** Cuando una prueba falla, lo primero que lees es su nombre. `test_clasificar_importe_de_500_exactos_es_medio` te dice qué se rompió sin abrir el archivo; `test_1` o `test_clasificar` no. Un buen nombre dice qué función se prueba, en qué situación y qué se espera. Nadie llama a estas funciones a mano, así que el largo no estorba.

### 3. Provoca el error: una prueba que falla, leída con calma

Una prueba que nunca has visto fallar todavía no te ha demostrado nada. Vas a romper el código a propósito para ver cómo responde.

Abre `funciones.py`, busca `clasificar_importe` y cambia `<` por `<=` en el primer `if`:

```python
    if importe <= 500:
        return "bajo"
```

Es un error muy creíble: un solo carácter, y solo afecta a los pedidos de 500 pesos exactos. Ningún mensaje rojo lo delataría en producción. Corre tu prueba otra vez:

```text
lecciones/leccion_07_pruebas/test_mis_pruebas.py F                       [100%]

=================================== FAILURES ===================================
_______________ test_clasificar_importe_de_500_exactos_es_medio ________________
lecciones/leccion_07_pruebas/test_mis_pruebas.py:40: in test_clasificar_importe_de_500_exactos_es_medio
    assert categoria == "medio"
E   AssertionError: assert 'bajo' == 'medio'
E     
E     - medio
E     + bajo
=========================== short test summary info ============================
FAILED lecciones/leccion_07_pruebas/test_mis_pruebas.py::test_clasificar_importe_de_500_exactos_es_medio
============================== 1 failed in 0.03s ===============================
```

El número de renglón puede ser otro en tu archivo. Léelo por partes, sin prisa:

1. **La `F`** en la primera línea. Cada prueba deja una marca: `.` si pasó, `F` si falló.
2. **El título entre guiones bajos.** Es el nombre de la prueba que falló. Aquí el nombre largo ya paga: sabes que el problema está en los 500 exactos.
3. **La línea con archivo y número.** `test_mis_pruebas.py:40` es el renglón del `assert` que no se cumplió, y debajo está el código de ese renglón.
4. **Las líneas `E`.** Son el motivo. `assert 'bajo' == 'medio'` muestra a la izquierda lo que devolvió la función y a la derecha lo que esperabas. Cuando son textos, pytest agrega la comparación: con `-` lo esperado y con `+` lo obtenido.
5. **El resumen final.** Una línea `FAILED` por cada prueba fallida y el conteo total.

Este repositorio muestra los fallos en formato corto. Pide el formato largo para ver la prueba completa:

```bash
pytest lecciones/leccion_07_pruebas/test_mis_pruebas.py --tb=long
```

```text
    def test_clasificar_importe_de_500_exactos_es_medio():
        importe = 500
    
        categoria = clasificar_importe(importe)
    
>       assert categoria == "medio"
E       AssertionError: assert 'bajo' == 'medio'
E         
E         - medio
E         + bajo

lecciones/leccion_07_pruebas/test_mis_pruebas.py:40: AssertionError
```

**La línea que empieza con `>`** señala el renglón exacto donde la prueba se detuvo. Todo lo que está arriba de ella sí se ejecutó.

Ahora la decisión importante. Cuando una prueba falla hay dos sospechosos: el código y la prueba. Eric Matthes da la regla: **si la prueba comprobaba lo correcto, se arregla el código y no la prueba.** Aquí la prueba dice que 500 pesos es "medio", y eso es lo que pide el docstring. La prueba tiene razón, así que cambiar `"medio"` por `"bajo"` en el `assert` para que "vuelva a pasar" sería esconder el error. La prueba solo se cambia cuando lo que cambió fue la regla del negocio.

**Deshaz el cambio:** regresa el `<=` a `<` en `funciones.py`, guarda y corre la prueba hasta ver `1 passed`. No sigas con la lección hasta dejar el archivo como estaba.

### 4. Probar errores esperados

Los ejemplos de este concepto y de los tres siguientes prueban funciones pequeñas, parecidas a las de lecciones anteriores. Están completos en `ejemplos_de_pruebas.py`.

A veces lo correcto es que la función falle. `validar_cantidad("0")` debe lanzar un `ValueError`, y si un día deja de hacerlo, un pedido con cantidad cero entra al flujo. Eso también se prueba, con `pytest.raises`:

```python
def test_calcular_total_rechaza_cantidad_negativa():
    with pytest.raises(ValueError):
        calcular_total(-1, 50.0)
```

Se lee así: "dentro de este bloque espero un `ValueError`". Hay tres resultados posibles:

| Qué pasa dentro del bloque | Resultado de la prueba |
| --- | --- |
| Se lanza `ValueError` | Pasa |
| No se lanza ningún error | Falla, con el mensaje `Failed: DID NOT RAISE` |
| Se lanza otro error, por ejemplo `TypeError` | Falla, y ves ese error |

Dentro del bloque va solo la llamada que debe fallar. Si pones dos, la segunda nunca se ejecuta: el bloque termina en el primer error.

Con `match` revisas además una parte del mensaje. Sirve para distinguir dos errores del mismo tipo:

```python
    with pytest.raises(ValueError, match="no puede ser negativa"):
        calcular_total(-1, 50.0)
```

Si el error es del tipo correcto pero el mensaje es otro, la prueba falla y te muestra los dos textos:

```text
E   AssertionError: Regex pattern did not match.
E     Expected regex: 'mayor que cero'
E     Actual message: "invalid literal for int() with base 10: 'tres'"
```

Ese ejemplo es real: `validar_cantidad("tres")` sí lanza `ValueError`, pero el mensaje lo pone `int()`, no nuestra función.

### 5. Muchos casos, una sola lógica

Para probar `calcular_total` con tres pares de valores podrías escribir tres pruebas casi iguales. `parametrize` hace eso por ti: escribes la prueba una vez y le das la lista de casos.

```python
@pytest.mark.parametrize(
    ("cantidad", "precio_unitario", "esperado"),
    [
        (3, 19.99, 59.97),
        (3, 0.1, 0.3),
        (0, 99.9, 0.0),
    ],
)
def test_calcular_total_redondea_a_dos_decimales(cantidad, precio_unitario, esperado):
    total = calcular_total(cantidad, precio_unitario)

    assert total == esperado
```

La línea que empieza con `@` es un decorador: una etiqueta que se pone encima de una función para que pytest la trate de forma especial. No necesitas saber cómo funciona por dentro; basta con saber leerla:

- El primer argumento son los **nombres** de los parámetros de la prueba.
- El segundo es una **lista de tuplas**, una por caso, con los valores en el mismo orden.
- La función recibe esos nombres como parámetros.

pytest corre la prueba una vez por tupla, y cada corrida cuenta como una prueba aparte: si el segundo caso falla, los otros dos siguen pasando y sabes exactamente cuál se rompió.

Con `ids` le pones nombre a cada caso. Es un argumento más del decorador y va después de la lista de casos. Así queda el decorador completo:

```python
@pytest.mark.parametrize(
    ("cantidad", "precio_unitario", "esperado"),
    [
        (3, 19.99, 59.97),
        (3, 0.1, 0.3),
        (0, 99.9, 0.0),
    ],
    ids=["caso_normal", "redondeo", "cantidad_cero"],
)
```

```bash
pytest lecciones/leccion_07_pruebas/ejemplos_de_pruebas.py -v -k redondea
```

```text
lecciones/leccion_07_pruebas/ejemplos_de_pruebas.py::test_calcular_total_redondea_a_dos_decimales[caso_normal] PASSED [ 33%]
lecciones/leccion_07_pruebas/ejemplos_de_pruebas.py::test_calcular_total_redondea_a_dos_decimales[redondeo] PASSED [ 66%]
lecciones/leccion_07_pruebas/ejemplos_de_pruebas.py::test_calcular_total_redondea_a_dos_decimales[cantidad_cero] PASSED [100%]
```

Sin `ids`, pytest arma el nombre con los valores, por ejemplo `[3-0.1-0.3]`. Funciona, pero un nombre que diga para qué está el caso se lee mejor.

Parametriza cuando cambian los datos y la lógica es la misma. Si para un caso necesitas un `if` dentro de la prueba, ese caso merece su propia prueba.

### 6. Qué casos elegir

No hace falta probar todas las entradas posibles, ni se puede. Hace falta elegir las pocas que más probablemente revelen un error. Cuatro preguntas cubren casi todo:

| Pregunta | Ejemplo con las funciones de esta lección |
| --- | --- |
| ¿Funciona el **caso normal**? | `limpiar_precio("$45.50")` devuelve `45.5` |
| ¿Qué pasa justo en los **límites**? | `clasificar_importe` con 499.99, 500, 1999.99 y 2000 |
| ¿Qué pasa con lo **vacío**? | `contar_por_ciudad([])` devuelve `{}` |
| ¿Qué pasa con lo **inválido**? | `validar_cantidad("tres")` lanza `ValueError` |

Los límites merecen atención especial. En el concepto 3 viste por qué: confundir `<` con `<=` solo cambia el resultado en un valor exacto. Una prueba con 100 y otra con 1000 habrían pasado sin notar nada. Por eso un límite se prueba por los dos lados: el valor exacto y el inmediato anterior.

No persigas una cobertura total. Un criterio más útil: **prueba lo que duele si falla.** Una función que calcula importes merece más casos que una que arma un texto de bienvenida.

### 7. Fixtures: preparar sin repetir

Cuando varias pruebas necesitan los mismos datos de entrada, repetirlos en cada una cansa y esconde lo que importa. Una fixture es una función que prepara algo para las pruebas. Se marca con otra etiqueta, `@pytest.fixture`:

```python
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
```

La prueba pide la fixture poniendo su nombre como parámetro. pytest ve el parámetro `pedidos_de_ejemplo`, busca una fixture con ese nombre, la ejecuta y le entrega a la prueba lo que devolvió. Tú nunca llamas a la fixture.

pytest trae fixtures ya hechas. La que más vas a usar en datos es `tmp_path`, que ya conoces de las pruebas de la lección 6: entrega una carpeta temporal, nueva y vacía para cada prueba, como un objeto de `pathlib`.

```python
def test_guardar_resumen_escribe_un_json_que_se_puede_leer(tmp_path):
    ruta = tmp_path / "resumen.json"
    resumen = {"ciudad": "Mérida", "pedidos": 2}

    guardar_resumen(ruta, resumen)

    leido = json.loads(ruta.read_text(encoding="utf-8"))
    assert leido == resumen
```

Así una prueba puede escribir archivos sin ensuciar tu repositorio ni depender de lo que haya en tu computadora.

### 8. Pruebas independientes

Cada prueba debe poder correr sola, y el conjunto debe pasar en cualquier orden. Una prueba que solo pasa si antes corrió otra es una prueba que un día va a fallar sin motivo aparente, por ejemplo cuando uses `-k` para correr solo una.

La causa más común es compartir datos que alguien modifica:

```python
pedidos = [{"ciudad": "Puebla"}]  # una sola lista para todas las pruebas


def test_agregar_un_pedido():
    pedidos.append({"ciudad": "Mérida"})

    assert len(pedidos) == 2


def test_hay_un_pedido():
    assert len(pedidos) == 1  # falla si la otra prueba corrió antes
```

Las fixtures resuelven esto: pytest ejecuta la fixture de nuevo para cada prueba que la pide, así que cada una recibe su propia lista recién creada. En `ejemplos_de_pruebas.py` hay una prueba que modifica los pedidos de la fixture y no afecta a las demás.

### 9. Opciones útiles de pytest

Las opciones se escriben después de la ruta y se pueden combinar.

| Opción | Qué hace | Cuándo usarla |
| --- | --- | --- |
| `-v` | Muestra una línea por prueba, con su nombre completo | Para ver qué pruebas existen y cuál falla |
| `-x` | Se detiene en el primer fallo | Cuando hay muchos fallos y quieres ir de uno en uno |
| `-k texto` | Corre solo las pruebas cuyo nombre contiene ese texto | Para trabajar en un ejercicio: `-k ejercicio_3` |
| `--tb=short` | Formato corto de los fallos; `--tb=long` es el completo | Aquí el corto ya viene activado; pide el largo si necesitas contexto |
| `-l` | Muestra el valor de las variables de la prueba que falló | Para no llenar la prueba de `print()` |
| `--lf` | Corre solo las pruebas que fallaron la vez anterior | Al corregir un fallo entre muchas pruebas |

Con `-l`, el fallo del concepto 3 habría terminado así:

```text
E     - medio
E     + bajo
        categoria  = 'bajo'
        importe    = 500
```

Un detalle sobre `--lf`: para saber qué falló, pytest guarda el resultado de cada corrida en una carpeta `.pytest_cache`, que Git ya ignora. Si corres `--lf` sin una corrida anterior, corre todas las pruebas.

### 10. Dónde vive la configuración

pytest lee su configuración del archivo `pyproject.toml`, en la carpeta principal del curso, dentro de la sección `[tool.pytest.ini_options]`. Ábrelo y ubica cada línea:

| Línea | Qué hace |
| --- | --- |
| `minversion = "8.0"` | Exige pytest 8.0 o más reciente; con una versión anterior se niega a correr |
| `pythonpath = [".", "proyecto"]` | Agrega esas carpetas a los lugares donde Python busca módulos. Por eso funciona `from lecciones...` |
| `testpaths = ["lecciones", "proyecto"]` | Dónde buscar pruebas cuando escribes `pytest` sin ruta |
| `python_files = ["test_*.py"]` | La convención de descubrimiento del concepto 1: qué archivos contienen pruebas |
| `addopts = "..."` | Opciones que se agregan solas a cada corrida, como si las escribieras tú |

Y dentro de `addopts`:

| Opción | Qué hace |
| --- | --- |
| `-ra` | Agrega al final el resumen `short test summary info` con todo lo que no pasó |
| `--tb=short` | El formato corto de los fallos |
| `--strict-markers` | Trata como error una etiqueta `@pytest.mark...` desconocida, por ejemplo una mal escrita |
| `--strict-config` | Trata como error una línea mal escrita en esta misma configuración |

Por eso `ejemplos_de_pruebas.py` no corre cuando evalúas la carpeta: su nombre no cumple `test_*.py`. pytest solo lo toma cuando escribes su ruta completa.

## Ejercicios

Los ejercicios 0 a 5 se resuelven en `ejercicios.py` y el 6 en `test_mis_pruebas.py`. El ejercicio 0 es un calentamiento con funciones como valores, y a partir del 1 escribes pruebas.

En esta lección no escribes las funciones del negocio: escribes **comprobaciones**. Una comprobación es una función que recibe como parámetro la función que debe revisar y la pone a prueba con `assert`. Esto funciona por lo que viste en el concepto 0: una función es un valor más, y si escribes su nombre sin paréntesis no la llamas, solo la nombras, y así se puede pasar como argumento.

```python
def comprobar_calcular_total(calcular_total):
    assert calcular_total(2, 50.0) == 100.0
    assert calcular_total(3, 0.1) == 0.3
```

Dentro de la comprobación, usa siempre el parámetro. Así nosotros podemos llamarla varias veces con funciones distintas:

| Nuestra prueba llama a tu comprobación con... | Y espera que tu comprobación... |
| --- | --- |
| La función correcta de `funciones.py` | Termine sin error |
| Una versión defectuosa, escrita por nosotros | Falle en algún `assert` |

Si a tu comprobación se le escapa una versión defectuosa, la prueba te dice qué defecto tenía. Tu trabajo es pensar con qué entrada se nota ese defecto. Las versiones defectuosas están en `test_ejercicios.py`, por si quieres leerlas.

Tres recordatorios para todos los ejercicios:

- Una comprobación no devuelve nada. Su resultado es terminar bien o fallar.
- Los `assert` de tus comprobaciones no necesitan mensaje.
- No modifiques `funciones.py`. Si lo cambiaste en el concepto 3, deshaz el cambio.

Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_07_pruebas/test_ejercicios.py -k ejercicio_1
```

### Ejercicio 0. Calentamiento: `aplicar_a_todos(pedidos, funcion)`

En `ejercicios.py`. Recibe una lista y una función. Devuelve una lista nueva con el resultado de llamar a esa función con cada elemento. No es una prueba todavía: es el patrón de "recibir una función y llamarla" que usan todas las comprobaciones que siguen.

| Entrada | Resultado |
| --- | --- |
| `aplicar_a_todos(["$45", " 1,250.50 "], limpiar_precio)` | `[45.0, 1250.5]` |
| `aplicar_a_todos(pedidos, obtener_ciudad)` | `['Guadalajara', 'Tijuana']` |
| `aplicar_a_todos([], limpiar_precio)` | `[]` |

Paso a paso:

1. Crea una lista vacía para los resultados.
2. Recorre los elementos recibidos.
3. Llama a la función recibida con cada elemento y agrega a la lista lo que devuelva.
4. Devuelve la lista.

<details>
<summary>Pista 1</summary>

El parámetro `funcion` guarda una función. Para llamarla se usa como cualquier otra: su nombre y, entre paréntesis, el argumento.

</details>

<details>
<summary>Pista 2</summary>

Dentro de `aplicar_a_todos` no debe aparecer el nombre `limpiar_precio` ni ningún otro nombre concreto. La función no sabe cuál le van a enviar, y por eso sirve para todas. Compara con `mostrar_de_cada_uno` en el concepto 0: allá se imprime cada resultado, aquí se guarda.

</details>

### Ejercicio 1. `comprobar_limpiar_precio(limpiar_precio)`

Comprueba con `assert` que la función recibida convierte bien los precios.

| Entrada | Resultado |
| --- | --- |
| `comprobar_limpiar_precio(limpiar_precio)`, con la función correcta | Termina sin error |
| La misma llamada con una versión que descarta los centavos | Lanza `AssertionError` |
| La misma llamada con una versión que ignora lo que sigue a la primera coma | Lanza `AssertionError` |

Paso a paso:

1. Lee el docstring de `limpiar_precio` en `funciones.py` y anota qué promete quitar.
2. Elige un precio sencillo, sin símbolos, y escribe un `assert` que compare el resultado con el número esperado.
3. Agrega un `assert` por cada cosa que la función promete quitar.
4. Corre las pruebas. Si se te escapa una versión defectuosa, lee qué defecto tenía y busca el precio que lo delata.

<details>
<summary>Pista 1</summary>

Cada `assert` tiene la forma del ejemplo `comprobar_calcular_total` de arriba: la llamada a la izquierda, `==`, y el número esperado a la derecha.

</details>

<details>
<summary>Pista 2</summary>

Si todos tus precios son cantidades cerradas, como `"$45"` o `"$1,000"`, una función que pierde los decimales devuelve lo mismo que la correcta. Piensa qué debe traer el precio para que la diferencia se vea.

</details>

### Ejercicio 2. `comprobar_limites_de_clasificar_importe(clasificar_importe)`

Comprueba que la función recibida respeta los dos límites: 500 y 2000.

| Entrada | Resultado |
| --- | --- |
| `comprobar_limites_de_clasificar_importe(clasificar_importe)`, con la función correcta | Termina sin error |
| La misma llamada con una versión que usa `>` en lugar de `>=` en un límite | Lanza `AssertionError` |
| La misma llamada con una versión que compara como si los importes no tuvieran centavos | Lanza `AssertionError` |

Paso a paso:

1. Escribe en un papel la recta de importes y marca los dos límites y las tres categorías.
2. Para el límite de 500, comprueba el valor exacto y un valor apenas menor.
3. Haz lo mismo para el límite de 2000.

<details>
<summary>Pista 1</summary>

Son cuatro `assert`. Valores cómodos como 100, 1000 y 5000 caen lejos de los límites y no distinguen `>` de `>=`.

</details>

<details>
<summary>Pista 2</summary>

"Apenas menor" tiene que ser de verdad apenas: un importe puede traer centavos. Si pruebas con un peso menos, se te escapa la versión que compara como si los centavos no existieran.

</details>

### Ejercicio 3. `comprobar_validar_cantidad_rechaza_invalidos(validar_cantidad)`

Comprueba, con `pytest.raises`, que la función recibida lanza `ValueError` con cada tipo de cantidad inválida.

| Entrada | Resultado |
| --- | --- |
| `comprobar_validar_cantidad_rechaza_invalidos(validar_cantidad)`, con la función correcta | Termina sin error |
| La misma llamada con una versión que acepta el cero | Falla |
| La misma llamada con una versión que devuelve 0 cuando el texto no es un número | Falla |

Paso a paso:

1. Lee el docstring de `validar_cantidad` y haz la lista de todo lo que debe rechazar. Son varios tipos de texto distintos.
2. Para el primero, escribe un bloque `with pytest.raises(ValueError):` con la llamada dentro.
3. Repite para cada tipo de texto inválido de tu lista.

<details>
<summary>Pista 1</summary>

No pongas dos llamadas dentro del mismo bloque `with`: el bloque termina en el primer error y la segunda llamada nunca se revisa. Cada texto inválido necesita su propio bloque.

</details>

<details>
<summary>Pista 2</summary>

Si tienes los textos inválidos en una lista, un bucle `for` puede abrir un bloque `with` en cada vuelta.

</details>

<details>
<summary>Pista 3</summary>

"No es un número entero" incluye más de un caso: un texto con letras y un número con punto decimal son defectos distintos, y cada uno necesita su propia entrada.

</details>

### Ejercicio 4. `comprobar_contar_por_ciudad(contar_por_ciudad)`

Comprueba que la función recibida cuenta bien los pedidos de cada ciudad, también cuando no hay pedidos.

| Entrada | Resultado |
| --- | --- |
| `comprobar_contar_por_ciudad(contar_por_ciudad)`, con la función correcta | Termina sin error |
| La misma llamada con una versión que distingue mayúsculas de minúsculas | Lanza `AssertionError` |
| La misma llamada con una versión que devuelve `None` con la lista vacía | Lanza `AssertionError` |

Paso a paso:

1. Preparar: arma una lista de tres o cuatro pedidos. Cada pedido es un diccionario con la clave `"ciudad"`. Incluye una ciudad repetida y escríbela de formas distintas, como llega en los datos crudos.
2. Actuar: llama a la función con tu lista y guarda el resultado.
3. Comprobar: compara el resultado con el diccionario completo que esperas.
4. Agrega una comprobación más para la lista vacía.

<details>
<summary>Pista 1</summary>

Compara el diccionario entero con `==`, no clave por clave. Así también detectas una clave que sobra.

</details>

<details>
<summary>Pista 2</summary>

"De formas distintas" son dos cosas en el docstring: mayúsculas y espacios en los extremos. Si tu lista solo varía una, la otra queda sin revisar.

</details>

<details>
<summary>Pista 3</summary>

Vuelve a leer el docstring para ver cómo quedan escritas las claves del resultado. Lo esperado debe tener esa misma forma.

</details>

### Ejercicio 5. `casos_de_limpiar_precio()`

Devuelve una lista de casos lista para usarse en `parametrize`: al menos cuatro tuplas `(texto, esperado)`.

| Entrada | Resultado |
| --- | --- |
| `casos_de_limpiar_precio()` | Una lista de tuplas |
| `casos_de_limpiar_precio()[0]` | Por ejemplo, `('45.5', 45.5)` |

Paso a paso:

1. Empieza con el caso normal: un precio sin símbolos y su número.
2. Agrega casos hasta cubrir lo que traen los precios crudos: el símbolo `$`, comas de miles, espacios en los extremos y centavos.
3. Devuelve la lista. Cada texto debe ser distinto.

Esta función sí devuelve algo, y no usa `assert`: solo entrega los datos. Nuestras pruebas revisan que cada esperado sea correcto y que, entre todos, tus casos delaten a las versiones defectuosas del ejercicio 1.

<details>
<summary>Pista 1</summary>

Un mismo caso puede cubrir varias cosas a la vez, pero si falla no sabrás por cuál. Conviene tener casos simples, que varían una sola cosa, y uno o dos combinados.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba dice que un esperado no es correcto, llama a `limpiar_precio` con ese texto en el intérprete y compara. El esperado es un número, no un texto.

</details>

### Ejercicio 6. Tu archivo `test_mis_pruebas.py`

Completa tu archivo de pruebas. Ya tiene la prueba que escribiste en el concepto 2; ahora lo conviertes en un archivo que cuide de verdad a `funciones.py`.

| Requisito | Cómo lo revisamos |
| --- | --- |
| Al menos tres funciones `test_` | Contamos las funciones del archivo con ese prefijo |
| Cada una comprueba algo | Buscamos un `assert` o un `pytest.raises` en cada una. Un `assert` que no usa ningún valor, como `assert True`, no cuenta |
| Al menos una está parametrizada | Buscamos la etiqueta `@pytest.mark.parametrize` |
| Usan al menos tres de las cuatro funciones de `funciones.py` | Buscamos sus nombres dentro de tus pruebas |
| Todas pasan | Corremos pytest sobre tu archivo con el `funciones.py` de la lección |
| Detectan defectos | Corremos pytest sobre tu archivo con copias de `funciones.py` en las que una función tiene un defecto: las mismas versiones defectuosas de los ejercicios 1 a 4. Con cada función que uses, al menos una de esas versiones debe hacer fallar alguna prueba tuya |

Las dos últimas filas son el mismo criterio que aplicamos a tus comprobaciones de los ejercicios 1 a 4, ahora sobre un archivo de pruebas de verdad: una prueba vale si pasa con la función correcta y falla con la defectuosa. Si el mensaje dice que a tus pruebas se les escaparon defectos, te enumera cuáles, por función.

Paso a paso:

1. Elige una función que tenga varios casos con la misma lógica y escribe para ella una prueba parametrizada. Los casos del ejercicio 5 son un buen punto de partida.
2. Escribe una prueba para un error esperado.
3. Escribe una prueba con datos preparados, en tres partes: preparar, actuar, comprobar.
4. Ponle a cada prueba un nombre que diga qué función prueba, en qué situación y qué espera.
5. Corre `pytest lecciones/leccion_07_pruebas/test_mis_pruebas.py -v` y lee los nombres en voz alta. Si alguno no se entiende solo, cámbialo.
6. Cuando el archivo use todos sus imports, borra la línea `# ruff: noqa: F401` y el comentario que la explica.

<details>
<summary>Pista 1</summary>

En el ejercicio 5 escribiste los casos dentro de una función. En una prueba parametrizada, la lista de tuplas va directamente como segundo argumento de la etiqueta, como en el concepto 5.

</details>

<details>
<summary>Pista 2</summary>

Si pytest responde `function uses no argument 'texto'`, los nombres del primer argumento de `parametrize` no coinciden con los parámetros de la función. Deben escribirse igual.

</details>

<details>
<summary>Pista 3</summary>

Haz con una de tus pruebas lo mismo que en el concepto 3: rompe a propósito la función que cuida, mira si la prueba falla y deshaz el cambio. Si no falla, la prueba todavía no cuida nada. Es justo lo que hacen nuestras pruebas con tu archivo, con un defecto distinto cada vez: una prueba que solo llama a la función, o que compara contra algo que cualquier versión cumple, no detecta ninguno.

</details>

## Evalúate

Cuando termines los siete ejercicios, corre nuestras pruebas:

```bash
pytest lecciones/leccion_07_pruebas/test_ejercicios.py
```

Debes ver `42 passed`. Si una prueba falla, lee el mensaje completo: te dice si tu comprobación falló con la función correcta o qué defecto se le escapó.

Si corres la carpeta completa, pytest también descubre tu archivo y suma tus pruebas al total: verás 42 más las que hayas escrito, todas en `passed`.

```bash
pytest lecciones/leccion_07_pruebas
```

Revisa también el estilo de tu código:

```bash
ruff check lecciones/leccion_07_pruebas
```

Y guarda tu trabajo:

```bash
git add .
git commit -m "Completa la lección 7"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Qué dos convenciones de nombre usa pytest para descubrir las pruebas?
2. ¿Cuáles son las tres partes de una prueba y qué hace cada una?
3. En una prueba fallida, ¿qué te dicen la línea que empieza con `>` y las que empiezan con `E`?
4. Una prueba falla después de un cambio en el código. ¿Cómo decides si arreglas el código o la prueba?
5. ¿Qué pasa con una prueba que usa `pytest.raises(ValueError)` si la función no lanza ningún error?
6. ¿Por qué un límite se prueba con el valor exacto y con el inmediato anterior?
7. ¿Qué diferencia hay entre escribir `limpiar_precio` y `limpiar_precio(texto)`?
8. De la lección 6: en un bloque `try`, ¿cuándo se ejecuta la parte `else`?
9. De la lección 4: ¿qué devuelve `conteo.get("puebla", 0)` si la clave no existe, y por qué eso sirve para contar?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. En esta lección te dice qué defecto se le escapó a tu comprobación.
2. Prueba a mano: abre el intérprete con `python`, importa la función de `funciones.py` y llámala con la entrada que estás pensando.
3. Si el mensaje dice que `funciones.py` ya no se comporta como al inicio, deshaz tu cambio del concepto 3. Si no recuerdas cuál fue, `git restore lecciones/leccion_07_pruebas/funciones.py` devuelve el archivo a su último commit.
4. Revisa los ejemplos resueltos de `ejemplos.py` y `ejemplos_de_pruebas.py`.
5. Abre las pistas del ejercicio, una a la vez.
6. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 11, "Testing Your Code": qué es una prueba unitaria, cómo leer una prueba fallida, la regla de arreglar el código y no la prueba, y fixtures.
- Brian Okken, *Python Testing with pytest*, capítulo 1, "Getting Started with pytest" (descubrimiento y lectura de la salida); capítulo 2, "Writing Test Functions" (`assert`, excepciones esperadas, parametrización y la estructura Given, When, Then); capítulo 3, "pytest Fixtures"; capítulo 6, "Configuration".
- Bill Lubanovic, *Introducing Python*, capítulo 12, "Be a Pythonista": nombres, documentación y pruebas como hábitos de trabajo.
- Felienne Hermans, *The Programmer's Brain*, capítulo 3, "How to learn programming syntax quickly": por qué intentar recordar antes de buscar y por qué conviene repasar espaciado.
