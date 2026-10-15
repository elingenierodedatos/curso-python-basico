# Lección 4: Diccionarios y conjuntos

Hasta ahora un pedido era un puñado de variables sueltas o una lista donde había que recordar qué iba en cada posición. En esta lección aprendes a guardar un pedido completo en una sola estructura, con cada dato bajo su nombre, y a responder con ella las preguntas de siempre: cuántos pedidos hay por ciudad y cuánto se vendió de cada producto.

**Tiempo estimado:** 120 minutos.
**Antes de empezar:** completa la [lección 3](../leccion_03_condicionales/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Guardar un registro en un diccionario y leer, agregar, modificar y borrar sus claves.
- Leer una clave que puede faltar sin que el programa se detenga.
- Recorrer un diccionario y una lista de diccionarios.
- Contar y sumar por grupo con un diccionario como acumulador.
- Obtener valores únicos con un conjunto.
- Copiar un diccionario para no modificar el que recibes.

## Por qué importa en datos

Una tabla es una lista de filas, y cada fila es un registro: un valor por columna. En Python eso se escribe como una lista de diccionarios, donde la clave es el nombre de la columna y el valor es el dato. Es el formato en que llegan los datos cuando lees un archivo CSV, un JSON o el resultado de una consulta, y es el formato en que recibirás los pedidos en el resto del curso.

También vas a escribir a mano la operación más común del análisis de datos: agrupar y resumir. Lo que en SQL se pide con `GROUP BY`, aquí lo construyes con un bucle y un diccionario. Cuando más adelante uses una herramienta que lo hace por ti, sabrás qué ocurre por dentro.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. No los copies y pegues: teclearlos es parte del aprendizaje.
2. Corre `python lecciones/leccion_04_diccionarios/ejemplos.py` y cambia valores para ver qué pasa.
3. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno.
4. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

## Conceptos

### 1. Un diccionario es un registro

Un diccionario guarda parejas de **clave** y **valor**. Se escribe entre llaves, con dos puntos entre la clave y su valor, y comas entre las parejas.

```python
pedido = {
    "id_pedido": 1001,
    "producto": "Café de olla",
    "cantidad": 2,
    "precio_unitario": 185.0,
}
```

Piensa en una fila de una tabla:

| id_pedido | producto | cantidad | precio_unitario |
| --- | --- | --- | --- |
| 1001 | Café de olla | 2 | 185.0 |

Cada clave es el nombre de una columna y cada valor es el dato de esa fila. Las claves casi siempre son textos; los valores pueden ser de cualquier tipo.

Para leer un valor se escribe la clave entre corchetes:

```python
print(pedido["producto"])
print(pedido["cantidad"] * pedido["precio_unitario"])
```

```text
Café de olla
370.0
```

En una lista pides un elemento por su posición: `fila[1]`. En un diccionario lo pides por su nombre: `pedido["producto"]`. El código se lee solo y no depende de recordar el orden de las columnas.

Un diccionario vacío se escribe `{}`, y `len(pedido)` devuelve cuántas claves tiene.

### 2. Agregar y modificar

Las dos cosas se escriben igual: la clave entre corchetes, el signo `=` y el valor.

```python
pedido["estado"] = "enviado"  # la clave no existía: se agrega
pedido["cantidad"] = 3  # la clave ya existía: se cambia su valor
print(pedido)
```

```text
{'id_pedido': 1001, 'producto': 'Café de olla', 'cantidad': 3, 'precio_unitario': 185.0, 'estado': 'enviado'}
```

Dos consecuencias:

- Una clave no se repite. Si asignas a una clave que ya existe, el valor anterior se pierde.
- Las mayúsculas cuentan. `"Estado"` y `"estado"` son dos claves distintas.

### 3. Provoca el error: una clave que no existe

Los datos reales no siempre traen todas las columnas. Crea un archivo `prueba.py` con un pedido sin ciudad e intenta leerla:

```python
pedido = {"id_pedido": 1001, "producto": "Café de olla", "cantidad": 2}
print(pedido["ciudad"])
```

Python responde:

```text
Traceback (most recent call last):
  File "prueba.py", line 2, in <module>
    print(pedido["ciudad"])
          ~~~~~~^^^^^^^^^^
KeyError: 'ciudad'
```

Léelo de abajo hacia arriba, como en la lección 1:

1. **Última línea:** `KeyError` significa que pediste una clave que el diccionario no tiene. Después de los dos puntos viene la clave que buscaste, tal como la escribiste.
2. **Línea con `File`:** el archivo y el renglón.
3. **El renglón señalado:** las marcas apuntan a la lectura con corchetes que falló.

Cuando veas un `KeyError`, compara la clave del mensaje con las claves reales del diccionario. Las tres causas de siempre: la clave no viene en ese registro, está escrita con otra ortografía (`"Ciudad"`, `"ciudad "`) o estás leyendo un diccionario distinto del que creías.

### 4. Leer una clave que puede faltar: `.get()` e `in`

El método `.get()` lee una clave sin provocar el error. Si la clave no existe, devuelve `None`; si le das un segundo valor, devuelve ese.

```python
pedido = {"id_pedido": 1001, "producto": "Café de olla", "cantidad": 2}

print(pedido.get("producto"))
print(pedido.get("ciudad"))
print(pedido.get("ciudad", "sin ciudad"))
```

```text
Café de olla
None
sin ciudad
```

`.get()` solo lee: el diccionario queda igual, sin la clave `"ciudad"`.

Para preguntar si una clave existe se usa `in`, que ya conoces de las listas. En un diccionario, `in` busca entre las claves, no entre los valores.

```python
print("producto" in pedido)
print("ciudad" in pedido)
print("Café de olla" in pedido)
```

```text
True
False
False
```

¿Cuál usar? Corchetes cuando la clave **debe** existir y su ausencia es un problema que quieres ver de inmediato. `.get()` cuando la ausencia es normal y tienes un valor razonable para ese caso.

### 5. Borrar una clave

`del` elimina la clave y su valor.

```python
pedido = {"id_pedido": 1001, "producto": "Café de olla", "notas": "N/D"}
del pedido["notas"]
print(pedido)
```

```text
{'id_pedido': 1001, 'producto': 'Café de olla'}
```

Si la clave no existe, `del` provoca el mismo `KeyError` que la lectura con corchetes.

### 6. Recorrer un diccionario

Hay tres métodos para recorrerlo con un `for`:

| Método | Qué entrega en cada vuelta |
| --- | --- |
| `.keys()` | Cada clave |
| `.values()` | Cada valor |
| `.items()` | Cada pareja, como una tupla `(clave, valor)` |

El más usado es `.items()`, con dos variables en el `for`: una recibe la clave y la otra el valor.

```python
pedido = {"id_pedido": 1001, "producto": "Café de olla", "cantidad": 2}

for clave, valor in pedido.items():
    print(f"{clave}: {valor}")
```

```text
id_pedido: 1001
producto: Café de olla
cantidad: 2
```

Las claves salen en el orden en que se agregaron. Si recorres el diccionario sin ningún método, recibes las claves: `for clave in pedido:` hace lo mismo que `for clave in pedido.keys():`.

```python
for valor in pedido.values():
    print(valor)
```

```text
1001
Café de olla
2
```

### 7. Una lista de diccionarios es una tabla

Un diccionario es una fila. Varias filas se guardan en una lista.

```python
pedidos = [
    {"id_pedido": 1001, "ciudad": "Puebla", "cantidad": 2, "estado": "entregado"},
    {"id_pedido": 1002, "ciudad": "Monterrey", "cantidad": 1, "estado": "enviado"},
    {"id_pedido": 1003, "ciudad": "Puebla", "cantidad": 4, "estado": "entregado"},
    {"id_pedido": 1004, "ciudad": "Tijuana", "cantidad": 3, "estado": "cancelado"},
    {"id_pedido": 1005, "ciudad": "Puebla", "cantidad": 5, "estado": "entregado"},
]
```

Todo lo que sabes de listas sigue valiendo: `len(pedidos)` es el número de filas y `pedidos[0]` es la primera. Como cada elemento es un diccionario, puedes pedirle una clave enseguida:

```python
print(len(pedidos))
print(pedidos[0]["ciudad"])
```

```text
5
Puebla
```

Y el bucle `for` recorre la tabla fila por fila:

```python
for fila in pedidos:
    print(fila["id_pedido"], fila["estado"])
```

```text
1001 entregado
1002 enviado
1003 entregado
1004 cancelado
1005 entregado
```

Este es el formato en que llegarán los pedidos de aquí en adelante.

### 8. Contar y sumar por grupo

¿Cuántos pedidos hay en cada estado? En la lección 2 usaste un acumulador: una variable que empieza en cero y crece en cada vuelta. Aquí necesitas un acumulador **por cada estado**, y no sabes de antemano cuántos estados hay. La solución es un diccionario que empieza vacío: la clave es el grupo y el valor es su cuenta.

```python
conteo = {}
for fila in pedidos:
    estado = fila["estado"]
    conteo[estado] = conteo.get(estado, 0) + 1

print(conteo)
```

```text
{'entregado': 3, 'enviado': 1, 'cancelado': 1}
```

La línea clave se lee de derecha a izquierda:

1. `conteo.get(estado, 0)`: cuánto llevaba ese estado. Si es la primera vez que aparece, todavía no está en el diccionario y `.get()` devuelve `0`.
2. `+ 1`: se suma el pedido actual.
3. `conteo[estado] = ...`: se guarda la cuenta nueva. Si la clave no existía, se agrega.

Así cambia `conteo` en cada vuelta:

| Vuelta | `estado` | `conteo` al terminar la vuelta |
| --- | --- | --- |
| 1 | `entregado` | `{'entregado': 1}` |
| 2 | `enviado` | `{'entregado': 1, 'enviado': 1}` |
| 3 | `entregado` | `{'entregado': 2, 'enviado': 1}` |
| 4 | `cancelado` | `{'entregado': 2, 'enviado': 1, 'cancelado': 1}` |
| 5 | `entregado` | `{'entregado': 3, 'enviado': 1, 'cancelado': 1}` |

Si en lugar de `.get()` escribieras `conteo[estado] + 1`, la primera vuelta fallaría con `KeyError: 'entregado'`: no se puede leer una cuenta que todavía no existe.

**Sumar por grupo** es el mismo patrón. Lo único que cambia es lo que se suma: en lugar de `1`, un valor de la fila.

```python
piezas = {}
for fila in pedidos:
    ciudad = fila["ciudad"]
    piezas[ciudad] = piezas.get(ciudad, 0) + fila["cantidad"]

print(piezas)
```

```text
{'Puebla': 11, 'Monterrey': 1, 'Tijuana': 3}
```

Si conoces SQL, esto es un `GROUP BY` hecho a mano: `SELECT ciudad, SUM(cantidad) FROM pedidos GROUP BY ciudad`.

### 9. Conjuntos: valores únicos

Un conjunto (`set`) es una colección que no admite repetidos. Se crea vacío con `set()` y se le agregan valores con `.add()`. Agregar un valor que ya está no hace nada.

```python
estados = set()
for fila in pedidos:
    estados.add(fila["estado"])

print(len(estados))
```

```text
3
```

Cinco pedidos, tres estados distintos. También puedes convertir una lista en conjunto de un solo paso: `set(["Puebla", "Tijuana", "Puebla"])` se queda con dos valores.

> Cuidado: `{}` es un diccionario vacío, no un conjunto vacío. El conjunto vacío se escribe `set()`.

**Un conjunto no tiene orden.** No guarda sus valores en posiciones, así que no existe "el primero". Compruébalo provocando el error:

```python
estados = {"entregado", "enviado", "cancelado"}
print(estados[0])
```

```text
TypeError: 'set' object is not subscriptable
```

"Not subscriptable" quiere decir que ese tipo no acepta corchetes. Además, si imprimes un conjunto de textos, el orden en que aparecen puede cambiar de una ejecución a otra. Un resultado que cambia solo no sirve para un reporte ni para una prueba.

Por eso, cuando el resultado tiene que salir del conjunto, se ordena. `sorted()` acepta un conjunto y devuelve una **lista** ordenada:

```python
print(sorted(estados))
```

```text
['cancelado', 'entregado', 'enviado']
```

### 10. Dos nombres, un solo diccionario

Recuerda la lección 1: una variable es un nombre que apunta a un valor. Asignar un diccionario a otra variable no crea un segundo diccionario; crea un segundo nombre para el mismo.

```python
original = {"id_pedido": 1001, "estado": "enviado"}
otro_nombre = original
otro_nombre["estado"] = "entregado"

print(original["estado"])
```

```text
entregado
```

Lo mismo pasa con el parámetro de una función. El diccionario que la función recibe es el mismo que tiene quien la llamó, no una copia:

```python
def marcar_entregado(pedido):
    pedido["estado"] = "entregado"
    return pedido


original = {"id_pedido": 1001, "estado": "enviado"}
resultado = marcar_entregado(original)

print(original["estado"])
```

```text
entregado
```

Quien llamó a la función no esperaba que su pedido cambiara. En un flujo de datos, donde los mismos pedidos pasan por muchas funciones, este descuido produce errores difíciles de rastrear. Las listas se comportan igual.

La solución es el método `.copy()`, que devuelve un diccionario nuevo con las mismas claves y valores. Lo que hagas con la copia no toca al original.

```python
original = {"id_pedido": 1001, "estado": "enviado"}
copia = original.copy()
copia["estado"] = "entregado"

print(original["estado"])
print(copia["estado"])
```

```text
enviado
entregado
```

Regla del curso: una función no modifica los datos que recibe. Si necesita un diccionario cambiado, copia, cambia la copia y la devuelve.

## Ejercicios

Abre `ejercicios.py`. Cada función tiene un docstring con lo que debe hacer y un ejemplo. Borra la línea `raise NotImplementedError(...)` y escribe tu código.

Tres recordatorios para todos los ejercicios:

- La función debe **devolver** el resultado con `return`. Usar `print()` no cuenta: las pruebas revisan lo que la función devuelve.
- Usa los parámetros que recibe la función. No escribas valores fijos.
- No modifiques los diccionarios ni las listas que recibes.

Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_04_diccionarios -k ejercicio_1
```

Varias tablas de esta sección usan la misma lista de ejemplo, a la que llamaremos `pedidos`:

| id_pedido | ciudad | producto | cantidad | precio_unitario |
| --- | --- | --- | --- | --- |
| 1001 | Puebla | Café de olla | 2 | 185.0 |
| 1002 | Monterrey | Prensa francesa | 1 | 420.0 |
| 1003 | Puebla | Taza de barro | 4 | 95.5 |
| 1004 | Guadalajara | Café de olla | 3 | 185.0 |
| 1005 | Puebla | Filtro de tela | 3 | 35.1 |

Cada fila es un diccionario con esas cinco claves.

### Ejercicio 1. `crear_pedido(id_pedido, producto, cantidad, precio_unitario)`

Arma un diccionario con los cuatro datos recibidos. Las claves se llaman igual que los parámetros.

| Entrada | Resultado |
| --- | --- |
| `crear_pedido(1001, "Café de olla", 2, 185.0)` | `{'id_pedido': 1001, 'producto': 'Café de olla', 'cantidad': 2, 'precio_unitario': 185.0}` |

Paso a paso:

1. Escribe un diccionario con cuatro parejas de clave y valor.
2. En cada pareja, la clave es un texto y el valor es el parámetro del mismo nombre.
3. Devuelve el diccionario.

<details>
<summary>Pista 1</summary>

La clave lleva comillas porque es un texto. El valor no las lleva porque es una variable: quieres lo que el parámetro guarda, no su nombre.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba dice que las claves no coinciden, compáralas letra por letra con los nombres de los parámetros. Un guion bajo de menos basta para que sea otra clave.

</details>

### Ejercicio 2. `obtener_ciudad(pedido)`

Devuelve la ciudad del pedido. Si el pedido no tiene la clave `"ciudad"`, devuelve el texto `"sin ciudad"`.

| Entrada | Resultado |
| --- | --- |
| `obtener_ciudad({"id_pedido": 1001, "ciudad": "Puebla"})` | `'Puebla'` |
| `obtener_ciudad({"id_pedido": 1002})` | `'sin ciudad'` |

Paso a paso:

1. Lee la clave `"ciudad"` de una forma que no falle cuando la clave no existe.
2. Indica qué valor quieres recibir en ese caso.
3. Devuelve el resultado.

<details>
<summary>Pista 1</summary>

Si la prueba termina con `KeyError: 'ciudad'`, estás leyendo con corchetes. Vuelve al concepto 4.

</details>

<details>
<summary>Pista 2</summary>

El método que necesitas acepta dos valores entre los paréntesis: la clave y lo que debe devolver si la clave falta.

</details>

### Ejercicio 3. `agregar_total(pedido)`

Devuelve una **copia** del pedido con una clave nueva, `"total"`: la cantidad por el precio unitario, redondeada a dos decimales. El pedido original debe quedar como estaba, sin la clave `"total"`.

| Entrada | Resultado |
| --- | --- |
| `agregar_total({"cantidad": 2, "precio_unitario": 185.0})` | `{'cantidad': 2, 'precio_unitario': 185.0, 'total': 370.0}` |
| `agregar_total({"cantidad": 3, "precio_unitario": 35.1})` | `{'cantidad': 3, 'precio_unitario': 35.1, 'total': 105.3}` |

Paso a paso:

1. Crea una copia del pedido y guárdala en una variable.
2. Calcula el total con los valores del pedido y redondéalo a dos decimales.
3. Agrega el total a la copia, bajo la clave `"total"`.
4. Devuelve la copia.

<details>
<summary>Pista 1</summary>

Si la prueba dice que el original cambió, revisa a qué diccionario le agregaste la clave. Escribir `copia = pedido` no copia nada: solo le pone otro nombre al mismo diccionario.

</details>

<details>
<summary>Pista 2</summary>

Si obtienes `105.30000000000001`, falta el redondeo. Es el mismo problema de los decimales que viste en la lección 1.

</details>

### Ejercicio 4. `contar_por_ciudad(pedidos)`

Recibe una lista de pedidos y devuelve un diccionario con el número de pedidos de cada ciudad. Con una lista vacía devuelve un diccionario vacío.

| Entrada | Resultado |
| --- | --- |
| `contar_por_ciudad(pedidos)` | `{'Puebla': 3, 'Monterrey': 1, 'Guadalajara': 1}` |
| `contar_por_ciudad([])` | `{}` |

Paso a paso:

1. Crea un diccionario vacío para llevar la cuenta.
2. Recorre la lista de pedidos.
3. En cada vuelta, toma la ciudad del pedido.
4. Suma 1 a la cuenta de esa ciudad. Si es la primera vez que aparece, su cuenta parte de 0.
5. Al terminar el bucle, devuelve el diccionario.

<details>
<summary>Pista 1</summary>

Es el patrón de conteo del concepto 8. Allá el grupo era el estado; aquí es la ciudad.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba termina con `KeyError: 'Puebla'`, estás leyendo la cuenta de una ciudad que todavía no está en el diccionario. Necesitas una lectura que devuelva 0 cuando la clave falta.

</details>

<details>
<summary>Pista 3</summary>

Revisa la sangría del `return`. Si queda dentro del bucle, la función termina en la primera vuelta y solo cuenta un pedido.

</details>

### Ejercicio 5. `ventas_por_producto(pedidos)`

Devuelve un diccionario con el importe vendido de cada producto. El importe de un pedido es su cantidad por su precio unitario. Cada suma va redondeada a dos decimales.

| Entrada | Resultado |
| --- | --- |
| `ventas_por_producto(pedidos)` | `{'Café de olla': 925.0, 'Prensa francesa': 420.0, 'Taza de barro': 382.0, 'Filtro de tela': 105.3}` |
| `ventas_por_producto([])` | `{}` |

El Café de olla aparece en dos pedidos: 2 × 185.0 más 3 × 185.0 da 925.0.

Paso a paso:

1. Crea un diccionario vacío para las sumas.
2. Recorre la lista de pedidos.
3. En cada vuelta, toma el producto y calcula el importe del pedido.
4. Suma ese importe a lo que ya llevaba el producto. Si es la primera vez que aparece, parte de 0.
5. Cuando termine el bucle, recorre las claves del diccionario de sumas y reemplaza cada valor por su versión redondeada a dos decimales.
6. Devuelve el diccionario.

<details>
<summary>Pista 1</summary>

Es el patrón de suma por grupo del concepto 8. En lugar de sumar 1, sumas el importe.

</details>

<details>
<summary>Pista 2</summary>

Guarda el importe en su propia variable antes de acumularlo. La línea del acumulador queda más corta y se lee mejor.

</details>

<details>
<summary>Pista 3</summary>

Para el paso 5 necesitas un segundo bucle, después del primero y no dentro de él. Cambiar el valor de una clave que ya existe mientras recorres el diccionario está permitido.

</details>

### Ejercicio 6. `ciudades_unicas(pedidos)`

Devuelve una lista con las ciudades distintas que aparecen en los pedidos, sin repetidas y ordenada con `sorted()`. Con una lista vacía devuelve una lista vacía.

| Entrada | Resultado |
| --- | --- |
| `ciudades_unicas(pedidos)` | `['Guadalajara', 'Monterrey', 'Puebla']` |
| `ciudades_unicas([])` | `[]` |

Paso a paso:

1. Crea un conjunto vacío.
2. Recorre los pedidos y agrega al conjunto la ciudad de cada uno.
3. Ordena el conjunto. El resultado de ordenar ya es una lista.
4. Devuelve esa lista.

<details>
<summary>Pista 1</summary>

Un conjunto vacío no se escribe con llaves. Si la prueba menciona que un `dict` no tiene el método `add`, ese es el motivo.

</details>

<details>
<summary>Pista 2</summary>

No necesitas revisar si la ciudad ya está antes de agregarla. El conjunto ignora los repetidos por su cuenta.

</details>

> `sorted()` compara los textos carácter por carácter y coloca las letras con acento después de todas las letras sin acento. Por eso pone `'Monterrey'` antes que `'Mérida'`, al revés que un directorio. Para este curso, el orden de `sorted()` es el correcto: lo importante es que el resultado sea siempre el mismo.

### Ejercicio 7. `pedido_mas_grande(pedidos)`

Devuelve el pedido con el mayor importe (cantidad por precio unitario, redondeado a dos decimales). Se devuelve el diccionario completo, no el importe. Si la lista está vacía devuelve `None`. Si hay empate, devuelve el que aparece primero en la lista.

| Entrada | Resultado |
| --- | --- |
| `pedido_mas_grande(pedidos)` | El pedido 1004 completo: 3 × 185.0 = 555.0 |
| `pedido_mas_grande([])` | `None` |

Paso a paso:

1. Crea dos variables antes del bucle: una para el pedido mayor encontrado hasta el momento, que empieza en `None`, y otra para su importe.
2. Recorre la lista de pedidos.
3. En cada vuelta, calcula el importe del pedido, redondeado a dos decimales como en los ejercicios anteriores. Sin el redondeo, `3 * 0.1` vale `0.30000000000000004` y un empate real se decide mal.
4. Si todavía no hay un pedido mayor, o si este importe supera al mayor que llevas, guarda este pedido y su importe en las dos variables.
5. Al terminar el bucle, devuelve el pedido mayor.

<details>
<summary>Pista 1</summary>

Es el patrón del acumulador, pero en lugar de sumar, recuerdas al mejor que has visto. Con una lista vacía el bucle no da ninguna vuelta y la variable sigue valiendo `None`: ese caso se resuelve solo.

</details>

<details>
<summary>Pista 2</summary>

La condición del paso 4 tiene dos partes unidas con `or`. La primera pregunta si la variable del pedido mayor todavía es `None`.

</details>

<details>
<summary>Pista 3</summary>

Si falla la prueba del empate, revisa el operador de la comparación. Con `>=`, un pedido que iguala al mayor lo reemplaza y terminas devolviendo el último, no el primero.

</details>

## Evalúate

Cuando termines los siete ejercicios, corre la lección completa:

```bash
pytest lecciones/leccion_04_diccionarios
```

Debes ver `35 passed`. Si una prueba falla, lee la línea que empieza con `E`: te dice con qué valores se probó, qué se esperaba y qué devolvió tu función.

Revisa también el estilo de tu código:

```bash
ruff check lecciones/leccion_04_diccionarios
```

Y guarda tu trabajo:

```bash
git add .
git commit -m "Completa la lección 4"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Qué error aparece si lees con corchetes una clave que no existe?
2. ¿Qué devuelve `pedido.get("ciudad")` si el pedido no tiene esa clave? ¿Y `pedido.get("ciudad", "sin ciudad")`?
3. En un diccionario, ¿`in` busca entre las claves o entre los valores?
4. ¿Qué entrega `.items()` en cada vuelta de un `for`?
5. En `conteo[ciudad] = conteo.get(ciudad, 0) + 1`, ¿para qué sirve el `0`?
6. ¿Por qué se usa `sorted()` antes de devolver los valores de un conjunto?
7. Después de `copia = pedido`, ¿cuántos diccionarios hay? ¿Qué cambia si escribes `copia = pedido.copy()`?
8. De lecciones anteriores: ¿qué diferencia hay entre una lista y una tupla? ¿Y por qué redondeamos los importes con `round(valor, 2)`?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. Casi siempre trae la respuesta.
2. Prueba tu función a mano: abre el intérprete con `python` y llama a la función con el valor que falló.
3. Dentro de un bucle, imprime el diccionario acumulador en cada vuelta para ver cómo cambia. Borra ese `print()` cuando termines.
4. Revisa los ejemplos resueltos de `ejemplos.py`.
5. Abre las pistas del ejercicio, una a la vez.
6. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 6, "Dictionaries": crear, leer, agregar, modificar y borrar claves, el método `get()`, recorrer un diccionario y anidar diccionarios dentro de una lista.
- Bill Lubanovic, *Introducing Python*, capítulo 3, "Py Filling: Lists, Tuples, Dictionaries, and Sets": diccionarios y conjuntos.
- Reuven Lerner, *Python Workout*, 2.ª ed., capítulo 5, "Dictionaries and sets": ejercicios de conteo y de acumulación con diccionarios, y conjuntos para valores únicos.
- Felienne Hermans, *The Programmer's Brain*, capítulo 3, "How to learn programming syntax quickly": por qué intentar recordar antes de buscar y por qué conviene repasar espaciado.
