# Lección 2: Listas y bucles

En la lección 1 limpiaste un dato a la vez. Un archivo de pedidos trae miles. En esta lección aprendes a guardar muchos valores juntos en una lista y a repetir la misma operación sobre cada uno con un bucle.

**Tiempo estimado:** 120 minutos.
**Antes de empezar:** completa la [lección 1](../leccion_01_variables_y_texto/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Guardar varios valores en una lista y leerlos por su posición.
- Agregar, modificar, contar y ordenar elementos sin perder los datos originales.
- Recorrer una lista con un bucle `for` y entender qué hace la sangría.
- Construir un resultado paso a paso con el patrón acumulador.
- Obtener un tramo de una lista con un slice y resumirla con `sum`, `min` y `max`.

## Por qué importa en datos

Una columna de una tabla es una lista: todos los importes, todas las ciudades, todas las cantidades. Casi cualquier tarea de un flujo de datos se reduce a recorrer una lista y hacer algo con cada elemento: limpiarlo, convertirlo, sumarlo.

Hay además un cuidado que distingue al trabajo con datos: no destruir la información original. Si ordenas o corriges la lista que recibiste, ya no puedes volver a consultarla tal como llegó. Por eso en esta lección vas a distinguir las operaciones que cambian una lista de las que devuelven una nueva.

Las funciones que escribas aquí reaparecen en el proyecto final, donde calcularás los totales de un archivo completo de pedidos.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. No los copies y pegues: teclearlos es parte del aprendizaje.
2. Corre `python lecciones/leccion_02_listas_y_bucles/ejemplos.py` y cambia valores para ver qué pasa.
3. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno.
4. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

## Conceptos

### 1. Listas

Una lista es una colección de valores en orden, guardada bajo un solo nombre. Se escribe entre corchetes, con los elementos separados por comas.

```python
ciudades = ["Puebla", "Mérida", "Tijuana"]
importes = [450.0, 1250.5, 89.9, 780.0]
print(ciudades)
```

```text
['Puebla', 'Mérida', 'Tijuana']
```

Dos costumbres que ayudan a leer el código:

- El nombre de una lista va en plural: `ciudades`, `importes`. El de un solo elemento, en singular: `ciudad`, `importe`.
- Una lista sin elementos se escribe `[]`. Es un valor válido y lo vas a usar seguido.

### 2. Índices: la posición de cada elemento

Cada elemento tiene una posición, llamada índice. **Python cuenta desde 0**, no desde 1.

| Elemento | `"Puebla"` | `"Mérida"` | `"Tijuana"` |
| --- | --- | --- | --- |
| Índice | `0` | `1` | `2` |
| Índice desde el final | `-3` | `-2` | `-1` |

Para leer un elemento, escribe su índice entre corchetes después del nombre de la lista.

```python
ciudades = ["Puebla", "Mérida", "Tijuana"]
print(ciudades[0])
print(ciudades[2])
print(ciudades[-1])
```

```text
Puebla
Tijuana
Tijuana
```

El índice `-1` siempre da el último elemento, sin importar cuántos haya. Es la forma más segura de pedirlo, porque no necesitas saber la longitud de la lista.

### 3. Provoca el error: un índice que no existe

La lista tiene tres elementos y sus índices son 0, 1 y 2. Pide el índice 3:

```python
ciudades = ["Puebla", "Mérida", "Tijuana"]
print(ciudades[3])
```

Python responde:

```text
Traceback (most recent call last):
  File "prueba.py", line 2, in <module>
    print(ciudades[3])
          ~~~~~~~~^^^
IndexError: list index out of range
```

Léelo de abajo hacia arriba, como en la lección 1:

1. **Última línea:** `IndexError` significa que pediste una posición que la lista no tiene. *Out of range* quiere decir "fuera del rango".
2. **Línea con `File`:** el archivo y el renglón donde ocurrió.
3. **El renglón señalado:** las marcas apuntan al índice que falló.

Este error casi siempre viene de contar desde 1. Cuando lo veas, revisa cuántos elementos tiene la lista y recuerda que el último índice es la longitud menos 1. También aparece al pedir cualquier índice, incluso el `-1`, a una lista vacía.

### 4. Modificar, agregar y contar

Para cambiar un elemento, asígnale un valor nuevo a su índice. Para agregar uno al final, usa el método `.append()`. Para saber cuántos hay, usa `len()`.

```python
ciudades = ["Puebla", "Merida", "Tijuana"]
ciudades[1] = "Mérida"
ciudades.append("Monterrey")
print(ciudades)
print(len(ciudades))
```

```text
['Puebla', 'Mérida', 'Tijuana', 'Monterrey']
4
```

Aquí hay una diferencia importante con la lección 1. Los métodos de texto devuelven un texto nuevo y dejan el original intacto. **Las listas sí se pueden cambiar**: `.append()` modifica la lista misma y no devuelve nada, así que no hace falta guardar su resultado.

```python
ciudades.append("Monterrey")  # correcto: la lista crece
ciudades = ciudades.append("Monterrey")  # error: ciudades deja de ser una lista
```

### 5. Ordenar: `sorted()` frente a `.sort()`

Hay dos formas de ordenar y hacen cosas distintas con la lista original.

| Forma | Qué hace con la original | Qué devuelve |
| --- | --- | --- |
| `sorted(lista)` | La deja como estaba | Una lista nueva, ordenada |
| `lista.sort()` | La cambia | Nada |

```python
importes = [450.0, 1250.5, 89.9, 780.0]
ordenados = sorted(importes)
print(ordenados)
print(importes)
```

```text
[89.9, 450.0, 780.0, 1250.5]
[450.0, 1250.5, 89.9, 780.0]
```

La lista `importes` conserva el orden en que llegó. Con `.sort()` ese orden se pierde:

```python
importes = [450.0, 1250.5, 89.9, 780.0]
importes.sort()
print(importes)
```

```text
[89.9, 450.0, 780.0, 1250.5]
```

Para ordenar de mayor a menor, las dos formas aceptan `reverse=True`:

```python
importes = [450.0, 1250.5, 89.9, 780.0]
print(sorted(importes, reverse=True))
```

```text
[1250.5, 780.0, 450.0, 89.9]
```

En datos, prefiere `sorted()`. El orden original suele significar algo (por ejemplo, el orden en que se hicieron los pedidos) y otra parte del programa puede necesitarlo.

> Los textos se ordenan alfabéticamente, pero las mayúsculas van antes que las minúsculas: `sorted(["puebla", "Tijuana", "Mérida"])` da `['Mérida', 'Tijuana', 'puebla']`. Es una razón más para limpiar los textos antes de ordenarlos.

### 6. El bucle `for`

Un bucle repite las mismas líneas una vez por cada elemento de la lista.

```python
ciudades = ["Puebla", "Mérida", "Tijuana"]
for ciudad in ciudades:
    print(f"Envío a {ciudad}")
```

```text
Envío a Puebla
Envío a Mérida
Envío a Tijuana
```

Se lee así: "para cada `ciudad` en `ciudades`, haz lo siguiente". Python toma el primer elemento, lo guarda en la variable `ciudad` y ejecuta las líneas con sangría. Luego toma el segundo y repite, hasta que la lista se acaba.

Tres detalles de la primera línea:

- `ciudad` es una variable que tú nombras. Podría llamarse de cualquier forma, pero el singular de la lista es lo más claro.
- Termina con dos puntos (`:`). Si los olvidas, Python responde `SyntaxError: expected ':'`.
- Si la lista está vacía, las líneas del bucle no se ejecutan ninguna vez. No es un error.

### 7. La sangría decide qué se repite

La sangría son los espacios al inicio de una línea. En Python no es decoración: **las líneas con sangría debajo del `for` pertenecen al bucle y se repiten; la primera línea sin sangría ya está fuera y se ejecuta una sola vez**, cuando el bucle termina.

```python
ciudades = ["Puebla", "Mérida", "Tijuana"]
for ciudad in ciudades:
    print(f"Envío a {ciudad}")
print("Fin de los envíos")
```

```text
Envío a Puebla
Envío a Mérida
Envío a Tijuana
Fin de los envíos
```

**Provoca el error.** Escribe el bucle sin sangría:

```python
ciudades = ["Puebla", "Mérida", "Tijuana"]
for ciudad in ciudades:
print(ciudad)
```

```text
  File "prueba.py", line 3
    print(ciudad)
    ^^^^^
IndentationError: expected an indented block after 'for' statement on line 2
```

`IndentationError` es un error de sangría. El mensaje dice que, después del `for` del renglón 2, Python esperaba un bloque con sangría y no lo encontró. Fíjate en que no hay `Traceback`: Python revisa la sangría antes de ejecutar el programa, así que ninguna línea llegó a correr.

**El error que no avisa.** Más peligroso es el caso contrario: una línea que debía repetirse y quedó fuera del bucle. El programa corre sin quejarse y entrega un resultado equivocado.

```python
ciudades = ["Puebla", "Mérida", "Tijuana"]
for ciudad in ciudades:
    print(f"Preparando envío a {ciudad}")
print(f"Envío a {ciudad} listo")
```

```text
Preparando envío a Puebla
Preparando envío a Mérida
Preparando envío a Tijuana
Envío a Tijuana listo
```

Solo Tijuana aparece como lista, porque la última línea se ejecutó una vez, al terminar el bucle, cuando `ciudad` guardaba el último elemento. Python no puede saber qué querías: las dos versiones son código válido. A esto se le llama error lógico, y la única defensa es comprobar el resultado. Para eso están las pruebas.

Lo mismo pasa al revés, y te va a importar en los ejercicios: si escribes el `return` de una función con la sangría del bucle, la función termina en la primera vuelta y devuelve un resultado a medias. El `return` va alineado con el `for`, no dentro de él.

### 8. El patrón acumulador

Es el patrón más usado al procesar datos. Tiene tres partes:

1. **Antes del bucle**, crea una variable con un valor inicial.
2. **Dentro del bucle**, actualízala con cada elemento.
3. **Después del bucle**, úsala: ya contiene el resultado.

**Para sumar**, el acumulador empieza en `0`:

```python
importes = [450.0, 1250.5, 89.9, 780.0]
total = 0
for importe in importes:
    total = total + importe
print(total)
```

```text
2570.4
```

La línea `total = total + importe` se lee de derecha a izquierda: "toma lo que llevas, súmale este importe y guárdalo otra vez en `total`".

**Para construir una lista nueva**, el acumulador empieza como lista vacía y crece con `.append()`:

```python
productos_crudos = ["  café de olla", "TAZA DE BARRO ", " filtro de tela "]
productos_limpios = []
for producto in productos_crudos:
    productos_limpios.append(producto.strip().lower())
print(productos_limpios)
print(productos_crudos)
```

```text
['café de olla', 'taza de barro', 'filtro de tela']
['  café de olla', 'TAZA DE BARRO ', ' filtro de tela ']
```

La lista original queda intacta y el resultado vive en una lista nueva. Así se limpia una columna completa.

El error típico de este patrón es crear el acumulador dentro del bucle. Entonces se reinicia en cada vuelta y al final solo recuerda el último elemento.

### 9. `range`: una serie de números

`range(n)` produce los enteros desde 0 hasta `n - 1`. El número que escribes no se incluye.

```python
for numero in range(3):
    print(numero)
```

```text
0
1
2
```

Con dos números, `range(1, 4)` empieza en 1 y termina en 3.

Su uso más común con listas es `range(len(lista))`, que produce justo los índices de la lista. Lo necesitas cuando tienes dos listas relacionadas por posición, como dos columnas de la misma tabla:

```python
productos = ["Café de olla", "Taza de barro", "Filtro de tela"]
existencias = [12, 0, 30]
for posicion in range(len(productos)):
    print(f"{productos[posicion]}: {existencias[posicion]} piezas")
```

```text
Café de olla: 12 piezas
Taza de barro: 0 piezas
Filtro de tela: 30 piezas
```

Si solo necesitas los elementos de una lista, recórrela directamente con `for elemento in lista`. Usa los índices solo cuando de verdad necesites la posición.

### 10. Resumir una lista: `sum`, `min` y `max`

Para las cuentas más comunes Python ya trae funciones hechas.

| Función | Qué devuelve | Con `[450.0, 1250.5, 89.9, 780.0]` |
| --- | --- | --- |
| `sum(lista)` | La suma de los elementos | `2570.4` |
| `min(lista)` | El menor | `89.9` |
| `max(lista)` | El mayor | `1250.5` |
| `len(lista)` | Cuántos elementos hay | `4` |

`sum()` hace por dentro lo mismo que tu bucle acumulador. Conviene saber escribir el bucle, porque el patrón sirve para muchas cosas que `sum()` no resuelve, y usar `sum()` cuando lo único que necesitas es sumar.

### 11. Slices: un tramo de la lista

Un slice toma una parte de la lista. Se escribe `lista[inicio:fin]` y devuelve una **lista nueva** con los elementos desde el índice `inicio` hasta el anterior a `fin`. Igual que en `range`, el final no se incluye.

```python
importes = [450.0, 1250.5, 89.9, 780.0]
print(importes[1:3])
print(importes[:2])
print(importes[2:])
print(importes[-2:])
```

```text
[1250.5, 89.9]
[450.0, 1250.5]
[89.9, 780.0]
[89.9, 780.0]
```

| Slice | Significado |
| --- | --- |
| `lista[1:3]` | Los elementos de los índices 1 y 2 |
| `lista[:2]` | Los primeros dos |
| `lista[2:]` | Desde el índice 2 hasta el final |
| `lista[-2:]` | Los últimos dos |

A diferencia de un índice, un slice que pide más de lo que hay no lanza error: devuelve lo que encuentra. `importes[:10]` da los cuatro elementos y `importes[5:]` da `[]`.

### 12. Copiar una lista no es lo mismo que asignarla

Con textos y números, asignar una variable a otra no trae sorpresas. Con listas sí: **el signo `=` no copia la lista, le pone un segundo nombre a la misma**.

```python
pedidos = [1001, 1002, 1003]
misma_lista = pedidos
copia = pedidos[:]

pedidos.append(1004)

print(misma_lista)
print(copia)
```

```text
[1001, 1002, 1003, 1004]
[1001, 1002, 1003]
```

`misma_lista` cambió aunque nunca la tocaste, porque es la misma lista con otro nombre. `copia` no cambió: el slice `[:]`, sin inicio ni fin, devuelve una lista nueva con todos los elementos.

Esto explica por qué una función puede dañar los datos de quien la llama. La lista que recibe como parámetro es la misma que existe afuera, no una copia. Si dentro de la función usas `.sort()` o `.append()` sobre ella, cambias la original. Por eso las pruebas de esta lección revisan que tus funciones no modifiquen lo que reciben.

### 13. Tuplas: una lista que no cambia

Una tupla es como una lista, pero una vez creada no se puede modificar. Se escribe con paréntesis en lugar de corchetes.

```python
estados = ("entregado", "enviado", "cancelado")
print(estados[0])
print(len(estados))
```

```text
entregado
3
```

Los índices, `len()`, los slices y el bucle `for` funcionan igual. Lo que no puedes hacer es cambiarla:

```python
estados[0] = "pendiente"
```

```text
TypeError: 'tuple' object does not support item assignment
```

Usa una tupla para valores que no deben cambiar mientras el programa corre, como los estados válidos de un pedido.

Las tuplas también sirven para que una función devuelva dos valores a la vez. Los paréntesis son opcionales: basta separar los valores con una coma.

```python
def menor_y_mayor(importes):
    return min(importes), max(importes)


print(menor_y_mayor([450.0, 1250.5, 89.9, 780.0]))
```

```text
(89.9, 1250.5)
```

### 14. Estilo: sangría y longitud de línea

La guía de estilo de Python se llama PEP 8. De ella, lo que aplica a esta lección:

- **Cuatro espacios por nivel de sangría.** Nunca mezcles espacios y tabuladores. Los editores modernos escriben cuatro espacios cuando presionas la tecla Tab; comprueba que el tuyo lo haga.
- **Líneas cortas.** PEP 8 recomienda un máximo de 79 caracteres. En este curso el límite es 88, que es el que revisa `ruff`.
- **Una lista larga se puede partir en varias líneas**, un elemento por línea y con coma al final de cada uno:

```python
ciudades = [
    "Ciudad de México",
    "Guadalajara",
    "Monterrey",
]
```

No necesitas memorizar las reglas: `ruff check` te avisa cuando una línea se pasa o la sangría no es consistente.

## Ejercicios

Abre `ejercicios.py`. Cada función tiene un docstring con lo que debe hacer y un ejemplo. Borra la línea `raise NotImplementedError(...)` y escribe tu código.

Tres recordatorios para todos los ejercicios:

- La función debe **devolver** el resultado con `return`. Usar `print()` no cuenta: las pruebas revisan lo que la función devuelve.
- El `return` va después del bucle, alineado con el `for`. Dentro del bucle termina la función en la primera vuelta.
- No modifiques las listas que recibe la función. Si necesitas una lista distinta, crea una nueva.

Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_02_listas_y_bucles -k ejercicio_1
```

### Ejercicio 1. `primero_y_ultimo(valores)`

Devuelve una tupla con el primer y el último elemento de la lista. Sirve para echar un vistazo a una columna: por ejemplo, el primer y el último número de pedido de un archivo. La lista siempre trae al menos un elemento.

| Entrada | Resultado |
| --- | --- |
| `primero_y_ultimo([1001, 1002, 1003])` | `(1001, 1003)` |
| `primero_y_ultimo(["Puebla", "Mérida"])` | `('Puebla', 'Mérida')` |
| `primero_y_ultimo(["Café de olla"])` | `('Café de olla', 'Café de olla')` |

Paso a paso:

1. Toma el primer elemento por su índice.
2. Toma el último elemento con un índice que funcione para listas de cualquier longitud.
3. Devuelve los dos valores juntos, como tupla.

<details>
<summary>Pista 1</summary>

Para el último elemento no necesitas saber cuántos hay. Revisa la fila "Índice desde el final" de la tabla de índices.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba dice que devolviste una lista, revisa los símbolos que rodean tus dos valores. La sección de tuplas muestra cómo una función devuelve dos valores a la vez.

</details>

### Ejercicio 2. `sumar_importes(importes)`

Suma todos los importes de la lista y redondea el total a dos decimales. Si la lista está vacía, el resultado es `0`.

Resuélvelo con un bucle acumulador, sin `sum()`. El objetivo es practicar el patrón, que vas a usar en todo el curso.

| Entrada | Resultado |
| --- | --- |
| `sumar_importes([100, 250.5, 49.5])` | `400.0` |
| `sumar_importes([0.1, 0.1, 0.1])` | `0.3` |
| `sumar_importes([])` | `0` |

Paso a paso:

1. Antes del bucle, crea el acumulador con su valor inicial.
2. Recorre la lista y suma cada importe al acumulador.
3. Después del bucle, redondea el acumulador a dos decimales y devuélvelo.

<details>
<summary>Pista 1</summary>

Si la prueba de la lista vacía falla, piensa qué valor tiene tu acumulador cuando el bucle no da ninguna vuelta. Ese valor inicial es justo lo que la función devuelve en ese caso.

</details>

<details>
<summary>Pista 2</summary>

Si obtienes solo el primer importe, tu `return` quedó dentro del bucle. Si obtienes solo el último, estás creando el acumulador dentro del bucle. Revisa la sangría de ambas líneas.

</details>

### Ejercicio 3. `limpiar_ciudades(ciudades)`

Devuelve una lista **nueva** en la que cada ciudad queda sin espacios en los extremos y con mayúscula inicial en cada palabra. La lista original no debe cambiar.

| Entrada | Resultado |
| --- | --- |
| `limpiar_ciudades(["  puebla ", "MÉRIDA"])` | `['Puebla', 'Mérida']` |
| `limpiar_ciudades([" ciudad de méxico"])` | `['Ciudad De México']` |
| `limpiar_ciudades([])` | `[]` |

Paso a paso:

1. Antes del bucle, crea una lista vacía para las ciudades limpias.
2. Recorre la lista que recibiste.
3. En cada vuelta, limpia el texto y agrégalo a la lista nueva.
4. Después del bucle, devuelve la lista nueva.

<details>
<summary>Pista 1</summary>

Es el patrón acumulador con una lista, como el ejemplo de los productos en la sección 8. Los dos métodos de texto que necesitas ya los usaste en la lección 1.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba dice que la función devolvió `None`, revisa si estás devolviendo el resultado de `.append()` en lugar de la lista. Ese método no devuelve nada.

</details>

### Ejercicio 4. `calcular_totales(cantidades, precios)`

Recibe dos listas del mismo tamaño: las cantidades y los precios unitarios de varios pedidos. La posición 0 de una corresponde a la posición 0 de la otra. Devuelve una lista nueva con el total de cada pedido (cantidad por precio), redondeado a dos decimales.

| Entrada | Resultado |
| --- | --- |
| `calcular_totales([2, 1], [45.5, 1250.0])` | `[91.0, 1250.0]` |
| `calcular_totales([3], [0.1])` | `[0.3]` |
| `calcular_totales([], [])` | `[]` |

Paso a paso:

1. Antes del bucle, crea una lista vacía para los totales.
2. Recorre las posiciones de las listas, no sus elementos.
3. En cada vuelta, toma la cantidad y el precio de esa posición, multiplícalos y redondea.
4. Agrega el total a la lista nueva.
5. Después del bucle, devuelve la lista de totales.

<details>
<summary>Pista 1</summary>

Para tomar un elemento de cada lista en la misma vuelta necesitas el índice. La sección de `range` tiene un ejemplo con dos listas relacionadas por posición.

</details>

<details>
<summary>Pista 2</summary>

Guarda el total de cada vuelta en una variable antes de agregarlo. Si la prueba muestra un valor como `0.30000000000000004`, falta redondear cada total.

</details>

### Ejercicio 5. `los_mas_altos(importes, n)`

Devuelve los `n` importes más altos, ordenados de mayor a menor. La lista original no debe cambiar. Si `n` es mayor que la cantidad de importes, devuelve todos.

| Entrada | Resultado |
| --- | --- |
| `los_mas_altos([450.0, 1250.5, 89.9, 780.0], 2)` | `[1250.5, 780.0]` |
| `los_mas_altos([500, 200, 500, 100], 2)` | `[500, 500]` |
| `los_mas_altos([89.9, 450.0], 5)` | `[450.0, 89.9]` |

Paso a paso:

1. Obtén una lista nueva con los importes ordenados de mayor a menor.
2. Toma de esa lista los primeros `n` elementos.
3. Devuelve ese tramo.

<details>
<summary>Pista 1</summary>

Si falla la prueba que revisa la lista original, estás ordenando con la forma que la cambia. Vuelve a la tabla de la sección 5.

</details>

<details>
<summary>Pista 2</summary>

Dentro de un slice puedes usar una variable en lugar de un número. Y no necesitas un caso especial para cuando `n` es muy grande: recuerda cómo se comporta un slice que pide de más.

</details>

### Ejercicio 6. `importe_promedio(importes)`

Devuelve el promedio de los importes, redondeado a dos decimales. La lista siempre trae al menos un importe, así que no necesitas revisar si está vacía.

| Entrada | Resultado |
| --- | --- |
| `importe_promedio([100, 200, 300])` | `200.0` |
| `importe_promedio([100, 100, 101])` | `100.33` |
| `importe_promedio([45.5])` | `45.5` |

Paso a paso:

1. Obtén la suma de los importes.
2. Obtén cuántos importes hay.
3. Divide la suma entre la cantidad.
4. Redondea a dos decimales y devuelve.

<details>
<summary>Pista</summary>

Aquí ya puedes usar las funciones de la sección 10: una te da la suma y otra la cantidad. No hace falta un bucle.

</details>

## Evalúate

Cuando termines los seis ejercicios, corre la lección completa:

```bash
pytest lecciones/leccion_02_listas_y_bucles
```

Debes ver `36 passed`. Si una prueba falla, lee la línea que empieza con `E`: te dice con qué valores se probó, qué se esperaba y qué devolvió tu función.

Revisa también el estilo de tu código:

```bash
ruff check lecciones/leccion_02_listas_y_bucles
```

Y guarda tu trabajo:

```bash
git add .
git commit -m "Completa la lección 2"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Qué índice tiene el primer elemento de una lista? ¿Y con qué índice pides el último sin saber cuántos hay?
2. ¿Qué tipo de error aparece si pides un índice que la lista no tiene?
3. ¿Qué diferencia hay entre `sorted(importes)` e `importes.sort()`?
4. En un bucle `for`, ¿cómo sabe Python qué líneas se repiten y cuáles no?
5. ¿Cuáles son las tres partes del patrón acumulador?
6. Después de `copia = pedidos`, ¿cuántas listas hay? ¿Qué cambia si escribes `copia = pedidos[:]`?
7. De la lección 1: ¿por qué `ciudad.strip()` en una línea sola no cambia la variable `ciudad`, y en cambio `ciudades.append("Puebla")` sí cambia la lista?
8. De la lección 1: ¿qué tipo de error aparece si intentas `float("$10")`?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. Casi siempre trae la respuesta.
2. Prueba tu función a mano: abre el intérprete con `python` y llama a la función con el valor que falló.
3. Agrega un `print()` temporal dentro del bucle para ver cuánto vale tu acumulador en cada vuelta. Bórralo cuando termines.
4. Revisa los ejemplos resueltos de `ejemplos.py`.
5. Abre las pistas del ejercicio, una a la vez.
6. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 3, "Introducing Lists": índices desde 0 e índice -1, modificar y agregar elementos, `sorted()` frente a `.sort()`, `len()` y cómo evitar un `IndexError`.
- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 4, "Working with Lists": bucles `for`, errores de sangría, `range`, `sum`, `min` y `max`, slices, copia de listas, tuplas y estilo PEP 8.
- Reuven Lerner, *Python Workout*, 2.ª ed., capítulo 4, "Lists and tuples": formato de ejercicio con enunciado, razonamiento y variantes.
- Felienne Hermans, *The Programmer's Brain*, capítulo 3, "How to learn programming syntax quickly" (recuperación y repaso espaciado), y capítulo 7, "Misconceptions: Bugs in thinking" (ideas equivocadas que se arrastran de un concepto a otro, como creer que asignar una lista la copia).
