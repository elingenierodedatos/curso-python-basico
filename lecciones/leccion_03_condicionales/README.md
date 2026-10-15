# Lección 3: Decisiones con if y bucles while

Hasta ahora tu código hace lo mismo con todos los datos. Pero un pedido cancelado no se cobra, una cantidad negativa no es válida y una celda con `"N/D"` no es una ciudad. En esta lección tu código aprende a preguntar antes de actuar y a repetir mientras haga falta.

**Tiempo estimado:** 100 minutos.
**Antes de empezar:** completa la [lección 2](../leccion_02_listas_y_bucles/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Escribir comparaciones y combinarlas con `and`, `or` y `not`.
- Tomar decisiones con `if`, `elif` y `else`, cuidando el orden de las condiciones.
- Reconocer un dato faltante, incluido `None`.
- Filtrar y contar los elementos de una lista con un `if` dentro de un `for`.
- Repetir con `while`, salir con `break` y detener un bucle que no termina.

## Por qué importa en datos

Limpiar datos es, sobre todo, decidir: este valor sirve, este no; este pedido entra al reporte, este se descarta; `"ENTREGADA "` y `"entregado"` son el mismo estado. Cada una de esas reglas se escribe con una condición.

Una regla mal escrita no siempre produce un error. A veces el programa corre, entrega un resultado y el resultado está mal. Por eso aquí practicas también los límites exactos de cada regla: qué pasa justo en 500, justo en cero, justo cuando la lista está vacía.

La lógica de `es_faltante()` y `normalizar_estado()` que escribas en esta lección es la base del proyecto final, aunque allí no siempre tenga los mismos nombres: `es_faltante()` reaparece tal cual en el módulo de limpieza, y los sinónimos de cada estado, en lugar de una cadena de `elif`, se guardan en un diccionario llamado `ESTADOS`.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. No los copies y pegues: teclearlos es parte del aprendizaje.
2. Corre `python lecciones/leccion_03_condicionales/ejemplos.py` y cambia valores para ver qué pasa.
3. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno.
4. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

## Conceptos

### 1. Valores booleanos y comparaciones

Una comparación es una pregunta que solo tiene dos respuestas: `True` (verdadero) o `False` (falso). Esos dos valores forman un tipo propio, `bool`, y se escriben con mayúscula inicial y sin comillas.

```python
cantidad = 3
print(cantidad == 3)
print(cantidad > 10)
```

```text
True
False
```

| Operador | Pregunta | Ejemplo | Resultado |
| --- | --- | --- | --- |
| `==` | ¿Son iguales? | `3 == 3` | `True` |
| `!=` | ¿Son distintos? | `3 != 3` | `False` |
| `<` | ¿Es menor? | `3 < 5` | `True` |
| `<=` | ¿Es menor o igual? | `5 <= 5` | `True` |
| `>` | ¿Es mayor? | `3 > 5` | `False` |
| `>=` | ¿Es mayor o igual? | `3 >= 5` | `False` |

El resultado de una comparación es un valor como cualquier otro: puedes guardarlo en una variable.

```python
precio_unitario = 45.5
es_caro = precio_unitario >= 100
print(es_caro)
```

```text
False
```

**Estilo:** deja un espacio a cada lado del operador. `cantidad >= 10` se lee mejor que `cantidad>=10`.

### 2. Provoca el error: `=` no es `==`

Un solo signo `=` **guarda** un valor en una variable. Dos signos `==` **preguntan** si dos valores son iguales. Confundirlos es el error más común de este tema. Escribe esto tal cual en un archivo de prueba:

```python
estado = "entregado"
if estado = "entregado":
    print("Pedido completo")
```

Python responde:

```text
  File "prueba.py", line 2
    if estado = "entregado":
       ^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

`SyntaxError` significa que el código está mal escrito y Python no pudo ni empezar a correrlo. Fíjate en dos cosas:

1. No hay `Traceback`, porque ninguna línea llegó a ejecutarse, ni siquiera la primera.
2. El mensaje sugiere la corrección: "quizá quisiste escribir `==`". La otra opción que menciona, `:=`, no se usa en este curso.

Cambia el `=` de la línea 2 por `==` y el programa funciona.

### 3. Comparar texto y comparar tipos distintos

Para Python, dos textos son iguales solo si coinciden carácter por carácter. Las mayúsculas y los espacios cuentan.

```python
ciudad_cruda = "  PUEBLA "
print(ciudad_cruda == "puebla")
print(ciudad_cruda.strip().lower() == "puebla")
```

```text
False
True
```

Por eso la regla es **limpiar antes de comparar**: primero `.strip().lower()`, como en la lección 1, y después la comparación.

Ahora provoca el segundo error de la lección. Las cantidades de un archivo llegan como texto, y es fácil olvidarlo:

```python
cantidad = "5"
print(cantidad > 3)
```

```text
Traceback (most recent call last):
  File "prueba.py", line 2, in <module>
    print(cantidad > 3)
          ^^^^^^^^^^^^
TypeError: '>' not supported between instances of 'str' and 'int'
```

`TypeError` significa que la operación no existe para esos tipos: Python no sabe decidir si un texto (`str`) es mayor que un número (`int`). La solución es convertir antes de comparar: `int(cantidad) > 3`.

Con `==` no hay error, pero la respuesta puede sorprenderte: `"5" == 5` da `False`, porque un texto nunca es igual a un número.

**Preguntar por el tipo antes de comparar.** Cuando no sabes qué tipo trae un valor, `isinstance(valor, int)` responde `True` si es un entero y `False` si no lo es. Sirve para evitar el `TypeError` de arriba: primero preguntas si es un número y solo después lo comparas.

```python
print(isinstance(5, int))
print(isinstance("5", int))
print(isinstance(2.5, int))
```

```text
True
False
False
```

Hay un detalle que sorprende: para Python, `True` y `False` también son enteros (`True` vale `1` y `False` vale `0`), así que `isinstance(True, int)` da `True`. Para rechazar los booleanos hace falta combinar dos preguntas; lo verás al final del concepto 4.

### 4. Combinar condiciones: `and`, `or`, `not`

| Operador | Es `True` cuando... | Ejemplo | Resultado |
| --- | --- | --- | --- |
| `and` | se cumplen las dos condiciones | `3 > 0 and 3 < 10` | `True` |
| `or` | se cumple al menos una | `3 > 5 or 3 < 10` | `True` |
| `not` | la condición es falsa | `not 3 > 5` | `True` |

```python
cantidad = 3
precio_unitario = 45.5
estado = "entregado"

print(cantidad > 0 and precio_unitario > 0)
print(estado == "enviado" or estado == "entregado")
print(not estado == "cancelado")
```

```text
True
True
True
```

Cada lado de un `and` o de un `or` debe ser una comparación completa. `estado == "enviado" or "entregado"` no pregunta lo que parece; hay que repetir `estado ==` del otro lado.

**Python evalúa de izquierda a derecha y se detiene en cuanto conoce la respuesta.** En un `and`, si la primera condición es falsa, la segunda ya no se revisa. Eso sirve para proteger una comparación que podría fallar: pon primero la condición que comprueba que es seguro seguir.

**Aceptar enteros, pero no booleanos.** Con `and` y `not` ya puedes resolver el detalle del concepto 3: pide que el valor sea un entero **y** que **no** sea un booleano.

```python
valor = True
print(isinstance(valor, int))
print(isinstance(valor, int) and not isinstance(valor, bool))
```

```text
True
False
```

### 5. Pertenencia: `in` y `not in`

`in` pregunta si un valor está dentro de una lista.

```python
ciudades_con_envio = ["Guadalajara", "Monterrey", "Puebla"]

print("Puebla" in ciudades_con_envio)
print("Tijuana" in ciudades_con_envio)
print("Tijuana" not in ciudades_con_envio)
```

```text
True
False
True
```

Con una lista, `in` busca un elemento **idéntico**. Es la forma corta de escribir varias comparaciones unidas con `or`.

Con un texto, `in` pregunta si un fragmento aparece dentro de otro:

```python
print("olla" in "Café de olla")
```

```text
True
```

No son la misma pregunta. `"na" in ["na", "null"]` busca el elemento `"na"`; `"na" in "canal"` busca las letras `na` dentro de otra palabra, y también da `True`.

### 6. `if` y `else`

`if` corre un bloque de código solo cuando su condición es verdadera. La línea termina en dos puntos y el bloque va con sangría de cuatro espacios, igual que en un `for`.

```python
estado = "cancelado"

if estado == "cancelado":
    print("El pedido no se cobra")
```

```text
El pedido no se cobra
```

Si la condición es falsa, Python se salta el bloque y sigue con lo que haya después.

Con `else` agregas el camino contrario. Siempre corre uno de los dos bloques, nunca ambos:

```python
estado = "entregado"

if estado == "cancelado":
    mensaje = "El pedido no se cobra"
else:
    mensaje = "El pedido se cobra"

print(mensaje)
```

```text
El pedido se cobra
```

### 7. `elif`: más de dos caminos, y el orden importa

Cuando hay más de dos opciones se usa `elif` ("si no, y si..."). Python revisa las condiciones de arriba hacia abajo, corre **solo el primer bloque cuya condición sea verdadera** y se salta todo lo demás.

```python
piezas = 12

if piezas >= 10:
    tipo_de_venta = "mayoreo"
elif piezas >= 5:
    tipo_de_venta = "medio mayoreo"
else:
    tipo_de_venta = "menudeo"

print(tipo_de_venta)
```

```text
mayoreo
```

Ahora mira el mismo código con las dos primeras condiciones en otro orden:

```python
piezas = 12

if piezas >= 5:
    tipo_de_venta = "medio mayoreo"
elif piezas >= 10:
    tipo_de_venta = "mayoreo"
else:
    tipo_de_venta = "menudeo"

print(tipo_de_venta)
```

```text
medio mayoreo
```

No aparece ningún error, y el resultado está mal. Doce también es mayor o igual que cinco, así que gana el primer bloque y el de `mayoreo` nunca se revisa. Esto se llama **error lógico**: Python no lo detecta, solo lo encuentras al comprobar el resultado. Para eso están las pruebas.

Dos reglas para evitarlo:

- Al clasificar por rangos, ordena las condiciones de un extremo al otro: de la más exigente a la menos exigente.
- Prueba siempre los valores que caen justo en un límite. Ahí se esconden casi todos los errores con `<` y `<=`.

El `else` final es opcional. Úsalo cuando quieras un resultado para "todo lo demás".

### 8. `None`: no hay valor

`None` es el valor que Python usa para decir "aquí no hay nada". No es cero ni un texto vacío: es la ausencia de dato. Se escribe con mayúscula inicial y sin comillas.

```python
fecha_de_entrega = None

if fecha_de_entrega is None:
    print("El pedido todavía no se entrega")
```

```text
El pedido todavía no se entrega
```

Para preguntar por `None` se usa `is None` (o `is not None`), no `==`.

`None` no tiene métodos de texto. Si intentas `fecha_de_entrega.strip()` obtienes `AttributeError: 'NoneType' object has no attribute 'strip'`. Cuando un valor puede ser `None`, pregunta eso primero y limpia después.

### 9. Un `if` dentro de un `for`: filtrar y contar

Aquí se juntan esta lección y la anterior. El `for` recorre la lista; el `if` decide qué hacer con cada elemento. Observa que el bloque del `if` lleva dos niveles de sangría.

**Filtrar** es el patrón acumulador con una condición: empiezas con una lista vacía y agregas solo lo que cumple.

```python
cantidades = [3, 0, 12, -1, 5]
cantidades_validas = []

for valor in cantidades:
    if valor > 0:
        cantidades_validas.append(valor)

print(cantidades_validas)
```

```text
[3, 12, 5]
```

**Contar** es lo mismo con un número: empiezas en cero y sumas uno cada vez que se cumple la condición.

```python
estados = ["entregado", "cancelado", "enviado", "cancelado", "entregado"]
cancelados = 0

for estado_del_pedido in estados:
    if estado_del_pedido == "cancelado":
        cancelados += 1

print(cancelados)
```

```text
2
```

`cancelados += 1` es la forma corta de `cancelados = cancelados + 1`. También existe `-=` para restar.

### 10. El bucle `while`

`while` repite un bloque **mientras** su condición sea verdadera. Antes de cada vuelta revisa la condición; cuando es falsa, el bucle termina.

```python
contador = 1

while contador <= 3:
    print("Intento", contador)
    contador += 1
```

```text
Intento 1
Intento 2
Intento 3
```

Un `while` con contador tiene tres partes: el valor inicial (`contador = 1`), la condición (`contador <= 3`) y el avance (`contador += 1`).

**Provoca un bucle infinito.** Borra la línea del avance y corre el código:

```python
contador = 1

while contador <= 3:
    print("Intento", contador)
```

La pantalla se llena de `Intento 1` y no se detiene: como `contador` nunca cambia, la condición nunca deja de cumplirse. Para detenerlo presiona **Ctrl+C** en la terminal (también en macOS es Ctrl, no Cmd). Python se interrumpe con este mensaje:

```text
Traceback (most recent call last):
  File "prueba.py", line 4, in <module>
    print("Intento", contador)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt
```

`KeyboardInterrupt` no indica una falla de Python: confirma que tú lo detuviste desde el teclado. El renglón señalado y las marcas debajo de él pueden variar, porque dependen de dónde iba el programa cuando presionaste las teclas y de tu versión de Python. Si un programa tuyo parece no terminar nunca, casi siempre a un `while` le falta el avance.

**`while` sirve cuando no sabes cuántas vueltas hacen falta.** ¿Cuántos pedidos se necesitan para alcanzar una meta de ventas?

```python
importes = [450.0, 1200.0, 380.0, 2500.0, 99.0]
meta = 2000
acumulado = 0
posicion = 0

while acumulado < meta and posicion < len(importes):
    acumulado += importes[posicion]
    posicion += 1

print(posicion, acumulado)
```

```text
3 2030.0
```

La segunda condición, `posicion < len(importes)`, evita pedir un índice que no existe si la lista se acaba antes de llegar a la meta.

**`break` termina el bucle en ese instante**, sin esperar a que la condición sea falsa. Aquí se surten pedidos hasta que uno ya no alcanza:

```python
existencias = 10
piezas_pedidas = [3, 4, 5, 2]
posicion = 0

while posicion < len(piezas_pedidas):
    if piezas_pedidas[posicion] > existencias:
        print("No alcanza para el pedido de la posición", posicion)
        break
    existencias -= piezas_pedidas[posicion]
    posicion += 1

print(existencias)
```

```text
No alcanza para el pedido de la posición 2
3
```

`break` también funciona dentro de un `for`.

### 11. ¿`for` o `while`?

| Usa `for` cuando... | Usa `while` cuando... |
| --- | --- |
| vas a recorrer todos los elementos de una lista | no sabes de antemano cuántas vueltas hacen falta |
| sabes cuántas veces repetir (`range`) | quieres detenerte en cuanto se cumpla una condición |

Si dudas, empieza con `for`: no puede volverse infinito, porque termina cuando la lista se acaba.

## Ejercicios

Abre `ejercicios.py`. Cada función tiene un docstring con lo que debe hacer y un ejemplo. Borra la línea `raise NotImplementedError(...)` y escribe tu código.

Tres recordatorios para todos los ejercicios:

- La función debe **devolver** el resultado con `return`. Usar `print()` no cuenta: las pruebas revisan lo que la función devuelve.
- Una función puede tener varios `return`, uno en cada camino de un `if`. En cuanto Python llega a un `return`, la función termina y entrega ese valor; lo que esté más abajo ya no corre.
- Una comparación ya vale `True` o `False`, así que puedes devolverla directamente: `return cantidad > 0`.

Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_03_condicionales -k ejercicio_1
```

### Ejercicio 1. `es_cantidad_valida(cantidad)`

Devuelve `True` si la cantidad es un número entero mayor que cero, y `False` en cualquier otro caso. En un archivo crudo, la columna de cantidad puede traer textos, decimales o nada.

Usa `isinstance(valor, int)`, del concepto 3, y recuerda el detalle de los booleanos del final del concepto 4: `True` y `False` no son cantidades válidas, aunque para Python sean enteros.

| Entrada | Resultado |
| --- | --- |
| `es_cantidad_valida(3)` | `True` |
| `es_cantidad_valida(0)` | `False` |
| `es_cantidad_valida("3")` | `False` |
| `es_cantidad_valida(2.5)` | `False` |
| `es_cantidad_valida(True)` | `False` |

Paso a paso:

1. Pregunta si la cantidad es un entero y no es un booleano.
2. Pregunta si la cantidad es mayor que cero.
3. Devuelve `True` solo si se cumplen todas las condiciones.

<details>
<summary>Pista 1</summary>

Son dos condiciones que deben cumplirse a la vez. Revisa la tabla del concepto 4 para elegir el operador que las une.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba muestra un `TypeError`, estás comparando un texto con cero. Recuerda que Python deja de evaluar en cuanto conoce la respuesta: el orden de las dos condiciones decide si la comparación llega a ocurrir.

</details>

### Ejercicio 2. `clasificar_importe(importe)`

Clasifica el importe de un pedido, en pesos, en uno de tres rangos.

| Importe | Resultado |
| --- | --- |
| Menor que 500 | `'bajo'` |
| De 500 a menos de 2000 | `'medio'` |
| De 2000 en adelante | `'alto'` |

| Entrada | Resultado |
| --- | --- |
| `clasificar_importe(120.5)` | `'bajo'` |
| `clasificar_importe(500)` | `'medio'` |
| `clasificar_importe(1999.99)` | `'medio'` |
| `clasificar_importe(2000)` | `'alto'` |

Paso a paso:

1. Escribe una cadena `if`, `elif`, `else` con un camino para cada rango.
2. Ordena las condiciones de un extremo al otro.
3. En cada camino, devuelve el texto que corresponde.

<details>
<summary>Pista 1</summary>

Como solo corre el primer bloque verdadero, al llegar al `elif` ya sabes que la condición anterior fue falsa. No hace falta repetirla.

</details>

<details>
<summary>Pista 2</summary>

Si fallan las pruebas de los límites, revisa cada comparación con el valor exacto: ¿en qué rango debe caer 500? ¿Tu condición usa `<` o `<=`?

</details>

### Ejercicio 3. `es_faltante(valor)`

Devuelve `True` si el valor representa un dato faltante. El valor llega como `None` o como texto, y es faltante si es `None` o si, ya limpio, es alguno de estos: `""`, `"n/d"`, `"na"`, `"null"`.

| Entrada | Resultado |
| --- | --- |
| `es_faltante(None)` | `True` |
| `es_faltante("   ")` | `True` |
| `es_faltante(" N/D ")` | `True` |
| `es_faltante("Puebla")` | `False` |
| `es_faltante("canal")` | `False` |

Paso a paso:

1. Si el valor es `None`, devuelve `True` de inmediato.
2. Limpia el texto: sin espacios en los extremos y en minúsculas.
3. Pregunta si el texto limpio es uno de los cuatro faltantes y devuelve la respuesta.

<details>
<summary>Pista 1</summary>

Si la prueba muestra `AttributeError: 'NoneType' object has no attribute 'strip'`, estás limpiando antes de preguntar por `None`. Revisa el concepto 8.

</details>

<details>
<summary>Pista 2</summary>

Para el paso 3, guarda los cuatro faltantes en una lista y usa el operador de pertenencia. Un texto de puros espacios, ya limpio, queda vacío.

</details>

<details>
<summary>Pista 3</summary>

Si `"canal"` te da `True`, estás buscando dentro de un texto y no dentro de una lista. Vuelve a leer el final del concepto 5.

</details>

### Ejercicio 4. `normalizar_estado(estado)`

El mismo estado llega escrito de muchas formas. Limpia el texto y devuelve una sola forma para cada uno.

| Texto limpio | Resultado |
| --- | --- |
| `entregado`, `entregada` | `'entregado'` |
| `enviado`, `en camino` | `'enviado'` |
| `cancelado`, `cancelada` | `'cancelado'` |
| Cualquier otro | `'desconocido'` |

| Entrada | Resultado |
| --- | --- |
| `normalizar_estado("  ENTREGADO ")` | `'entregado'` |
| `normalizar_estado("En camino")` | `'enviado'` |
| `normalizar_estado("Cancelada")` | `'cancelado'` |
| `normalizar_estado("devuelto")` | `'desconocido'` |

Paso a paso:

1. Limpia el texto y guárdalo en una variable.
2. Si el texto limpio es una de las formas de "entregado", devuelve `"entregado"`.
3. Haz lo mismo para "enviado" y para "cancelado".
4. Si no coincidió con ninguno, devuelve `"desconocido"`.

<details>
<summary>Pista 1</summary>

Es una cadena `if`, `elif`, `elif`, `else`. Cada condición pregunta si el texto limpio es una de dos formas posibles.

</details>

<details>
<summary>Pista 2</summary>

"Es una de dos formas" se puede escribir con `or` (repitiendo la comparación completa de cada lado) o con `in` y una lista pequeña. Elige la que te resulte más clara.

</details>

### Ejercicio 5. `filtrar_mayores(importes, minimo)`

Devuelve una lista nueva con los importes mayores o iguales al mínimo, en el mismo orden en que venían. La lista original no debe cambiar.

| Entrada | Resultado |
| --- | --- |
| `filtrar_mayores([450.0, 1200.0, 380.0, 2500.0], 1000)` | `[1200.0, 2500.0]` |
| `filtrar_mayores([499.99, 500, 500.01], 500)` | `[500, 500.01]` |
| `filtrar_mayores([], 500)` | `[]` |

Paso a paso:

1. Crea una lista vacía para el resultado.
2. Recorre los importes con un `for`.
3. Si el importe alcanza el mínimo, agrégalo a la lista nueva.
4. Al terminar el bucle, devuelve la lista nueva.

<details>
<summary>Pista 1</summary>

Es el patrón de filtrar del concepto 9, con la condición de este ejercicio.

</details>

<details>
<summary>Pista 2</summary>

Cuida la sangría del `return`. Si queda dentro del `for`, la función termina en la primera vuelta y devuelve una lista incompleta.

</details>

### Ejercicio 6. `contar_faltantes(valores)`

Devuelve cuántos elementos de la lista son datos faltantes. No repitas la regla: llama a tu función `es_faltante()` del ejercicio 3.

| Entrada | Resultado |
| --- | --- |
| `contar_faltantes(["Puebla", "", "N/D", "Mérida", None])` | `3` |
| `contar_faltantes(["Puebla", "Mérida"])` | `0` |
| `contar_faltantes([])` | `0` |

Paso a paso:

1. Crea un contador en cero.
2. Recorre los valores con un `for`.
3. Si el valor es faltante, suma uno al contador.
4. Al terminar el bucle, devuelve el contador.

<details>
<summary>Pista</summary>

`es_faltante(valor)` ya devuelve `True` o `False`, así que puede ir directamente como condición del `if`, sin compararla con nada.

</details>

### Ejercicio 7. `posicion_del_primer_faltante(valores)`

Devuelve el índice del primer dato faltante de la lista. Si no hay ninguno, devuelve `-1`. Resuélvelo con un bucle `while`: la idea es detenerte en cuanto encuentres el primero, sin revisar el resto.

| Entrada | Resultado |
| --- | --- |
| `posicion_del_primer_faltante(["Puebla", "Mérida", "NA", ""])` | `2` |
| `posicion_del_primer_faltante([None, "Puebla"])` | `0` |
| `posicion_del_primer_faltante(["Puebla", "Mérida"])` | `-1` |
| `posicion_del_primer_faltante([])` | `-1` |

Paso a paso:

1. Crea una variable de posición que empiece en cero.
2. Repite mientras la posición sea menor que el tamaño de la lista.
3. En cada vuelta, revisa el elemento que está en esa posición. Si es faltante, devuelve la posición.
4. Si no lo es, avanza la posición en uno.
5. Si el bucle termina sin encontrar nada, devuelve `-1`.

<details>
<summary>Pista 1</summary>

Compara tu bucle con el ejemplo de `break` del concepto 10: tiene las mismas tres partes (valor inicial, condición y avance). Aquí, un `return` dentro del bucle hace el trabajo del `break`, porque termina la función completa.

</details>

<details>
<summary>Pista 2</summary>

Si las pruebas se quedan corriendo sin terminar, detenlas con Ctrl+C y revisa el avance: debe ejecutarse en cada vuelta en la que no encontraste un faltante.

</details>

<details>
<summary>Pista 3</summary>

El `return -1` va fuera del `while`, con la misma sangría que la palabra `while`. Solo se llega ahí cuando ya se revisó toda la lista.

</details>

## Evalúate

Cuando termines los siete ejercicios, corre la lección completa:

```bash
pytest lecciones/leccion_03_condicionales
```

Debes ver `64 passed`. Si una prueba falla, lee la línea que empieza con `E`: te dice con qué valores se probó, qué se esperaba y qué devolvió tu función.

Revisa también el estilo de tu código:

```bash
ruff check lecciones/leccion_03_condicionales
```

Y guarda tu trabajo:

```bash
git add .
git commit -m "Completa la lección 3"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Qué diferencia hay entre `=` y `==`?
2. ¿Por qué `"Puebla " == "puebla"` da `False`, y qué harías antes de comparar?
3. En una cadena `if`, `elif`, `else`, ¿cuántos bloques corren como máximo?
4. ¿Qué tipo de error aparece al evaluar `"5" > 3`?
5. ¿Cómo preguntas si una variable vale `None`?
6. ¿Qué le falta a un `while` que nunca termina, y cómo lo detienes desde la terminal?
7. De la lección 2: ¿qué diferencia hay entre `lista.append(valor)` y `sorted(lista)` respecto a la lista original?
8. De la lección 1: ¿qué devuelve `"  N/D ".strip().lower()`?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. Casi siempre trae la respuesta.
2. Prueba tu función a mano: abre el intérprete con `python` y llama a la función con el valor que falló.
3. Si el resultado es incorrecto pero no hay error, sigue tu código renglón por renglón con ese valor y anota por cuál camino del `if` entra.
4. Revisa los ejemplos resueltos de `ejemplos.py`.
5. Abre las pistas del ejercicio, una a la vez.
6. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 5, "if Statements": comparaciones, `and` y `or`, `in` y `not in`, cadenas `if-elif-else`, uso de `if` con listas y estilo de las condiciones.
- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 7, "User Input and while Loops": bucle `while`, `break` y cómo evitar y detener un bucle infinito.
- Bill Lubanovic, *Introducing Python*, capítulo 4, "Py Crust: Code Structures": comparaciones, `if`, `elif`, `else` y bucles `while` con `break`.
- Felienne Hermans, *The Programmer's Brain*, capítulo 7, "Misconceptions: Bugs in thinking": por qué lo que ya sabes de otros contextos puede llevarte a errores al programar, y cómo corregir esas ideas.
