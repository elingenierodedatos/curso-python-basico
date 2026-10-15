# Plan de estudios

**Curso:** Python básico para ingeniería de datos
**Modalidad:** a tu ritmo, con ejercicios evaluados por pruebas unitarias
**Duración estimada:** 24 horas de trabajo (16 de lecciones y 8 de proyecto)
**Costo:** gratuito

## A quién va dirigido

A quien quiere empezar en ingeniería de datos y nunca ha programado, o programó poco y sin método. No necesitas conocimientos previos de programación. Sí necesitas una computadora con Windows, macOS o Linux, y disposición para escribir código todos los días que estudies.

## Qué vas a poder hacer al terminar

1. Escribir funciones de Python claras, con buen estilo y documentadas.
2. Limpiar y validar datos que llegan como texto: precios, fechas, ciudades, faltantes.
3. Leer y escribir archivos CSV y JSON de forma que funcionen en cualquier sistema operativo.
4. Manejar errores sin esconderlos: rechazar el dato inválido y dejar constancia del motivo.
5. Escribir y leer pruebas unitarias con pytest.
6. Guardar datos en una base SQLite y consultarlos con SQL básico.
7. Organizar un proyecto en módulos y publicarlo en GitHub.
8. Construir un flujo de datos completo: extraer, limpiar, cargar y reportar.

## Cómo se aprende en este curso

Cada decisión de diseño tiene un sustento. Estas son las principales.

| Decisión | Por qué | Sustento |
| --- | --- | --- |
| Cada lección abre con ejemplos resueltos y después pide ejercicios | A quien empieza, estudiar un ejemplo explicado le rinde más que enfrentarse a un problema en blanco: la memoria de trabajo se satura con facilidad | Hermans, cap. 4 (carga cognitiva) |
| Ejercicios cortos, de un solo concepto nuevo | La práctica dirigida a una habilidad concreta es la que construye dominio | Hermans, cap. 2 (práctica deliberada); Lerner, cap. 1 |
| Cada lección te hace provocar un error a propósito | Leer un error es una habilidad que se entrena. Verlo primero en un entorno controlado quita el miedo | Matthes, cap. 2 a 6: provoca y explica `NameError`, `IndexError`, `IndentationError` y `KeyError` |
| Todo ejercicio se evalúa con pruebas unitarias | La retroalimentación inmediata y exacta permite corregir en el momento. Además, leer pruebas desde el primer día prepara para escribirlas | Matthes, cap. 11; Okken, cap. 1 |
| Preguntas de repaso al final, para responder de memoria | Intentar recordar fija más que releer, y repasar espaciado rinde más que repasar seguido | Hermans, cap. 3 |
| Sin asistentes de IA durante el curso | Delegar el código produce ilusión de progreso y evita el esfuerzo que construye la memoria | Lerner, sección 1.5; Hermans, cap. 3. Detalle en [por-que-sin-ia.md](por-que-sin-ia.md) |
| Un solo dominio en todo el curso: pedidos de una tienda en línea | Reutilizar el mismo contexto reduce la carga que no aporta, y deja la atención para el concepto nuevo | Hermans, cap. 4; Matthes reutiliza el mismo programa entre ejercicios |
| Nombres en español, descriptivos y sin abreviar | Un buen nombre le ahorra trabajo a la memoria de quien lee | Hermans, cap. 8; Matthes, cap. 2 |
| Rutas con `pathlib` y codificación UTF-8 explícita | El mismo código debe correr en Windows, macOS y Linux | Matthes, cap. 10 |

## Contenido

| # | Lección | Tiempo | Pruebas |
| --- | --- | --- | --- |
| 0 | Preparación | 45 min | 2 |
| 1 | Variables, texto y números | 90 min | 29 |
| 2 | Listas y bucles | 120 min | 36 |
| 3 | Decisiones con if y bucles while | 100 min | 64 |
| 4 | Diccionarios y conjuntos | 120 min | 35 |
| 5 | Funciones y módulos | 100 min | 53 |
| 6 | Archivos y manejo de errores | 120 min | 63 |
| 7 | Pruebas con pytest | 140 min | 42 |
| 8 | Guardar y consultar datos con SQLite | 120 min | 46 |
| P | Proyecto final: flujo de ventas | 8 h | 105 |

El curso se aprueba cuando las 475 pruebas pasan.

### Lección 0. Preparación

- **Temas:** instalar Python y Git, crear tu copia del repositorio, entorno virtual, instalar dependencias, correr pytest, leer una prueba fallida, guardar tu trabajo con Git.
- **Por qué va aquí:** un entorno mal configurado es la primera causa de abandono. Dejarlo resuelto y comprobado con una prueba real evita que los problemas de instalación se confundan con problemas de programación.
- **Por qué importa en datos:** los entornos aislados y el control de versiones son la base del trabajo reproducible.
- **Referencias:** Matthes, cap. 1 y 11; Okken, cap. 1.

### Lección 1. Variables, texto y números

- **Temas:** variables y reglas de nombres, `str`, `int` y `float`, métodos de texto, f-strings, conversión de texto a número, redondeo, formato de importes, comentarios, lectura de `NameError` y `ValueError`, la forma mínima de una función (`def` y `return`) para poder entregar los ejercicios.
- **Por qué va aquí:** son las piezas más pequeñas del lenguaje; todo lo demás se construye con ellas.
- **Por qué importa en datos:** los archivos entregan todo como texto. Convertir `"$1,250.50"` en un número confiable es el primer trabajo de cualquier flujo de datos.
- **Referencias:** Matthes, cap. 2; Lerner, cap. 2 y 3; Hermans, cap. 3.

### Lección 2. Listas y bucles

- **Temas:** listas, índices, `append`, `len`, `sorted` frente a `sort`, bucle `for`, sangría, patrón acumulador, `range`, `sum`, `min`, `max`, slices, copia de listas, tuplas, estilo PEP 8.
- **Por qué va aquí:** con un solo valor no se hace análisis. La lista y el bucle permiten aplicar lo de la lección 1 a muchos datos.
- **Por qué importa en datos:** una columna es una lista. Recorrerla, acumular y ordenar son las operaciones de las que nacen los totales y los promedios.
- **Referencias:** Matthes, cap. 3 y 4; Lerner, cap. 4; Hermans, cap. 3 y 7.

### Lección 3. Decisiones con if y bucles while

- **Temas:** booleanos, comparaciones, `and`, `or`, `not`, `in`, `isinstance`, `if-elif-else`, `None`, filtrar y contar dentro de un `for`, `while` y `break`, cuándo usar cada bucle.
- **Por qué va aquí:** hasta ahora el código trata igual a todos los datos. Decidir permite separar lo válido de lo inválido.
- **Por qué importa en datos:** validar, clasificar y detectar faltantes son decisiones. Un `elif` en el orden equivocado no lanza error: produce cifras incorrectas.
- **Referencias:** Matthes, cap. 5 y 7; Lubanovic, cap. 4.

### Lección 4. Diccionarios y conjuntos

- **Temas:** diccionario como registro, `get`, recorrer con `items`, lista de diccionarios como tabla, conteo y suma por grupo, conjuntos para valores únicos, copiar frente a compartir.
- **Por qué va aquí:** las listas guardan una columna; el diccionario guarda una fila completa con nombre para cada dato.
- **Por qué importa en datos:** la lista de diccionarios es la forma en que Python representa una tabla. La suma por grupo que aquí se hace a mano es el `GROUP BY` que se verá en SQL.
- **Referencias:** Matthes, cap. 6; Lubanovic, cap. 3; Lerner, cap. 5.

### Lección 5. Funciones y módulos

- **Temas:** anatomía de una función, parámetros y argumentos, `return` frente a `print`, valores por defecto, argumentos por nombre, devolver varios valores, alcance de las variables, docstrings, módulos e `import`, estilo de funciones.
- **Por qué va aquí:** el alumno ya completó decenas de funciones; ahora las escribe enteras y las organiza. Llegar a la definición formal después de usarlas hace que el concepto tenga dónde anclarse.
- **Por qué importa en datos:** una función que hace una sola cosa se puede probar sola y reutilizar. Un flujo de datos es una cadena de funciones pequeñas.
- **Referencias:** Matthes, cap. 8; Lubanovic, cap. 5; Lerner, cap. 7; Hermans, cap. 8.

### Lección 6. Archivos y manejo de errores

- **Temas:** rutas con `pathlib`, lectura y escritura de texto, codificación UTF-8, `try-except-else`, `raise`, CSV con `DictReader` y `DictWriter`, JSON.
- **Por qué va aquí:** con funciones y estructuras de datos ya dominadas, el alumno puede dejar los datos de juguete y trabajar con archivos reales.
- **Por qué importa en datos:** casi todo flujo empieza y termina en un archivo. Un error que se calla produce un reporte equivocado, así que se enseña a rechazar con motivo y no a esconder.
- **Referencias:** Matthes, cap. 10; Lubanovic, cap. 8; Lerner, cap. 6.

### Lección 7. Pruebas con pytest

- **Temas:** las funciones como valores (pasar una función como argumento), qué es una prueba unitaria, `assert`, preparar, actuar y comprobar, lectura detallada de un fallo, `pytest.raises`, parametrización, fixtures, qué casos elegir, opciones de pytest y su configuración.
- **Por qué va aquí:** tras seis lecciones leyendo pruebas ajenas, el alumno conoce el formato y puede concentrarse en lo difícil: decidir qué probar. Las funciones como valores se enseñan aquí, y no en la lección 5, porque es aquí donde se necesitan: cada comprobación recibe la función que debe revisar.
- **Por qué importa en datos:** en datos el error no avisa; aparece como una cifra equivocada en un tablero. Las pruebas son lo que separa un script de un trabajo de ingeniería.
- **Cómo se evalúa:** las pruebas del alumno se corren contra una implementación correcta y contra varias defectuosas. Deben aprobar la primera y detectar las demás.
- **Referencias:** Matthes, cap. 11; Okken, cap. 1, 2, 3 y 6.

### Lección 8. Guardar y consultar datos con SQLite

- **Temas:** por qué una base de datos, SQL mínimo (`CREATE TABLE`, `INSERT`, `SELECT`, `WHERE`, `ORDER BY`, `COUNT`, `SUM`, `GROUP BY`), el módulo `sqlite3`, parámetros con `?`, `commit`, claves primarias.
- **Por qué va aquí:** es el destino natural de los datos limpios y la puerta a SQL, el otro lenguaje indispensable del oficio.
- **Por qué importa en datos:** cargar a una base y consultarla es la mitad del trabajo diario. SQLite viene con Python y corre igual en todos los sistemas, así que se aprende el concepto sin instalar un servidor. Los parámetros se enseñan desde el primer `INSERT` porque armar SQL pegando textos es un riesgo de seguridad.
- **Referencias:** Lubanovic, cap. 8; documentación de Python, módulo `sqlite3`.

### Proyecto final. Flujo de ventas

- **Qué se construye:** un flujo que lee 63 pedidos crudos de un CSV, los limpia y valida, rechaza con motivo los que no se pueden corregir, carga los válidos en SQLite y genera un reporte de ventas en JSON.
- **Por qué cierra el curso:** obliga a combinar todas las lecciones en un programa organizado en módulos, con menos guía y con datos sucios de verdad.
- **Qué demuestra en tu portafolio:** que sabes llevar datos de un archivo sucio a un resultado confiable, con pruebas que lo respaldan.
- **Referencias:** Matthes, cap. 10 (refactorizar en funciones de una sola tarea); Lubanovic, cap. 8; Okken, cap. 3.

## Qué no cubre este curso, y por qué

| Tema | Motivo |
| --- | --- |
| Clases y programación orientada a objetos | No hacen falta para un primer flujo de datos y duplican la carga conceptual |
| Comprensiones, `lambda` y decoradores | Son atajos; primero se aprende la forma larga y explícita |
| pandas y otras bibliotecas | Sin dominar listas y diccionarios, pandas se usa de memoria y sin entender |
| Anotaciones de tipo | Útiles en equipos; se dejan para el siguiente curso |
| Docker y nube | El curso corre con Python y nada más, para que la instalación no sea una barrera |

## Evaluación

- Cada ejercicio tiene pruebas unitarias. Las corres en tu computadora con `pytest`, y GitHub las corre de nuevo en Windows, macOS y Linux cada vez que subes cambios.
- `python progreso.py` muestra tu avance por lección.
- No hay exámenes ni calificación subjetiva: el código pasa las pruebas o no las pasa.

## Ritmo sugerido

| Semana | Contenido |
| --- | --- |
| 1 | Lecciones 0, 1 y 2 |
| 2 | Lecciones 3, 4 y 5 |
| 3 | Lecciones 6, 7 y 8 |
| 4 | Proyecto final |

Seis horas por semana, repartidas en varios días. Estudiar una hora diaria rinde más que seis horas seguidas el domingo.

## Bibliografía

El contenido del curso es original. Estos libros sustentan el orden de los temas y el método; si quieres profundizar, son los que recomendamos.

- Eric Matthes. *Python Crash Course*, 3.ª edición. No Starch Press, 2023. Columna vertebral de las lecciones 1 a 7.
- Bill Lubanovic. *Introducing Python*. O'Reilly Media. Estructuras de datos, módulos, archivos, CSV y SQLite.
- Brian Okken. *Python Testing with pytest*. Pragmatic Bookshelf. Lección 7 y diseño de las pruebas del curso.
- Reuven Lerner. *Python Workout*, 2.ª edición. Manning. Formato de los ejercicios y postura sobre la IA al aprender.
- Felienne Hermans. *The Programmer's Brain*. Manning, 2021. Fundamento del método de enseñanza.
