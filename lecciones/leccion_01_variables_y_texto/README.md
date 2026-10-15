# Lección 1: Variables, texto y números

Los datos reales llegan sucios: precios escritos como texto, ciudades con espacios de más, nombres en mayúsculas y minúsculas mezcladas. En esta lección aprendes las piezas más pequeñas de Python y las usas para limpiar un dato a la vez.

**Tiempo estimado:** 90 minutos.
**Antes de empezar:** completa la [lección 0](../leccion_00_preparacion/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Guardar valores en variables con nombres claros.
- Distinguir texto (`str`), enteros (`int`) y números con decimales (`float`).
- Limpiar y dar formato a un texto con sus métodos y con f-strings.
- Convertir un texto en número y hacer cuentas con él.
- Leer un mensaje de error sin asustarte.

## Por qué importa en datos

Casi todo archivo que recibas trae los números como texto. Para Python, `"$1,250.50"` no es una cantidad: es una fila de caracteres, y no se puede sumar. Convertir ese texto en un número confiable es el primer trabajo de cualquier flujo de datos, y es lo que harás aquí.

Las funciones que escribas en esta lección reaparecen en el proyecto final, donde limpiarás un archivo completo de pedidos.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. No los copies y pegues: teclearlos es parte del aprendizaje.
2. Corre `python lecciones/leccion_01_variables_y_texto/ejemplos.py` y cambia valores para ver qué pasa.
3. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno.
4. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

## Conceptos

### 1. Variables

Una variable es un nombre que apunta a un valor. Se crea con el signo `=`.

```python
producto = "Café de olla"
cantidad = 3
```

Se lee de derecha a izquierda: "toma el valor `3` y llámalo `cantidad`". Desde ese momento puedes usar el nombre en lugar del valor.

```python
print(cantidad)
```

```text
3
```

Reglas para nombrar variables:

- Solo letras, números y guion bajo. No pueden empezar con número.
- Sin espacios: `precio_unitario`, no `precio unitario`.
- En minúsculas, con palabras separadas por guion bajo.
- Que digan qué guardan. `precio_unitario` se entiende; `p` o `x1` no.

> En este curso escribimos los nombres en español y sin acentos ni ñ: `tamano`, no `tamaño`. Python sí los acepta, pero evitarlos ahorra problemas entre teclados y sistemas operativos.

### 2. Provoca tu primer error

Equivocarte es parte del trabajo. Lo que distingue a quien avanza es que lee el error. Crea un archivo de prueba, o usa el intérprete, y escribe esto tal cual, con la falta de ortografía incluida:

```python
mensaje = "Hola, datos"
print(mensage)
```

Python responde:

```text
Traceback (most recent call last):
  File "prueba.py", line 2, in <module>
    print(mensage)
          ^^^^^^^
NameError: name 'mensage' is not defined. Did you mean: 'mensaje'?
```

Léelo de abajo hacia arriba:

1. **Última línea:** el tipo de error y su explicación. `NameError` significa que usaste un nombre que Python no conoce.
2. **Línea con `File`:** el archivo y el número de renglón donde ocurrió.
3. **El renglón señalado:** el código exacto que falló.

Los mensajes de Python están en inglés. No necesitas traducirlos completos: con el tipo de error y el renglón casi siempre basta. En [docs/como-leer-un-error.md](../../docs/como-leer-un-error.md) hay una tabla con los más comunes.

### 3. Texto

El texto se escribe entre comillas, simples o dobles. Su tipo se llama `str`.

```python
ciudad = "  ciudad de méxico  "
```

Los textos tienen **métodos**: acciones que se piden con un punto después del valor.

| Método | Qué devuelve | Ejemplo | Resultado |
| --- | --- | --- | --- |
| `.strip()` | El texto sin espacios en los extremos | `"  hola ".strip()` | `'hola'` |
| `.lower()` | Todo en minúsculas | `"HOLA".lower()` | `'hola'` |
| `.upper()` | Todo en mayúsculas | `"hola".upper()` | `'HOLA'` |
| `.title()` | Mayúscula al inicio de cada palabra | `"ana lópez".title()` | `'Ana López'` |
| `.replace(a, b)` | El texto con `a` cambiado por `b` | `"1,250".replace(",", "")` | `'1250'` |

> **Sobre `.title()` en español:** pone mayúscula a todas las palabras, incluidas las preposiciones. `"ciudad de méxico".title()` da `'Ciudad De México'`, con esa `De` que en español no se escribe así. Para nombres propios con reglas, como las ciudades, en el proyecto final lo combinarás con un diccionario de nombres oficiales. En esta lección basta con `.title()` tal como está.

Dos ideas que evitan muchos errores:

**Los métodos no cambian el texto original; devuelven uno nuevo.** Si no guardas el resultado, se pierde.

```python
ciudad = "  puebla  "
ciudad.strip()  # el resultado se pierde
print(repr(ciudad))  # '  puebla  '

ciudad = ciudad.strip()  # ahora sí se guarda
print(repr(ciudad))  # 'puebla'
```

`repr()` muestra el texto con sus comillas, así puedes ver los espacios que `print()` esconde.

**Los métodos se pueden encadenar.** Cada uno trabaja sobre el resultado del anterior, de izquierda a derecha.

```python
ciudad = "  ciudad de méxico  ".strip().title()
print(ciudad)
```

```text
Ciudad De México
```

### 4. f-strings: texto con valores dentro

Para armar un texto con variables, pon una `f` antes de las comillas y los nombres entre llaves.

```python
producto = "Café de olla"
cantidad = 3
mensaje = f"{cantidad} piezas de {producto}"
print(mensaje)
```

```text
3 piezas de Café de olla
```

### 5. Números

Hay dos tipos básicos:

- `int`: enteros, como `3` o `-10`.
- `float`: con punto decimal, como `45.5` o `3.0`.

```python
cantidad = 3
precio_unitario = 45.5
total = cantidad * precio_unitario
print(total)
```

```text
136.5
```

| Operación | Símbolo | Ejemplo | Resultado |
| --- | --- | --- | --- |
| Suma | `+` | `10 + 3` | `13` |
| Resta | `-` | `10 - 3` | `7` |
| Multiplicación | `*` | `10 * 3` | `30` |
| División | `/` | `10 / 4` | `2.5` |
| Potencia | `**` | `10 ** 2` | `100` |

La división con `/` siempre devuelve un `float`, aunque el resultado sea exacto: `10 / 2` da `5.0`.

**Redondeo.** Las computadoras guardan los decimales de forma aproximada, y a veces eso se nota:

```python
print(3 * 0.1)
print(round(3 * 0.1, 2))
```

```text
0.30000000000000004
0.3
```

Por eso, al trabajar con dinero redondeamos con `round(valor, 2)`.

### 6. De texto a número

`"45"` y `45` no son lo mismo. El primero es texto; el segundo, un número.

```python
print("45" + "5")
print(45 + 5)
```

```text
455
50
```

Para convertir se usan `int()` y `float()`:

```python
precio = float("45.50")
print(precio + 10)
```

```text
55.5
```

Ahora provoca el segundo error de la lección:

```python
float("$1,250.50")
```

```text
ValueError: could not convert string to float: '$1,250.50'
```

`ValueError` significa que el tipo es correcto (sí es un texto) pero su contenido no sirve para lo que pediste. `float()` solo entiende dígitos y un punto. La solución es limpiar antes de convertir:

```python
precio_crudo = "$1,250.50"
precio_sin_simbolos = precio_crudo.replace("$", "").replace(",", "")
precio = float(precio_sin_simbolos)
print(precio)
```

```text
1250.5
```

### 7. Formato de números dentro de un f-string

Dentro de las llaves, después de dos puntos, puedes indicar cómo mostrar un número.

| Formato | Significado | Ejemplo | Resultado |
| --- | --- | --- | --- |
| `:.2f` | Dos decimales | `f"{45:.2f}"` | `'45.00'` |
| `:,` | Comas de miles | `f"{1250000:,}"` | `'1,250,000'` |
| `:,.2f` | Ambos | `f"{1250.5:,.2f}"` | `'1,250.50'` |

El resultado es texto, pensado para mostrarse. Para hacer cuentas, usa siempre el número.

### 8. Comentarios

Todo lo que sigue a un `#` es un comentario: Python lo ignora y sirve para quien lee el código.

```python
# El archivo trae los precios con símbolo y comas; hay que quitarlos antes de convertir.
precio = float(precio_crudo.replace("$", "").replace(",", ""))
```

Un buen comentario explica **por qué** se hace algo. El **qué** ya lo dice el código.

### 9. Cómo entregas tu respuesta en los ejercicios: `def` y `return`

Cada ejercicio de este curso es una función que tú completas. Para hacerlo solo necesitas reconocer cuatro piezas:

```python
def describir_pedido(producto, cantidad):
    return f"{cantidad} piezas de {producto}"
```

- `def` define una función y le da un nombre, aquí `describir_pedido`.
- Lo que va entre paréntesis son los datos que recibe. Dentro de la función los usas como variables normales.
- Lo que va indentado con cuatro espacios es el **cuerpo**: las líneas que se ejecutan cuando alguien usa la función.
- `return` **entrega el resultado**. Lo que pongas después de `return` es lo que recibe quien llamó a la función.

Para usar la función la llamas por su nombre, con los datos entre paréntesis, y guardas lo que devuelve:

```python
descripcion = describir_pedido("Café de olla", 3)
print(descripcion)
```

```text
3 piezas de Café de olla
```

Un error muy común es usar `print` en lugar de `return`. `print` solo muestra el valor en pantalla y no entrega nada: la función devuelve `None`, y las pruebas lo reciben así aunque en pantalla se vea el texto correcto.

```python
def describir_pedido_mal(producto, cantidad):
    print(f"{cantidad} piezas de {producto}")


resultado = describir_pedido_mal("Café de olla", 3)
print(resultado)
```

```text
3 piezas de Café de olla
None
```

Las funciones de `ejercicios.py` tienen exactamente esta forma. Tu trabajo es escribir el cuerpo y terminar con un `return`. En la lección 5 verás las funciones a fondo.

## Ejercicios

Abre `ejercicios.py`. Cada función tiene un docstring con lo que debe hacer y un ejemplo. Borra la línea `raise NotImplementedError(...)` y escribe tu código.

Dos recordatorios para todos los ejercicios:

- La función debe **devolver** el resultado con `return`. Usar `print()` no cuenta: las pruebas revisan lo que la función devuelve.
- Usa los parámetros que recibe la función. No escribas valores fijos.

Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_01_variables_y_texto -k ejercicio_1
```

### Ejercicio 1. `nombre_completo(nombre, apellido)`

Une el nombre y el apellido con un espacio, cada palabra con mayúscula inicial.

| Entrada | Resultado |
| --- | --- |
| `nombre_completo("ana", "lópez")` | `'Ana López'` |
| `nombre_completo("JOSÉ", "PÉREZ")` | `'José Pérez'` |

Paso a paso:

1. Arma un texto que contenga el nombre, un espacio y el apellido.
2. Aplica a ese texto el método que pone mayúscula al inicio de cada palabra.
3. Devuelve el resultado.

<details>
<summary>Pista 1</summary>

Un f-string te permite unir las dos variables con un espacio entre ellas.

</details>

<details>
<summary>Pista 2</summary>

Revisa la tabla de métodos de texto. Uno de ellos hace justo lo del paso 2, y puedes aplicarlo directamente al f-string.

</details>

### Ejercicio 2. `limpiar_texto(texto)`

Quita los espacios de los extremos y pasa todo a minúsculas. Es la limpieza más común al comparar textos: sin ella, `"Monterrey "` y `"monterrey"` cuentan como dos ciudades distintas.

| Entrada | Resultado |
| --- | --- |
| `limpiar_texto("  Monterrey ")` | `'monterrey'` |
| `limpiar_texto("  San Luis Potosí  ")` | `'san luis potosí'` |

Paso a paso:

1. Quita los espacios de los extremos.
2. Pasa el resultado a minúsculas.
3. Devuelve el texto limpio.

<details>
<summary>Pista</summary>

Son dos métodos encadenados. Los espacios de en medio se quedan como están: ningún método de esta lección los toca.

</details>

### Ejercicio 3. `precio_a_numero(texto)`

Convierte un precio escrito como texto en un `float`. El texto puede traer espacios, el símbolo `$` y comas de miles.

| Entrada | Resultado |
| --- | --- |
| `precio_a_numero("45.5")` | `45.5` |
| `precio_a_numero(" $1,250.50 ")` | `1250.5` |
| `precio_a_numero("$1,000,000")` | `1000000.0` |

Paso a paso:

1. Quita los espacios de los extremos.
2. Elimina el símbolo `$`.
3. Elimina las comas.
4. Convierte lo que queda en `float` y devuélvelo.

<details>
<summary>Pista 1</summary>

"Eliminar" un carácter es reemplazarlo por un texto vacío: `""`.

</details>

<details>
<summary>Pista 2</summary>

Guarda cada paso en una variable con buen nombre, por ejemplo `sin_simbolos`. El código queda más largo, pero se lee y se corrige mejor.

</details>

### Ejercicio 4. `calcular_total(cantidad, precio_unitario)`

Multiplica la cantidad por el precio unitario y redondea a dos decimales.

| Entrada | Resultado |
| --- | --- |
| `calcular_total(3, 19.99)` | `59.97` |
| `calcular_total(3, 0.1)` | `0.3` |

Paso a paso:

1. Multiplica los dos valores.
2. Redondea el resultado a dos decimales.
3. Devuélvelo.

<details>
<summary>Pista</summary>

Si la prueba dice que obtuviste `0.30000000000000004`, te falta el redondeo. Vuelve a leer la sección de números.

</details>

### Ejercicio 5. `aplicar_descuento(total, porcentaje)`

Resta al total el porcentaje indicado y redondea a dos decimales. El porcentaje llega como número entre 0 y 100.

| Entrada | Resultado |
| --- | --- |
| `aplicar_descuento(200, 15)` | `170.0` |
| `aplicar_descuento(100, 0)` | `100.0` |

Paso a paso:

1. Calcula cuánto dinero representa el descuento: total por porcentaje, entre 100.
2. Resta ese descuento al total.
3. Redondea a dos decimales y devuelve.

<details>
<summary>Pista</summary>

Guarda el descuento en su propia variable antes de restar. Con `total = 200` y `porcentaje = 15`, el descuento vale `30.0`.

</details>

### Ejercicio 6. `formatear_importe(importe)`

Devuelve el importe como texto listo para mostrarse: símbolo de pesos, comas de miles, dos decimales y la moneda.

| Entrada | Resultado |
| --- | --- |
| `formatear_importe(1250.5)` | `'$1,250.50 MXN'` |
| `formatear_importe(45)` | `'$45.00 MXN'` |

Paso a paso:

1. Escribe un f-string que empiece con el símbolo `$`.
2. Dentro de las llaves pon el importe con el formato de miles y dos decimales.
3. Termina con un espacio y `MXN`.

<details>
<summary>Pista</summary>

El formato que necesitas está en la última fila de la tabla de formatos. El símbolo `$` va fuera de las llaves.

</details>

## Evalúate

Cuando termines los seis ejercicios, corre la lección completa:

```bash
pytest lecciones/leccion_01_variables_y_texto
```

Debes ver `29 passed`. Si una prueba falla, lee la línea que empieza con `E`: te dice con qué valores se probó, qué se esperaba y qué devolvió tu función.

Revisa también el estilo de tu código:

```bash
ruff check lecciones/leccion_01_variables_y_texto
```

Y guarda tu trabajo:

```bash
git add .
git commit -m "Completa la lección 1"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Qué diferencia hay entre `"45"` y `45`?
2. ¿Qué devuelve `"  Hola ".strip().lower()`?
3. ¿Por qué `ciudad.strip()` en una línea sola no cambia la variable `ciudad`?
4. ¿Qué tipo de error aparece si usas un nombre de variable mal escrito?
5. ¿Qué tipo de error aparece si intentas `float("$10")`?
6. ¿Para qué sirve `round(valor, 2)`?
7. ¿Qué diferencia hay entre `print()` y `return`?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. Casi siempre trae la respuesta.
2. Prueba tu función a mano: abre el intérprete con `python` y llama a la función con el valor que falló.
3. Revisa los ejemplos resueltos de `ejemplos.py`.
4. Abre las pistas del ejercicio, una a la vez.
5. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 2, "Variables and Simple Data Types": variables y reglas de nombres, métodos de texto, f-strings, números, comentarios, y la lectura guiada de un `NameError`.
- Reuven Lerner, *Python Workout*, 2.ª ed., capítulos 2 ("Numeric types") y 3 ("Strings"): formato de ejercicio con enunciado, razonamiento y variantes.
- Felienne Hermans, *The Programmer's Brain*, capítulo 3, "How to learn programming syntax quickly": por qué intentar recordar antes de buscar y por qué conviene repasar espaciado.
