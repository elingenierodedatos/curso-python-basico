# Cómo leer un error

Un error es Python diciéndote qué pasó y dónde. Leerlo con calma ahorra más tiempo que cualquier otra habilidad del curso.

## Un error de Python

```text
Traceback (most recent call last):
  File "prueba.py", line 2, in <module>
    print(mensage)
          ^^^^^^^
NameError: name 'mensage' is not defined. Did you mean: 'mensaje'?
```

Léelo de abajo hacia arriba:

1. **La última línea** trae el tipo de error y la explicación.
2. **La línea con `File`** trae el archivo y el número de renglón.
3. **El renglón señalado** es el código que falló.

Si el error ocurre dentro de una función llamada por otra, verás varias líneas `File`. La de más abajo es donde falló; las de arriba cuentan cómo se llegó ahí.

## Una prueba fallida

```text
E   AssertionError: Con texto=' $1,250.50 ' se esperaba 1250.5 y se obtuvo 1.0. Antes de convertir, quita los espacios, el símbolo $ y las comas.
```

1. **La última línea de toda la salida** dice cuántas pruebas fallaron y cuántas pasaron.
2. **Las líneas que empiezan con `E`** dicen con qué valores se probó, qué se esperaba y qué devolvió tu función.
3. **El nombre de la prueba** dice qué comportamiento se estaba revisando, por ejemplo `test_ejercicio_3_convierte_precios_con_simbolos`.

Opciones útiles al corregir:

| Comando | Para qué |
| --- | --- |
| `pytest lecciones/leccion_01_variables_y_texto -k ejercicio_3` | Correr solo un ejercicio |
| `pytest lecciones/leccion_01_variables_y_texto -x` | Detenerse en el primer fallo |
| `pytest lecciones/leccion_01_variables_y_texto -v` | Ver el nombre de cada prueba |

## Los errores más comunes

| Error | Qué significa | Causa frecuente |
| --- | --- | --- |
| `NameError` | Usaste un nombre que Python no conoce | Variable o función mal escrita, o usada antes de crearla |
| `SyntaxError` | El código está mal escrito y Python no puede leerlo | Faltan dos puntos, una comilla o un paréntesis; `=` donde iba `==` |
| `IndentationError` | La sangría no es la esperada | Falta sangría después de `def`, `for` o `if`, o se mezclaron espacios |
| `TypeError` | La operación no aplica a ese tipo de dato | Sumar texto con número; llamar una función con argumentos de más o de menos |
| `ValueError` | El tipo es correcto pero el contenido no sirve | `int("dos")`, `float("$10")` |
| `IndexError` | Pediste una posición que no existe en la lista | Olvidar que los índices empiezan en 0; lista vacía |
| `KeyError` | Pediste una clave que no existe en el diccionario | Clave mal escrita o con otra combinación de mayúsculas |
| `AttributeError` | Ese valor no tiene el método que pediste | Usar un método de texto sobre un número o sobre `None` |
| `FileNotFoundError` | El archivo no existe en esa ruta | Ruta mal escrita, o comando corrido desde otra carpeta |
| `ModuleNotFoundError` | Python no encuentra el módulo | Entorno virtual sin activar, o comando corrido fuera de la carpeta principal |
| `NotImplementedError` | La función sigue con el aviso inicial | Todavía no borras la línea `raise NotImplementedError(...)` |
| `AssertionError` | Una prueba comprobó algo y no se cumplió | Tu función devuelve un valor distinto al esperado |

## Cuando no entiendes el error

1. Lee el mensaje completo, despacio. Copia el tipo de error en tus notas.
2. Ve al renglón que indica y lee también el anterior: muchas veces el problema está una línea arriba.
3. Reproduce el problema en pequeño: abre el intérprete con `python` y prueba esa sola línea.
4. Si deshiciste algo y volvió a funcionar, ya sabes dónde está.
5. Pregunta en la comunidad con tres datos: qué intentabas, qué código escribiste y el error completo.
