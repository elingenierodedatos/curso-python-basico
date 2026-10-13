# Lección 8: Guardar y consultar datos con SQLite

Ya sabes leer pedidos de un archivo, limpiarlos y guardarlos en otro archivo. El siguiente paso es guardarlos en un lugar al que se le puedan hacer preguntas: una base de datos. En esta lección aprendes el SQL mínimo y lo usas desde Python con SQLite, que ya viene instalado.

**Tiempo estimado:** 120 minutos.
**Antes de empezar:** completa la [lección 7](../leccion_07_pruebas/README.md) y activa tu entorno virtual.

## Qué vas a lograr

- Explicar cuándo conviene una base de datos en lugar de un archivo.
- Crear una tabla con tipos y clave primaria.
- Insertar filas desde Python pasando los valores como parámetros.
- Consultar con filtros, orden, conteos y sumas por grupo.
- Convertir las filas que devuelve la base en diccionarios.
- Leer los dos errores más comunes de SQLite y saber qué los causa.

## Por qué importa en datos

Un archivo CSV sirve para mover datos de un lugar a otro, pero para responder "¿cuánto se vendió en Guadalajara?" hay que leerlo completo y recorrerlo con un bucle. Una base de datos responde esa pregunta con una sola instrucción, y además cuida los datos por ti:

- **Consulta sin cargar todo.** Pides solo las filas y columnas que necesitas.
- **Guarda tipos.** Una cantidad se guarda como número y vuelve como número, no como texto.
- **Es una sola fuente.** Todos los programas leen la misma tabla, en lugar de copias del mismo archivo con versiones distintas.

Casi todo flujo de datos termina cargando sus resultados en una base de datos, y el lenguaje para hablar con ella es SQL. En el proyecto final guardarás así los pedidos ya limpios.

## Cómo trabajar esta lección

1. Lee cada concepto y escribe los ejemplos tú mismo. No los copies y pegues: teclearlos es parte del aprendizaje.
2. Corre `python lecciones/leccion_08_sqlite/ejemplos.py` y cambia valores para ver qué pasa.
3. Resuelve los ejercicios en orden, uno a la vez, corriendo las pruebas después de cada uno.
4. Hazlo sin asistentes de IA. La explicación está en [docs/por-que-sin-ia.md](../../docs/por-que-sin-ia.md).

## Conceptos

### 1. SQLite: una base de datos que ya tienes

SQLite es una base de datos completa que cabe en **un solo archivo**. No hay servidor que instalar ni contraseña que configurar, y funciona igual en Windows, macOS y Linux. El módulo que la maneja, `sqlite3`, viene con Python:

```python
import sqlite3
```

Una base de datos guarda **tablas**. Una tabla se parece a una hoja de cálculo: tiene **columnas** con nombre y tipo, y **filas**, una por cada pedido.

Las instrucciones se escriben en **SQL**, un lenguaje aparte que Python envía a la base como texto. Por costumbre, las palabras de SQL van en mayúsculas (`SELECT`, `FROM`) y los nombres de tablas y columnas en minúsculas. A SQLite le da igual, pero así se lee mejor.

### 2. Conectar y cerrar

Para trabajar con una base se abre una **conexión**. Para practicar, el nombre especial `":memory:"` crea una base temporal que vive en la memoria y desaparece al cerrarla:

```python
conexion = sqlite3.connect(":memory:")
```

Para una base de verdad se pasa la ruta del archivo. Si el archivo no existe, SQLite lo crea:

```python
from pathlib import Path

ruta = Path("salida") / "tienda.db"
conexion = sqlite3.connect(ruta)
```

SQLite crea el archivo, pero no la carpeta. Si `salida` no existe, Python responde:

```text
sqlite3.OperationalError: unable to open database file
```

Por eso primero se crea la carpeta. `ruta.parent` es la carpeta que contiene al archivo, y `mkdir` la crea:

```python
ruta.parent.mkdir(parents=True, exist_ok=True)
```

`parents=True` crea también las carpetas intermedias que falten, y `exist_ok=True` evita un error si la carpeta ya estaba ahí.

Cuando terminas, cierras:

```python
conexion.close()
```

Una conexión abierta mantiene ocupado el archivo. Piensa en ella como en una llave de agua: quien la abre, la cierra. En Windows, por ejemplo, no se puede borrar ni mover el archivo de una base mientras alguna conexión siga abierta.

### 3. Crear una tabla

`CREATE TABLE` define el nombre de la tabla y sus columnas. Las instrucciones se envían con `conexion.execute()`. Como esta ocupa varios renglones, va entre comillas triples:

```python
conexion.execute(
    """
    CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido INTEGER PRIMARY KEY,
        fecha TEXT,
        cliente TEXT,
        ciudad TEXT,
        producto TEXT,
        cantidad INTEGER,
        precio_unitario REAL,
        estado TEXT
    )
    """
)
```

Cada columna lleva su nombre y su tipo:

| Tipo en SQLite | Qué guarda | Equivale en Python a |
| --- | --- | --- |
| `INTEGER` | Números enteros | `int` |
| `REAL` | Números con decimales | `float` |
| `TEXT` | Texto | `str` |

Dos detalles de esa instrucción:

- **`IF NOT EXISTS`** crea la tabla solo si todavía no existe. Sin esas palabras, correr el programa por segunda vez falla con `table pedidos already exists`.
- **`PRIMARY KEY`** marca la columna que identifica a cada fila. La base no acepta dos filas con la misma clave primaria: no puede haber dos pedidos con el mismo `id_pedido`.

SQLite no tiene un tipo para fechas. Se guardan como texto con el formato `AAAA-MM-DD`, que además se ordena bien alfabéticamente.

> Guardamos el precio como `REAL` y redondeamos al sumar, que para este curso es suficiente. En sistemas reales el dinero suele guardarse en centavos, como número entero, para evitar los decimales aproximados que viste en la lección 1.

### 4. Insertar filas con parámetros

`INSERT INTO` agrega una fila. Los valores no se escriben dentro del SQL: en su lugar va un signo de interrogación por cada uno, y los valores viajan aparte, en una tupla, como segundo argumento de `execute()`:

```python
sql = "INSERT INTO pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
pedido = (
    1,
    "2024-03-01",
    "Ana López",
    "Ciudad de México",
    "Café de olla",
    3,
    89.9,
    "entregado",
)
conexion.execute(sql, pedido)
```

Esos signos se llaman **parámetros**. SQLite pone cada valor de la tupla en el lugar del `?` que le corresponde, en orden: el primero va a la primera columna de la tabla, el segundo a la segunda, y así hasta la octava.

Para insertar muchas filas con la misma instrucción existe `executemany()`, que recibe una lista de tuplas:

```python
mas_pedidos = [
    (
        2,
        "2024-03-01",
        "Luis Hernández",
        "Guadalajara",
        "Prensa francesa",
        1,
        499.0,
        "enviado",
    ),
    (
        3,
        "2024-03-02",
        "María Fernández",
        "Ciudad de México",
        "Molinillo manual",
        1,
        1250.5,
        "entregado",
    ),
    (
        4,
        "2024-03-03",
        "Sofía Ramírez",
        "Guadalajara",
        "Filtro de tela",
        4,
        65.0,
        "cancelado",
    ),
]
conexion.executemany(sql, mas_pedidos)
```

Con estos cuatro pedidos trabajan todos los ejemplos que siguen.

### 5. Provoca el error: SQL armado con un f-string

Si ya sabes meter variables en un texto con un f-string, es natural pensar en armar así el SQL. No lo hagas nunca. Para ver por qué, pruébalo en una base de práctica aparte, con una taza cuyo nombre trae comillas y un apóstrofo:

```python
practica = sqlite3.connect(":memory:")
practica.execute("CREATE TABLE productos (nombre TEXT)")

producto = 'Taza "La Abuela\'s"'
sql = f"INSERT INTO productos VALUES ('{producto}')"
practica.execute(sql)
```

Python responde:

```text
sqlite3.OperationalError: near "s": syntax error
```

`OperationalError` con `syntax error` significa que SQLite recibió un SQL que no pudo entender. Para saber por qué, imprime el texto que le enviaste:

```python
print(sql)
```

```text
INSERT INTO productos VALUES ('Taza "La Abuela's"')
```

En SQL el texto va entre apóstrofos. El apóstrofo de `Abuela's` cerró el texto antes de tiempo, y lo que quedó suelto, `s"')`, ya no tiene sentido. De ahí el `near "s"`: el mensaje señala el punto donde SQLite se perdió.

Ahora hazlo con parámetros:

```python
sql = "INSERT INTO productos VALUES (?)"
practica.execute(sql, (producto,))
print(practica.execute("SELECT nombre FROM productos").fetchall())
practica.close()
```

```text
[('Taza "La Abuela\'s"',)]
```

La coma de `(producto,)` es necesaria: los parámetros van siempre en una tupla, y una tupla de un solo elemento se escribe así. Funciona sin tocar el texto, porque el valor ya no forma parte de la instrucción: viaja aparte y SQLite lo guarda tal cual.

El problema va más allá de un apóstrofo. Si el SQL se arma pegando textos que escribió otra persona, esa persona puede escribir SQL en lugar de un nombre y tu programa lo ejecutará: puede leer filas que no le tocan o borrar la tabla. Ese ataque se llama **inyección de SQL**, y la defensa es justo esta: los valores van siempre como parámetros.

> Regla de la lección: el texto del SQL lo escribes tú, completo y fijo. Todo valor que venga de una variable entra con `?`.

### 6. Confirmar los cambios con `commit()`

Lo que insertas queda pendiente hasta que lo confirmas. Hazlo ahora con los cuatro pedidos:

```python
conexion.commit()
```

Si cierras la conexión sin `commit()`, los cambios pendientes se descartan sin ningún aviso. Compruébalo en el intérprete con una base en archivo:

```python
import sqlite3

conexion = sqlite3.connect("practica.db")
conexion.execute("CREATE TABLE notas (texto TEXT)")
conexion.execute("INSERT INTO notas VALUES (?)", ("sin guardar",))
conexion.close()

conexion = sqlite3.connect("practica.db")
print(conexion.execute("SELECT COUNT(*) FROM notas").fetchone())
conexion.close()
```

```text
(0,)
```

La tabla existe, pero la fila se perdió. Repite el experimento con otro nombre de archivo y un `conexion.commit()` antes del primer `close()`: ahora verás `(1,)`. Al terminar, borra los archivos de práctica para que no se suban a tu repositorio.

Lo que acabas de usar para leer, `SELECT` y `fetchone()`, es el tema que sigue.

### 7. Consultar: `SELECT`, `WHERE` y `ORDER BY`

`SELECT` pide columnas y `FROM` dice de qué tabla. `execute()` envía la consulta y `fetchall()` trae todas las filas que resultaron:

```python
filas = conexion.execute("SELECT id_pedido, cliente, ciudad FROM pedidos").fetchall()
print(filas)
```

```text
[(1, 'Ana López', 'Ciudad de México'), (2, 'Luis Hernández', 'Guadalajara'), (3, 'María Fernández', 'Ciudad de México'), (4, 'Sofía Ramírez', 'Guadalajara')]
```

El resultado es una **lista de tuplas**: una tupla por fila, con los valores en el orden en que pediste las columnas. Si ninguna fila cumple, la lista llega vacía.

**`WHERE` filtra filas.** La condición se parece a la de un `if`, con una diferencia: en SQL la igualdad se escribe con un solo `=`. El valor con el que comparas es un parámetro:

```python
sql = "SELECT id_pedido, producto, estado FROM pedidos WHERE ciudad = ?"
print(conexion.execute(sql, ("Guadalajara",)).fetchall())
```

```text
[(2, 'Prensa francesa', 'enviado'), (4, 'Filtro de tela', 'cancelado')]
```

Fíjate otra vez en la coma de `("Guadalajara",)`. Sin ella, `("Guadalajara")` es solo un texto entre paréntesis, y SQLite intenta usar cada letra como un parámetro distinto:

```text
sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 11 supplied.
```

Si ves ese mensaje, cuenta: el número de `?` y el número de valores de la tupla deben coincidir.

Otros operadores de `WHERE` son `!=` (distinto), `>`, `<`, `>=` y `<=`. Cuando el valor es fijo y lo escribes tú, puede ir dentro del SQL, entre apóstrofos si es texto.

**`ORDER BY` ordena el resultado.** De menor a mayor si no dices otra cosa; con `DESC`, de mayor a menor:

```python
sql = """
    SELECT producto, precio_unitario
    FROM pedidos
    WHERE estado != 'cancelado'
    ORDER BY precio_unitario DESC
"""
print(conexion.execute(sql).fetchall())
```

```text
[('Molinillo manual', 1250.5), ('Prensa francesa', 499.0), ('Café de olla', 89.9)]
```

El orden de las partes es fijo: `SELECT`, `FROM`, `WHERE`, `ORDER BY`. Sin `ORDER BY`, la base no promete ningún orden.

**`fetchone()` trae una sola fila.** Úsalo cuando esperas un único resultado. Devuelve una tupla, o `None` si no hubo filas:

```python
sql = "SELECT cliente, ciudad FROM pedidos WHERE id_pedido = ?"
print(conexion.execute(sql, (3,)).fetchone())
print(conexion.execute(sql, (99,)).fetchone())
```

```text
('María Fernández', 'Ciudad de México')
None
```

### 8. De tuplas a diccionarios

Una tupla obliga a recordar qué hay en cada posición. En el resto del curso un pedido es un diccionario, así que conviene convertir cada fila con un bucle:

```python
sql = "SELECT id_pedido, cliente, producto FROM pedidos WHERE ciudad = ?"
filas = conexion.execute(sql, ("Guadalajara",)).fetchall()

pedidos = []
for fila in filas:
    pedido = {"id_pedido": fila[0], "cliente": fila[1], "producto": fila[2]}
    pedidos.append(pedido)

print(pedidos)
```

```text
[{'id_pedido': 2, 'cliente': 'Luis Hernández', 'producto': 'Prensa francesa'}, {'id_pedido': 4, 'cliente': 'Sofía Ramírez', 'producto': 'Filtro de tela'}]
```

Las posiciones de la tupla siguen el orden de las columnas del `SELECT`. Por eso conviene escribir las columnas una por una: así el orden lo decides tú y está a la vista.

### 9. Contar, sumar y agrupar

`COUNT(*)` cuenta filas y `SUM()` suma una columna. El resultado es una sola fila, así que se lee con `fetchone()`:

```python
print(conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone())
print(conexion.execute("SELECT SUM(cantidad) FROM pedidos").fetchone())
```

```text
(4,)
(9,)
```

Sigue siendo una tupla, aunque tenga un solo valor. El número está en la posición `0`:

```python
fila = conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone()
print(fila[0])
```

```text
4
```

Dentro de `SELECT` también puedes hacer cuentas entre columnas, y `ROUND(valor, 2)` redondea igual que `round()` en Python:

```python
sql = "SELECT cantidad * precio_unitario FROM pedidos WHERE id_pedido = ?"
print(conexion.execute(sql, (1,)).fetchone())

sql = "SELECT ROUND(cantidad * precio_unitario, 2) FROM pedidos WHERE id_pedido = ?"
print(conexion.execute(sql, (1,)).fetchone())
```

```text
(269.70000000000005,)
(269.7,)
```

**`GROUP BY` hace la cuenta una vez por grupo.** En la lección 4 sumaste por grupo a mano, con un diccionario que acumula. Con los pedidos de esta lección se vería así:

```python
piezas_por_ciudad = {}
for fila in conexion.execute("SELECT ciudad, cantidad FROM pedidos").fetchall():
    ciudad = fila[0]
    cantidad = fila[1]
    piezas_por_ciudad[ciudad] = piezas_por_ciudad.get(ciudad, 0) + cantidad

print(piezas_por_ciudad)
```

```text
{'Ciudad de México': 4, 'Guadalajara': 5}
```

`GROUP BY` le pide a la base que haga ese mismo trabajo:

```python
sql = "SELECT ciudad, SUM(cantidad) FROM pedidos GROUP BY ciudad"
print(conexion.execute(sql).fetchall())
```

```text
[('Ciudad de México', 4), ('Guadalajara', 5)]
```

La idea es la misma: junta las filas que tienen la misma ciudad y calcula la suma de cada grupo. Lo que en el diccionario era la clave, aquí es la columna de `GROUP BY`; lo que era el valor acumulado, aquí es `SUM()`.

Para ordenar por el resultado de la suma, ponle un nombre con `AS` y úsalo en `ORDER BY`:

```python
sql = """
    SELECT ciudad, SUM(cantidad) AS piezas
    FROM pedidos
    GROUP BY ciudad
    ORDER BY piezas DESC
"""
print(conexion.execute(sql).fetchall())
```

```text
[('Guadalajara', 5), ('Ciudad de México', 4)]
```

Si además hay un `WHERE`, va antes de `GROUP BY`: primero se filtran las filas y después se agrupan las que quedaron. El orden completo es `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`.

### 10. Provoca el error: una clave repetida

El pedido 1 ya está en la tabla. Intenta insertar otro con el mismo `id_pedido`:

```python
sql = "INSERT INTO pedidos (id_pedido, cliente) VALUES (?, ?)"
conexion.execute(sql, (1, "Carla Mendoza"))
```

```text
sqlite3.IntegrityError: UNIQUE constraint failed: pedidos.id_pedido
```

Léelo por partes:

1. **`IntegrityError`:** el SQL está bien escrito, pero el dato rompe una regla de la tabla.
2. **`UNIQUE constraint failed`:** la regla rota es la de valores únicos.
3. **`pedidos.id_pedido`:** la tabla y la columna donde ocurrió.

Este error es una buena noticia: la base rechazó un pedido duplicado que en un archivo CSV habría pasado sin que nadie lo notara. La fila original queda intacta.

Compara los dos errores de la lección:

| Error | Qué significa | Dónde buscar |
| --- | --- | --- |
| `sqlite3.OperationalError` | SQLite no pudo ejecutar la instrucción: SQL mal escrito, una tabla que no existe, un archivo que no se pudo abrir | En el texto del SQL o en la ruta |
| `sqlite3.IntegrityError` | El dato rompe una regla de la tabla, como la clave primaria | En los datos que intentas guardar |

## Ejercicios

Abre `ejercicios.py`. Cada función tiene un docstring con lo que debe hacer y un ejemplo. Borra la línea `raise NotImplementedError(...)` y escribe tu código.

Tres recordatorios para todos los ejercicios:

- Salvo la primera, todas las funciones **reciben la conexión ya abierta** como primer parámetro. No abras otra dentro de la función y no la cierres: eso le toca a quien la abrió.
- Todo valor que llegue por un parámetro de la función entra al SQL con `?`. Ningún f-string.
- Las columnas de la tabla van siempre en este orden: `id_pedido`, `fecha`, `cliente`, `ciudad`, `producto`, `cantidad`, `precio_unitario`, `estado`.

Las pruebas le pasan a tus funciones una base en memoria recién creada y la cierran al terminar. Cuando necesitan un archivo, usan la carpeta temporal `tmp_path` que conociste en la lección 7.

Después de cada ejercicio corre sus pruebas. Por ejemplo, para el ejercicio 1:

```bash
pytest lecciones/leccion_08_sqlite -k ejercicio_1
```

### Ejercicio 1. `abrir_base(ruta)`

Abre la base de datos guardada en `ruta` y devuelve la conexión. Si la carpeta del archivo no existe, la crea primero.

| Entrada | Resultado |
| --- | --- |
| `abrir_base(Path("salida") / "tienda.db")` | Una conexión abierta; existen la carpeta `salida` y, dentro, `tienda.db` |
| La misma llamada otra vez | Una conexión a la misma base, con lo que ya tenía guardado |

Paso a paso:

1. Obtén la carpeta que contiene al archivo.
2. Crea esa carpeta, de modo que no falle si ya existe ni si faltan carpetas intermedias.
3. Abre la conexión con la ruta recibida.
4. Devuelve la conexión.

<details>
<summary>Pista 1</summary>

Todo lo que necesitas está en el concepto 2: `ruta.parent`, `mkdir()` con sus dos argumentos y `sqlite3.connect()`.

</details>

<details>
<summary>Pista 2</summary>

Si la prueba dice `unable to open database file`, la carpeta no se creó antes de conectar. Si dice que la función devolvió `None`, te falta el `return`.

</details>

### Ejercicio 2. `crear_tabla(conexion)`

Crea la tabla `pedidos` con sus ocho columnas, sus tipos y su clave primaria. Llamarla dos veces no debe fallar ni borrar datos. No devuelve nada.

| Entrada | Resultado |
| --- | --- |
| `crear_tabla(conexion)` | La base tiene la tabla `pedidos`, vacía |
| `crear_tabla(conexion)` por segunda vez | No hay error y la tabla conserva sus filas |

Paso a paso:

1. Escribe la instrucción `CREATE TABLE` entre comillas triples, con una columna por renglón.
2. Dale a cada columna su tipo: los enteros, los decimales y los textos.
3. Marca `id_pedido` como clave primaria.
4. Envía la instrucción con el método de la conexión que ejecuta SQL.

<details>
<summary>Pista 1</summary>

Si la segunda llamada falla con `table pedidos already exists`, te faltan tres palabras en la instrucción. Están en el concepto 3.

</details>

<details>
<summary>Pista 2</summary>

Las pruebas revisan el nombre, el orden y el tipo de cada columna. Compara tu instrucción, renglón por renglón, con la lista de columnas del docstring de `ejercicios.py`.

</details>

### Ejercicio 3. `insertar_pedido(conexion, pedido)`

Inserta un pedido que llega como diccionario y confirma el cambio. No devuelve nada y no modifica el diccionario.

| Entrada | Resultado |
| --- | --- |
| Un pedido con `"id_pedido": 1`, `"cliente": "Ana López"`... | La tabla tiene una fila más, con cada valor en su columna |
| Un pedido con `"producto": 'Taza "La Abuela\'s"'` | Se guarda el texto tal cual, con sus comillas y su apóstrofo |
| Un pedido cuyo `id_pedido` ya existe | `sqlite3.IntegrityError` |

Paso a paso:

1. Escribe el SQL del `INSERT` con un `?` por cada columna.
2. Arma una tupla con los ocho valores del diccionario, en el orden de las columnas de la tabla.
3. Ejecuta el SQL pasando la tupla como segundo argumento.
4. Confirma el cambio.

<details>
<summary>Pista 1</summary>

El diccionario puede traer sus claves en cualquier orden. Toma cada valor por su clave, por ejemplo `pedido["fecha"]`, y colócalo en la posición que le toca dentro de la tupla.

</details>

<details>
<summary>Pista 2</summary>

Si falla la prueba que cierra la base y la vuelve a abrir, relee el concepto 6. Para el `id_pedido` repetido no tienes que escribir nada: el error lo lanza SQLite por la clave primaria, y tu función solo debe dejarlo pasar.

</details>

### Ejercicio 4. `insertar_varios(conexion, pedidos)`

Inserta una lista de pedidos (diccionarios) con `executemany`, confirma el cambio y devuelve cuántos insertó.

| Entrada | Resultado |
| --- | --- |
| `insertar_varios(conexion, [pedido_1, pedido_2, pedido_3])` | `3`, y la tabla tiene tres filas más |
| `insertar_varios(conexion, [])` | `0`, y la tabla queda igual |

Paso a paso:

1. Crea una lista vacía para las tuplas.
2. Recorre los pedidos y, por cada uno, agrega a la lista su tupla de ocho valores.
3. Envía el `INSERT` y la lista de tuplas con `executemany`.
4. Confirma el cambio.
5. Devuelve cuántos pedidos insertaste.

<details>
<summary>Pista 1</summary>

En el paso 2 necesitas la misma conversión de diccionario a tupla que hiciste en el ejercicio 3. Si la sacas a una función propia, por ejemplo `pedido_a_fila(pedido)`, la escribes una sola vez y la usas en los dos ejercicios.

</details>

<details>
<summary>Pista 2</summary>

Para el paso 5 no hace falta preguntarle nada a la base: ya tienes una lista y sabes medir su tamaño.

</details>

### Ejercicio 5. `contar_pedidos(conexion)`

Devuelve cuántas filas tiene la tabla `pedidos`, como número entero.

| Entrada | Resultado |
| --- | --- |
| `contar_pedidos(conexion)` con la tabla vacía | `0` |
| `contar_pedidos(conexion)` con ocho pedidos | `8` |

Paso a paso:

1. Ejecuta la consulta que cuenta las filas de la tabla.
2. Trae la única fila del resultado.
3. Saca el número de esa fila y devuélvelo.

<details>
<summary>Pista</summary>

Si la prueba dice que obtuviste `(8,)` en lugar de `8`, estás devolviendo la tupla completa. El número está en su primera posición.

</details>

### Ejercicio 6. `buscar_por_ciudad(conexion, ciudad)`

Devuelve los pedidos de una ciudad como lista de diccionarios, cada uno con las ocho columnas, ordenados por `id_pedido`. Si la ciudad no tiene pedidos, devuelve una lista vacía.

| Entrada | Resultado |
| --- | --- |
| `buscar_por_ciudad(conexion, "Mérida")` | `[{"id_pedido": 4, "fecha": "2024-03-02", ...}]` |
| `buscar_por_ciudad(conexion, "Ek' Balam")` | Los pedidos de esa ciudad; el apóstrofo no causa ningún error |
| `buscar_por_ciudad(conexion, "Atlantis")` | `[]` |

Paso a paso:

1. Escribe un `SELECT` con las ocho columnas, una por una, que filtre por ciudad con un parámetro y ordene por `id_pedido`.
2. Ejecútalo pasando la ciudad en una tupla y trae todas las filas.
3. Crea una lista vacía.
4. Recorre las filas y, por cada una, arma un diccionario con las ocho claves y agrégalo a la lista.
5. Devuelve la lista.

<details>
<summary>Pista 1</summary>

Si aparece `Incorrect number of bindings supplied`, revisa la tupla del paso 2. Una tupla de un solo elemento lleva una coma antes de cerrar el paréntesis.

</details>

<details>
<summary>Pista 2</summary>

El paso 4 es el bucle del concepto 8, con ocho claves en lugar de tres. Las claves del diccionario se llaman igual que las columnas, y la posición de cada valor en la fila es la de su columna en tu `SELECT`.

</details>

<details>
<summary>Pista 3</summary>

Una de las pruebas busca la ciudad `Mérida' OR '1' = '1` y espera una lista vacía. Si tu función devuelve todos los pedidos, estás armando el SQL con el texto de la ciudad. Relee el concepto 5.

</details>

### Ejercicio 7. `ventas_por_ciudad(conexion)`

Devuelve el total vendido en cada ciudad como lista de tuplas `(ciudad, total)`. El total es la suma de `cantidad * precio_unitario`, redondeada a dos decimales. Los pedidos cancelados no cuentan. La lista va del total más alto al más bajo.

| Pedidos en la tabla | Resultado |
| --- | --- |
| Puebla: 2 piezas de 100.0, entregado. Puebla: 5 piezas de 100.0, cancelado. Tijuana: 9 piezas de 100.0, cancelado | `[('Puebla', 200.0)]` |
| Puebla: 3 piezas de 19.99 y 3 piezas de 0.1, ninguno cancelado | `[('Puebla', 60.27)]` |
| Ninguno | `[]` |

Paso a paso:

1. Empieza por una consulta que devuelva la ciudad y la suma de `cantidad * precio_unitario`, agrupada por ciudad. Pruébala.
2. Agrega el filtro que deja fuera los pedidos cuyo estado es `cancelado`.
3. Redondea la suma a dos decimales y ponle un nombre.
4. Ordena por ese nombre, de mayor a menor.
5. Ejecuta la consulta y devuelve todas las filas.

<details>
<summary>Pista 1</summary>

Cada paso corresponde a una pieza del concepto 9. Constrúyela de a una pieza y corre las pruebas cada vez: el mensaje te dice cuál falta.

</details>

<details>
<summary>Pista 2</summary>

Recuerda el orden de las partes: `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`. Un `WHERE` colocado después de `GROUP BY` produce un `OperationalError` con `syntax error`.

</details>

<details>
<summary>Pista 3</summary>

`fetchall()` ya entrega una lista de tuplas. Si tu `SELECT` pide exactamente dos columnas, no necesitas ningún bucle para darle forma al resultado.

</details>

## Evalúate

Cuando termines los siete ejercicios, corre la lección completa:

```bash
pytest lecciones/leccion_08_sqlite
```

Debes ver `46 passed`. Si una prueba falla, lee la línea que empieza con `E`: te dice con qué valores se probó, qué se esperaba y qué devolvió tu función. Si la línea `E` empieza con `sqlite3.`, el error viene de la base: revisa primero el texto de tu SQL.

Revisa también el estilo de tu código:

```bash
ruff check lecciones/leccion_08_sqlite
```

Y guarda tu trabajo:

```bash
git add .
git commit -m "Completa la lección 8"
git push
```

## Repaso

Responde de memoria antes de pasar a la siguiente lección. Si no recuerdas algo, intenta primero y revisa después.

1. ¿Qué ventajas tiene una base de datos frente a un archivo CSV? Menciona dos.
2. ¿Por qué los valores se pasan con `?` y no con un f-string?
3. ¿Qué pasa con lo que insertaste si cierras la conexión sin `commit()`?
4. ¿Qué devuelve `fetchall()`? ¿Y `fetchone()` cuando no hay filas?
5. ¿Qué error aparece al insertar dos veces la misma clave primaria?
6. ¿En qué se parece `GROUP BY ciudad` a acumular en un diccionario con `.get(ciudad, 0)`?
7. De la lección 7: ¿para qué sirve `tmp_path` en una prueba?
8. De la lección 1: ¿por qué redondeamos los importes con `round(valor, 2)`?

Vuelve a estas preguntas dentro de dos o tres días. Repasar espaciado en el tiempo rinde más que repasar muchas veces el mismo día.

## Si te atoras

1. Lee el mensaje de la prueba completo. Casi siempre trae la respuesta.
2. Imprime el texto de tu SQL con `print(sql)` y léelo despacio: la mayoría de los `OperationalError` son una coma, un paréntesis o una palabra mal escrita.
3. Prueba tu consulta a mano: abre el intérprete con `python`, conéctate a `":memory:"`, crea la tabla, inserta dos o tres filas y ejecuta la consulta.
4. Revisa los ejemplos resueltos de `ejemplos.py`.
5. Abre las pistas del ejercicio, una a la vez.
6. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Bill Lubanovic, *Introducing Python*, capítulo 8, "Data Has to Go Somewhere": bases de datos relacionales, SQL, la DB-API de Python y SQLite.
- Documentación de Python, módulo `sqlite3`: `connect`, `execute`, `executemany`, `commit`, `fetchone`, `fetchall`, `close`, el uso de parámetros con `?` y las excepciones `OperationalError` e `IntegrityError`.
- Brian Okken, *Python Testing with pytest*, capítulo 3, "pytest Fixtures": cómo las pruebas de esta lección preparan una base de datos y la cierran al terminar.
- Felienne Hermans, *The Programmer's Brain*, capítulo 3, "How to learn programming syntax quickly": por qué intentar recordar antes de buscar y por qué conviene repasar espaciado.
