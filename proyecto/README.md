# Proyecto final: Flujo de ventas

Llegó un archivo con los pedidos del trimestre de una tienda en línea. Dirección quiere saber cuánto se vendió por ciudad y por producto. El archivo viene como vienen los datos reales: precios con símbolos, ciudades escritas de cinco formas, fechas en dos formatos, filas repetidas y valores que faltan.

Tu trabajo es construir el flujo de datos que convierte ese archivo en un reporte confiable.

**Tiempo estimado:** 8 horas.
**Antes de empezar:** completa las lecciones 0 a 8.

## Qué vas a construir

```text
pedidos_crudos.csv
       |
   1. extraer     lee el archivo tal como llega
       |
   2. limpiar     corrige lo que se puede, rechaza lo que no y anota el motivo
       |
   3. cargar      guarda los pedidos limpios en SQLite
       |
   4. reportar    consulta la base y arma el reporte
       |
salida/ventas.db   salida/reporte.json   salida/rechazados.csv
```

En la industria, a un flujo así se le llama *pipeline* de datos, y a las tres primeras etapas, ETL: extraer, transformar y cargar.

## Cómo está organizado

```text
proyecto/
├── datos/pedidos_crudos.csv    los 63 pedidos de entrada (no lo modifiques)
├── flujo_ventas/               tu código
│   ├── extraer.py              etapa 1
│   ├── limpiar.py              etapa 2
│   ├── cargar.py               etapa 3
│   ├── reportar.py             etapa 4
│   └── principal.py            une las cuatro etapas
├── tests/                      las pruebas (no las modifiques)
└── ejecutar.py                 corre el flujo con los datos del proyecto
```

Cada etapa vive en su propio módulo y no sabe cómo trabajan las demás: solo recibe datos y entrega datos. Por eso puedes construirlas y probarlas una por una.

## En qué se distingue de las lecciones

- **No hay pistas.** Cada función tiene un docstring que es su contrato: qué recibe, qué devuelve y qué errores lanza. Léelo completo antes de escribir.
- **Los datos están sucios de verdad.** Abre `datos/pedidos_crudos.csv` y revísalo antes de programar. Entender los datos es parte del trabajo.
- **Las etapas dependen unas de otras.** Sigue el orden.

## Reglas del negocio

| Regla | Detalle |
| --- | --- |
| Nada se descarta en silencio | Un pedido que no se puede corregir se rechaza, con su número de fila y el motivo |
| Un id, un pedido | Si un `id_pedido` se repite, se conserva el primero y los demás se rechazan |
| Una venta no está cancelada | Los pedidos cancelados se cargan en la base, pero no cuentan en las ventas |
| El flujo se puede repetir | Correrlo dos veces da el mismo resultado, sin duplicar filas |

## Paso a paso

Trabaja una etapa a la vez. Corre sus pruebas, corrige y avanza solo cuando todas pasen.

### Etapa 1. Extraer

Archivo: `flujo_ventas/extraer.py`. Una función.

```bash
pytest proyecto/tests/test_1_extraer.py
```

Aplica lo de la lección 6: `pathlib`, `csv.DictReader`, codificación y errores con mensaje claro.

### Etapa 2. Limpiar

Archivo: `flujo_ventas/limpiar.py`. Cinco funciones, de la más pequeña a la más grande. Resuélvelas en el orden en que aparecen: cada una usa las anteriores.

```bash
pytest proyecto/tests/test_2_limpiar.py
```

Es la etapa más larga. El archivo ya trae tres constantes para que no tengas que escribirlas: `FALTANTES`, `CIUDADES` y `ESTADOS`.

Para correr solo las pruebas de una función:

```bash
pytest proyecto/tests/test_2_limpiar.py -k limpiar_fecha
```

### Etapa 3. Cargar

Archivo: `flujo_ventas/cargar.py`. Tres funciones.

```bash
pytest proyecto/tests/test_3_cargar.py
```

Aplica lo de la lección 8. La parte nueva es que la carga debe poder repetirse.

### Etapa 4. Reportar

Archivo: `flujo_ventas/reportar.py`. Cinco funciones.

```bash
pytest proyecto/tests/test_4_reportar.py
```

Decide qué resolver con SQL y qué con Python. Las dos opciones son válidas si las pruebas pasan.

### Etapa 5. Unir el flujo

Archivo: `flujo_ventas/principal.py`. Dos funciones.

```bash
pytest proyecto/tests/test_5_flujo_completo.py
```

Aquí no hay lógica nueva: se trata de llamar a cada etapa en orden y pasar el resultado a la siguiente.

## Lo que necesitas y no vimos en las lecciones

Son cuatro piezas pequeñas. Búscalas en la documentación de Python o de SQLite antes de usarlas: leer documentación es parte del oficio.

| Pieza | Para qué sirve aquí |
| --- | --- |
| `texto.capitalize()` | Deja en mayúscula solo la primera letra del texto |
| `f"{numero:02d}"` | Muestra un entero con dos dígitos, rellenando con cero |
| `INSERT OR REPLACE INTO ...` | Inserta la fila, o la reemplaza si la clave primaria ya existe |
| `try: ... finally: ...` | El bloque `finally` corre siempre, haya error o no; sirve para cerrar la conexión |

## Corre el flujo completo

Cuando las pruebas pasen:

```bash
python proyecto/ejecutar.py
```

Verás el resumen en la terminal y tres archivos en `proyecto/salida/`:

- `ventas.db`: la base con los pedidos limpios.
- `reporte.json`: las ventas por ciudad y por producto.
- `rechazados.csv`: los pedidos que no se cargaron, con su motivo.

Abre los tres y revísalos. Luego responde, consultando tus resultados:

1. ¿Qué ciudad vendió más y cuánto?
2. ¿Qué producto dejó más ingresos? ¿Es el mismo que vendió más unidades?
3. ¿Cuál fue el motivo de rechazo más frecuente?
4. ¿Cuánto dinero dejó de contarse por pedidos cancelados? Para saberlo necesitas escribir tu propia consulta SQL sobre `ventas.db`.

## Evalúate

```bash
pytest proyecto
```

Debes ver `105 passed`. Después revisa el estilo y tu avance total:

```bash
ruff check proyecto
ruff format proyecto
python progreso.py
```

## Hazlo tuyo

El curso termina cuando las pruebas pasan. Tu portafolio empieza cuando le agregas algo propio. Algunas ideas, de menor a mayor esfuerzo:

1. **Escribe tus propias pruebas.** Crea `proyecto/tests/test_mis_pruebas.py` con casos que se te ocurran y que las nuestras no cubren.
2. **Agrega ventas por mes** al reporte, a partir de la columna `fecha`.
3. **Agrega una regla de validación**, por ejemplo rechazar fechas futuras, con su motivo y sus pruebas.
4. **Acepta la ruta del archivo por la terminal**, para que el flujo sirva con otros archivos.
5. **Reescribe el README de tu repositorio** contando qué hace el flujo, cómo se corre y qué decisiones tomaste. Quien revise tu portafolio va a leer eso primero.

## Si te atoras

1. Lee el docstring otra vez, completo. Casi todas las dudas se responden ahí.
2. Lee el mensaje de la prueba que falla: dice con qué datos se probó.
3. Prueba la función a mano en el intérprete con ese mismo dato.
4. Vuelve a la lección del tema. La etapa 1 es la lección 6; la 2, las lecciones 1 a 6; la 3 y la 4, la lección 8.
5. Pregunta en la comunidad del curso, contando qué intentaste y qué error obtuviste.

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 10: archivos, excepciones y refactorización en funciones de una sola tarea.
- Bill Lubanovic, *Introducing Python*, capítulo 8, "Data Has to Go Somewhere": CSV, JSON y SQLite.
- Brian Okken, *Python Testing with pytest*, capítulo 3: fixtures como las de `tests/conftest.py`.
- Documentación de Python, módulos `csv`, `json`, `pathlib` y `sqlite3`.
