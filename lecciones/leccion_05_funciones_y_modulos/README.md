# Lección 5: Funciones y módulos

Hasta ahora completaste funciones que alguien más había empezado. En esta lección las escribes tú desde la primera línea, las guardas en un módulo propio y las reutilizas desde otro archivo para limpiar pedidos completos.

**Tiempo estimado:** 100 minutos.
**Antes de empezar:** completa la [lección 4](../leccion_04_diccionarios/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Escribir una función completa: línea `def`, parámetros, docstring, cuerpo y `return`.
- Distinguir `return` de `print()` y explicar por qué una función sin `return` devuelve `None`.
- Llamar funciones con argumentos por posición y por nombre, y dar valores por defecto a los parámetros.
- Devolver varios valores a la vez y recibirlos en variables separadas.
- Guardar funciones en un módulo e importarlas desde otro archivo.
- Leer los tres errores típicos del tema: argumento faltante, operar con `None` y usar una variable fuera de su función.

## Por qué importa en datos

Un flujo de datos es una cadena de pasos pequeños: limpiar un texto, convertir un precio, decidir si un registro sirve. Si cada paso es una función con nombre, puedes probarlo por separado, y cuando un número sale mal sabes en qué paso buscar.

Repetir código es repetir errores. Si la limpieza de precios está copiada en cinco lugares y el archivo del proveedor cambia de formato, tienes cinco correcciones pendientes y basta olvidar una para que los totales dejen de cuadrar. Con una función, corriges en un solo lugar.

El módulo `limpieza.py` que escribes aquí es el mismo tipo de archivo que vas a usar en el proyecto final.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. No los copies y pegues: teclearlos es parte del aprendizaje.
2. Corre `python lecciones/leccion_05_funciones_y_modulos/ejemplos.py` y cambia valores para ver qué pasa.
3. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno. Los ejercicios 4 a 6 usan las funciones de los ejercicios 1 a 3.
4. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

## Conceptos

### 1. Por qué funciones

Una función es un bloque de código con nombre que hace **una** tarea. Tiene tres ventajas:

- **Se usa por su nombre.** Quien lee `limpiar_precio(texto)` entiende qué pasa sin leer cómo se hace.
- **Se escribe una vez.** Si hay un error, se corrige en un solo lugar.
- **Se prueba sola.** Le das una entrada, revisas la salida. Eso es lo que hacen las pruebas de este curso.

Ya usas funciones desde la lección 1: `len()`, `round()`, `sorted()`. Ahora vas a crear las tuyas.

### 2. Anatomía de una función

```python
def calcular_total(cantidad, precio_unitario):
    """Multiplica cantidad por precio unitario y redondea a dos decimales."""
    total = cantidad * precio_unitario
    return round(total, 2)
```

| Parte | En el ejemplo | Para qué sirve |
| --- | --- | --- |
| `def` | `def` | Palabra reservada que anuncia una función nueva. |
| Nombre | `calcular_total` | Con él la llamas después. |
| Parámetros | `(cantidad, precio_unitario)` | Nombres para los datos que la función recibe. Van entre paréntesis y la línea termina con dos puntos. |
| Docstring | `"""Multiplica..."""` | Texto entre comillas triples, justo debajo de `def`, que dice qué hace la función. |
| Cuerpo | las líneas con sangría | El código que hace el trabajo. Todo lo que tiene sangría de cuatro espacios pertenece a la función. |
| `return` | `return round(total, 2)` | Entrega el resultado a quien llamó y termina la función. |

Definir una función no la ejecuta: solo le enseña a Python qué hacer cuando la llames. Para llamarla escribes su nombre y, entre paréntesis, los valores:

```python
total = calcular_total(3, 45.5)
print(total)
```

```text
136.5
```

**Parámetro y argumento no son lo mismo.** El parámetro es el nombre que aparece en la definición (`cantidad`). El argumento es el valor que envías al llamar (`3`). En cada llamada, los argumentos llenan los parámetros: aquí `cantidad` vale `3` y `precio_unitario` vale `45.5`.

### 3. Provoca el error: falta un argumento

Guarda esto en un archivo `prueba.py` y córrelo. La llamada envía un solo argumento a una función que espera dos:

```python
def calcular_total(cantidad, precio_unitario):
    return round(cantidad * precio_unitario, 2)


total = calcular_total(3)
```

```text
Traceback (most recent call last):
  File "prueba.py", line 5, in <module>
    total = calcular_total(3)
TypeError: calcular_total() missing 1 required positional argument: 'precio_unitario'
```

Léelo de abajo hacia arriba. `TypeError` aparece aquí porque la llamada no coincide con la definición. El mensaje dice cuántos argumentos faltan (`missing 1`) y cuál (`'precio_unitario'`). El renglón señalado es la **llamada**, no la definición: ahí está lo que hay que corregir.

### 4. `return` frente a `print()`

`print()` muestra un valor en la pantalla. `return` lo entrega al código que llamó a la función, que puede guardarlo en una variable y seguir trabajando con él. Se parecen cuando pruebas a mano, y son muy distintos cuando una función alimenta a otra.

Provoca el error típico. Esta versión imprime el total en lugar de devolverlo:

```python
def calcular_total(cantidad, precio_unitario):
    print(round(cantidad * precio_unitario, 2))


total = calcular_total(3, 45.5)
print(total)
total_con_iva = total * 1.16
```

```text
136.5
None
Traceback (most recent call last):
  File "prueba.py", line 7, in <module>
    total_con_iva = total * 1.16
                    ~~~~~~^~~~~~
TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'
```

Lo que pasó, línea por línea de la salida:

1. `136.5` lo imprimió el `print()` de dentro de la función. Parece que funciona.
2. `None` es lo que quedó guardado en `total`. **Una función que no tiene `return` devuelve `None`.**
3. El `TypeError` dice que no se puede multiplicar `'NoneType'` (el tipo de `None`) por un `float`.

Cuando veas `'NoneType'` en un error, busca la función que debía entregar ese valor y revisa su `return`. Por eso las funciones de este curso siempre devuelven su resultado.

### 5. Argumentos por posición y por nombre

Hay dos maneras de enviar argumentos:

```python
print(calcular_total(3, 45.5))
print(calcular_total(precio_unitario=45.5, cantidad=3))
```

```text
136.5
136.5
```

- **Por posición:** el primer argumento llena el primer parámetro, el segundo llena el segundo. El orden importa: `calcular_total(45.5, 3)` pondría el precio en `cantidad`.
- **Por nombre:** escribes `parametro=valor`. El orden deja de importar y la llamada se lee sola.

Puedes mezclarlos, siempre con los posicionales primero: `calcular_total(3, precio_unitario=45.5)`. Al revés, Python se detiene antes de correr nada con `SyntaxError: positional argument follows keyword argument`.

### 6. Valores por defecto

Un parámetro puede traer un valor de fábrica, que se usa cuando la llamada no lo envía. Se escribe en la línea `def`:

```python
def aplicar_descuento(total, porcentaje=10):
    """Resta al total el porcentaje indicado. Si no se indica, resta 10."""
    descuento = total * porcentaje / 100
    return round(total - descuento, 2)


print(aplicar_descuento(200))
print(aplicar_descuento(200, 15))
print(aplicar_descuento(200, porcentaje=50))
```

```text
180.0
170.0
100.0
```

Dos reglas:

- Los parámetros con valor por defecto van al final, después de los que no lo tienen.
- Alrededor de ese `=` no se dejan espacios: `porcentaje=10`, tanto en la definición como en la llamada.

Un valor por defecto sirve para el caso más común. Así la llamada habitual queda corta y el caso especial sigue siendo posible.

### 7. Devolver varios valores

Para devolver más de un valor, sepáralos con una coma en el `return`. Python los empaca en una tupla:

```python
def calcular_minimo_y_maximo(precios):
    """Devuelve dos valores: el precio más bajo y el más alto."""
    ordenados = sorted(precios)
    return ordenados[0], ordenados[-1]


resultado = calcular_minimo_y_maximo([120.0, 45.5, 890.0, 350.0])
print(resultado)
```

```text
(45.5, 890.0)
```

Lo habitual es desempaquetar la tupla al recibirla, con una variable por cada valor, igual que haces con `for clave, valor in diccionario.items()`:

```python
minimo, maximo = calcular_minimo_y_maximo([120.0, 45.5, 890.0, 350.0])
print(minimo)
print(maximo)
```

```text
45.5
890.0
```

### 8. Alcance: lo que se crea dentro, se queda dentro

Las variables que nacen dentro de una función, incluidos sus parámetros, solo existen mientras la función corre. Provoca el error:

```python
def calcular_total(cantidad, precio_unitario):
    subtotal = cantidad * precio_unitario
    return round(subtotal, 2)


total = calcular_total(3, 45.5)
print(total)
print(subtotal)
```

```text
136.5
Traceback (most recent call last):
  File "prueba.py", line 8, in <module>
    print(subtotal)
          ^^^^^^^^
NameError: name 'subtotal' is not defined
```

Es el mismo `NameError` de la lección 1, con otra causa: el nombre está bien escrito, pero `subtotal` desapareció cuando la función terminó. Fuera de ella no existe.

Esto es una ventaja. Cada función es una caja cerrada: lo único que entra son los argumentos y lo único que sale es lo que pasa por `return`. Dos funciones pueden usar el mismo nombre de variable sin estorbarse.

### 9. Funciones pequeñas que se combinan

Una función debe hacer una sola cosa. Si para describirla necesitas la palabra "y" ("limpia el precio **y** calcula el total **y** lo muestra"), probablemente son tres funciones.

Las funciones pequeñas se combinan: el resultado de una es el argumento de otra.

```python
total_con_descuento = aplicar_descuento(calcular_total(2, 350.0), 15)
print(total_con_descuento)
```

```text
595.0
```

Python resuelve primero la llamada de dentro (`calcular_total(2, 350.0)` da `700.0`) y con ese valor llama a la de fuera. Una función también puede llamar a otra dentro de su cuerpo, y eso es justo lo que harás en los ejercicios: `es_faltante` usa `limpiar_texto`, y `limpiar_pedido` usa las tres.

### 10. Módulos

Un **módulo** es un archivo `.py`. Nada más. Las funciones que defines en un archivo se pueden usar desde otro con `import`.

En esta carpeta hay un módulo ya resuelto, `formato.py`, con dos funciones. `ejemplos.py` vive en la misma carpeta y lo usa. Hay tres formas de importar:

```python
import formato

print(formato.formatear_importe(1250.5))
```

```text
$1,250.50 MXN
```

| Forma | Cómo se usa después | Cuándo conviene |
| --- | --- | --- |
| `import formato` | `formato.formatear_importe(1250.5)` | Casi siempre. Se ve de qué módulo viene cada función. |
| `from formato import formatear_importe` | `formatear_importe(1250.5)` | Cuando usas una o dos funciones muchas veces. |
| `import formato as fmt` | `fmt.formatear_importe(1250.5)` | Cuando el nombre del módulo es largo. `fmt` es un alias. |

Python también trae módulos listos, la biblioteca estándar. Se importan igual:

```python
import math

print(math.ceil(7 / 6))
```

```text
2
```

**Dónde busca Python un módulo.** Primero, en la carpeta del archivo que estás corriendo. Por eso a `ejemplos.py` le basta `import formato`. Las pruebas, en cambio, se corren desde la carpeta principal del curso, así que desde ahí hay que indicar el camino completo, con puntos en lugar de diagonales:

```python
from lecciones.leccion_05_funciones_y_modulos import limpieza
```

Se lee: "de la carpeta `lecciones`, de la carpeta `leccion_05_funciones_y_modulos`, trae el módulo `limpieza`". Esa línea ya está escrita en `ejercicios.py`. Después de ella, las funciones se usan como `limpieza.limpiar_texto(...)`.

**El bloque `if __name__ == "__main__":`.** Al importar un módulo, Python ejecuta todo el archivo. Si no quieres que una parte corra al importarlo, ponla dentro de este bloque: solo se ejecuta cuando corres el archivo directamente. Compruébalo: `python lecciones/leccion_05_funciones_y_modulos/formato.py` imprime una demostración, y esa demostración no aparece cuando `ejemplos.py` importa el módulo.

### 11. Estilo de las funciones

El estilo que sigue casi todo el código de Python está escrito en una guía llamada PEP 8. Para funciones pide:

- **Nombres en minúsculas, con guion bajo:** `limpiar_precio`, no `LimpiarPrecio` ni `limpiarprecio`.
- **Dos líneas en blanco** antes y después de cada función.
- **Los `import`, al inicio del archivo**, debajo del docstring del módulo.
- **Sin espacios alrededor del `=`** de un valor por defecto o de un argumento por nombre.

En este curso añadimos dos costumbres propias:

- **El nombre empieza con un verbo en infinitivo** que dice qué hace: `limpiar_`, `calcular_`, `separar_`. Las funciones que responden sí o no empiezan con `es_` o `tiene_`: `es_faltante`.
- **Toda función lleva docstring.** Una frase que diga qué hace basta.

`ruff check` revisa por ti los nombres y el orden de los imports, y `ruff format` acomoda las líneas en blanco.

## Ejercicios

Esta lección tiene dos archivos de trabajo.

| Archivo | Ejercicios | Qué haces |
| --- | --- | --- |
| `limpieza.py` | 1, 2 y 3 | El archivo está casi vacío. Escribes cada función completa, desde `def`. |
| `ejercicios.py` | 4, 5 y 6 | Como en las lecciones anteriores: borras el `raise NotImplementedError(...)` y completas el cuerpo, reutilizando las funciones de `limpieza.py`. |

Mientras una función de `limpieza.py` no exista, sus pruebas fallan con este mensaje:

```text
E   Failed: Todavía no existe la función limpiar_texto() en limpieza.py. Escríbela completa: la línea def con ese nombre exacto, su docstring, el cuerpo y el return.
```

Tres recordatorios para todos los ejercicios:

- La función debe **devolver** el resultado con `return`. Usar `print()` no cuenta.
- Usa los parámetros que recibe la función. No escribas valores fijos.
- Los nombres de las funciones y de los parámetros deben ser exactamente los del enunciado: las pruebas los buscan por nombre.

Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_05_funciones_y_modulos -k ejercicio_1
```

### Ejercicio 1. `limpiar_texto(texto)`

En `limpieza.py`. Quita los espacios de los extremos y pasa todo a minúsculas. Ya resolviste esta lógica en la lección 1; lo nuevo es que ahora escribes la función entera.

| Entrada | Resultado |
| --- | --- |
| `limpiar_texto("  Monterrey ")` | `'monterrey'` |
| `limpiar_texto("GUADALAJARA")` | `'guadalajara'` |

Paso a paso:

1. Debajo del docstring del módulo, deja dos líneas en blanco.
2. Escribe la línea `def` con el nombre de la función y su parámetro. Termina con dos puntos.
3. En la línea siguiente, con cuatro espacios de sangría, escribe el docstring: una frase entre comillas triples que diga qué hace la función.
4. Escribe el cuerpo: limpia el texto que llega en el parámetro.
5. Devuelve el resultado.

<details>
<summary>Pista 1</summary>

Usa como plantilla la función `calcular_total` de la sección "Anatomía de una función". Cambian el nombre, los parámetros, el docstring y el cuerpo; la forma es la misma.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba dice que la función no existe y tú ya la escribiste, revisa tres cosas: que guardaste el archivo, que el nombre está escrito igual que en el enunciado y que la línea `def` empieza pegada al margen izquierdo, sin sangría.

</details>

### Ejercicio 2. `limpiar_precio(texto, simbolo="$")`

En `limpieza.py`. Convierte un precio escrito como texto en un `float`. Quita los espacios, el símbolo de moneda y las comas de miles. El símbolo es un parámetro con valor por defecto, porque no todos los archivos escriben la moneda igual.

| Entrada | Resultado |
| --- | --- |
| `limpiar_precio(" $1,250.50 ")` | `1250.5` |
| `limpiar_precio("1,250.50 MXN", simbolo="MXN")` | `1250.5` |
| `limpiar_precio("USD 2,100.00", "USD")` | `2100.0` |

Paso a paso:

1. Deja dos líneas en blanco después de la función anterior y escribe la línea `def` con los dos parámetros. El segundo lleva su valor por defecto.
2. Escribe el docstring.
3. Quita los espacios de los extremos.
4. Elimina el símbolo que llegó en el parámetro.
5. Elimina las comas.
6. Convierte lo que queda en `float` y devuélvelo.

<details>
<summary>Pista 1</summary>

Dentro de la función, `simbolo` es una variable como cualquier otra: puedes pasarla como argumento a un método de texto. Si escribes un `"$"` fijo en el cuerpo, la función ignora lo que le envían.

</details>

<details>
<summary>Pista 2</summary>

Con `"1,250.50 MXN"`, al quitar `MXN` queda un espacio al final. No te preocupes por él: `float()` acepta espacios en los extremos.

</details>

### Ejercicio 3. `es_faltante(valor)`

En `limpieza.py`. Indica si un valor representa un dato que no se capturó. Devuelve `True` si el valor es `None` o si, una vez limpio, es alguno de estos textos: `""`, `"n/d"`, `"na"`, `"null"`. En cualquier otro caso devuelve `False`.

| Entrada | Resultado |
| --- | --- |
| `es_faltante(None)` | `True` |
| `es_faltante(" N/D ")` | `True` |
| `es_faltante("   ")` | `True` |
| `es_faltante("Nayarit")` | `False` |

Paso a paso:

1. Escribe la línea `def` y el docstring.
2. Si el valor es `None`, devuelve `True` de inmediato.
3. Limpia el valor con la función que escribiste en el ejercicio 1.
4. Devuelve si el texto limpio está entre los cuatro textos de la lista.

<details>
<summary>Pista 1</summary>

El orden de los pasos 2 y 3 importa. `None` no es un texto y no tiene métodos: si intentas limpiarlo primero, Python responde con un `AttributeError`.

</details>

<details>
<summary>Pista 2</summary>

Dentro de un mismo archivo, una función llama a otra solo por su nombre, sin `import`. Y recuerda de la lección 3 que `valor in coleccion` ya da `True` o `False`: puedes devolver ese resultado directamente.

</details>

### Ejercicio 4. `limpiar_pedido(pedido_crudo)`

En `ejercicios.py`. Recibe un pedido tal como llega del archivo, con todos sus valores como texto, y devuelve un diccionario **nuevo** con los valores limpios. No modifica el original.

| Clave | Valor crudo | Valor limpio | Cómo |
| --- | --- | --- | --- |
| `id_pedido` | `" 1001 "` | `1001` | Entero. |
| `ciudad` | `"  GUADALAJARA "` | `'Guadalajara'` | Texto limpio y luego `.title()`. |
| `producto` | `" prensa francesa"` | `'Prensa Francesa'` | Texto limpio y luego `.title()`. |
| `cantidad` | `"2"` | `2` | Entero. |
| `precio_unitario` | `" $1,250.50 "` | `1250.5` | Con `limpiar_precio`. |
| `estado` | `" Entregado "` | `'entregado'` | Texto limpio. |

Paso a paso:

1. Crea un diccionario nuevo.
2. Para cada clave, toma el valor de `pedido_crudo`, límpialo o conviértelo según la tabla y guárdalo en el diccionario nuevo con la misma clave.
3. Devuelve el diccionario nuevo.

<details>
<summary>Pista 1</summary>

Las funciones de limpieza viven en otro módulo. Se llaman con el nombre del módulo por delante: `limpieza.limpiar_texto(...)`. Si escribes solo `limpiar_texto(...)`, Python responde con un `NameError`.

</details>

<details>
<summary>Pista 2</summary>

`limpieza.limpiar_texto(...)` devuelve un texto, y a un texto se le pueden encadenar métodos. `int()` acepta espacios en los extremos, igual que `float()`.

</details>

<details>
<summary>Pista 3</summary>

Si la prueba dice que modificaste el original, estás asignando sobre `pedido_crudo`. Las asignaciones van sobre el diccionario nuevo; `pedido_crudo` solo se lee.

</details>

### Ejercicio 5. `es_pedido_valido(pedido)`

En `ejercicios.py`. Recibe un pedido **ya limpio** y devuelve `True` solo si cumple las tres condiciones: la ciudad no es un faltante, la cantidad es mayor que 0 y el precio unitario es mayor que 0.

| Pedido limpio | Resultado |
| --- | --- |
| ciudad `'Guadalajara'`, cantidad `2`, precio `1250.5` | `True` |
| ciudad `'N/D'`, cantidad `2`, precio `1250.5` | `False` |
| ciudad `'Guadalajara'`, cantidad `0`, precio `1250.5` | `False` |
| ciudad `'Guadalajara'`, cantidad `2`, precio `0.0` | `False` |

Paso a paso:

1. Revisa la ciudad con `es_faltante`. Si falta, el pedido no es válido.
2. Revisa que la cantidad sea mayor que 0.
3. Revisa que el precio unitario sea mayor que 0.
4. Devuelve `True` solo si pasó las tres revisiones.

<details>
<summary>Pista 1</summary>

Un `return` termina la función en ese momento. Puedes revisar las condiciones una por una y devolver `False` en cuanto una no se cumpla; si la función llega hasta el final, el pedido es válido.

</details>

<details>
<summary>Pista 2</summary>

Cuida que todos los caminos terminen en un `return`. Si la prueba dice que obtuviste `None`, hay un camino que llega al final de la función sin devolver nada.

</details>

### Ejercicio 6. `separar_validos(pedidos)`

En `ejercicios.py`. Recibe una lista de pedidos limpios y la reparte en dos listas: los válidos y los rechazados. Devuelve las dos, en ese orden, en una tupla. No se pierde ningún pedido: cada uno termina en una de las dos listas.

| Entrada | Resultado |
| --- | --- |
| `separar_validos([bueno, sin_ciudad, otro_bueno])` | `([bueno, otro_bueno], [sin_ciudad])` |
| `separar_validos([])` | `([], [])` |

Paso a paso:

1. Crea dos listas vacías, una para cada grupo.
2. Recorre los pedidos.
3. Decide con la función del ejercicio 5 a cuál lista va cada pedido y agrégalo.
4. Devuelve las dos listas con un solo `return`.

<details>
<summary>Pista 1</summary>

Es el patrón de acumulador de la lección 2, con dos acumuladores en lugar de uno. `es_pedido_valido` está en este mismo archivo, así que se llama solo por su nombre.

</details>

<details>
<summary>Pista 2</summary>

Vuelve a la sección "Devolver varios valores". El orden en el `return` es el orden en que quien llama recibe las listas: primero válidos, después rechazados.

</details>

## Evalúate

Cuando termines los seis ejercicios, corre la lección completa:

```bash
pytest lecciones/leccion_05_funciones_y_modulos
```

Debes ver `53 passed`. Si una prueba falla, lee la línea que empieza con `E`: te dice con qué valores se probó, qué se esperaba y qué devolvió tu función.

Revisa también el estilo de tu código. El primer comando avisa de nombres e imports fuera de estilo; el segundo acomoda por ti el formato, incluidas las dos líneas en blanco entre funciones:

```bash
ruff check lecciones/leccion_05_funciones_y_modulos
ruff format lecciones/leccion_05_funciones_y_modulos
```

Para terminar, usa tus funciones a mano. Desde la carpeta principal del curso abre el intérprete con `python` y escribe:

```python
from lecciones.leccion_05_funciones_y_modulos import limpieza

limpieza.limpiar_precio("1,250.50 MXN", simbolo="MXN")
help(limpieza.limpiar_precio)
```

`help()` muestra el docstring que tú escribiste. Para eso sirve. Sal de la ayuda con la tecla `q`.

Y guarda tu trabajo:

```bash
git add .
git commit -m "Completa la lección 5"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Qué diferencia hay entre un parámetro y un argumento?
2. ¿Qué devuelve una función que no tiene `return`? ¿Qué error aparece si multiplicas ese resultado por un número?
3. Con `def aplicar_descuento(total, porcentaje=10)`, ¿qué devuelve `aplicar_descuento(200)`? ¿Y `aplicar_descuento(200, porcentaje=50)`?
4. ¿Por qué no puedes usar fuera de una función una variable que creaste dentro de ella? ¿Qué error aparece?
5. ¿Qué diferencia hay entre `import limpieza` y `from limpieza import limpiar_texto` a la hora de llamar a la función?
6. De la lección 4: ¿qué devuelve `pedido.get("ciudad")` si el diccionario no tiene esa clave?
7. De la lección 2: ¿cómo se llama el patrón de crear una lista vacía antes de un bucle y llenarla dentro de él?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. Casi siempre trae la respuesta.
2. Prueba tu función a mano: desde la carpeta principal abre el intérprete con `python`, importa el módulo como en la sección "Evalúate" y llama a la función con el valor que falló. Si cambias el archivo, cierra el intérprete con `exit()` y vuelve a abrirlo para que tome los cambios.
3. Revisa los ejemplos resueltos de `ejemplos.py` y el módulo `formato.py`.
4. Abre las pistas del ejercicio, una a la vez.
5. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

| Qué ves | Qué significa |
| --- | --- |
| `Failed: Todavía no existe la función ...` | Falta escribirla en `limpieza.py`, o su nombre no coincide con el del enunciado. |
| `AttributeError: module '...limpieza' has no attribute '...'` | Un ejercicio de `ejercicios.py` llama a una función de `limpieza.py` que aún no existe o tiene otro nombre. |
| `TypeError: ... missing 1 required positional argument` | La llamada envía menos argumentos de los que la función espera. |
| `TypeError` con `'NoneType'` | Alguna función terminó sin `return` y entregó `None`. |
| `IndentationError` | El docstring o el cuerpo no tienen la sangría de cuatro espacios bajo `def`. |

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 8, "Functions": definición y llamada, argumentos por posición y por nombre, valores por defecto, `return`, funciones guardadas en módulos, formas de `import` y estilo de funciones.
- Bill Lubanovic, *Introducing Python*, capítulo 5, "Py Boxes: Modules, Packages, and Programs": módulos, `import` y alias.
- Reuven Lerner, *Python Workout*, 2.ª ed., capítulo 7, "Functions": ejercicios sobre parámetros, valores por defecto y funciones que reciben funciones.
- Felienne Hermans, *The Programmer's Brain*, capítulo 8, "How to get better at naming things": por qué un buen nombre reduce el esfuerzo de leer código.
