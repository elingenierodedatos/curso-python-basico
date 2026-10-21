# Python básico para ingeniería de datos

Aprende Python desde cero limpiando datos reales. Completas funciones, corres pruebas y terminas con un flujo de datos propio en tu GitHub.

Un curso gratuito de **EL INGENIERO DE DATOS**. Ensúciate las manos con datos reales.

## Qué vas a construir

Al final del curso tendrás un flujo que lee un archivo de pedidos sucio, lo limpia, rechaza con motivo lo que no se puede corregir, carga el resto en una base de datos y genera un reporte de ventas. Todo respaldado por pruebas y publicado en tu repositorio.

Son **475 pruebas** en total, repartidas entre las nueve lecciones y el proyecto. El curso se aprueba cuando todas pasan; `python progreso.py` te dice cuántas llevas.

## Cómo funciona

1. Lees la guía de la lección, con ejemplos resueltos.
2. Completas las funciones del archivo de ejercicios.
3. Corres las pruebas. Te dicen qué esperaban y qué obtuvieron.
4. Corriges hasta que pasen y subes tu avance a GitHub.

No hay exámenes: el código pasa las pruebas o no las pasa.

## Contenido

| # | Lección | Qué aprendes |
| --- | --- | --- |
| 0 | [Preparación](lecciones/leccion_00_preparacion/README.md) | Instalar todo, correr tu primera prueba y leer un error |
| 1 | [Variables, texto y números](lecciones/leccion_01_variables_y_texto/README.md) | Convertir texto sucio en datos utilizables |
| 2 | [Listas y bucles](lecciones/leccion_02_listas_y_bucles/README.md) | Trabajar con una columna completa |
| 3 | [Decisiones con if y bucles while](lecciones/leccion_03_condicionales/README.md) | Validar, clasificar y detectar faltantes |
| 4 | [Diccionarios y conjuntos](lecciones/leccion_04_diccionarios/README.md) | Representar filas y agrupar |
| 5 | [Funciones y módulos](lecciones/leccion_05_funciones_y_modulos/README.md) | Escribir y organizar tu propio código |
| 6 | [Archivos y manejo de errores](lecciones/leccion_06_archivos_y_errores/README.md) | Leer y escribir CSV y JSON sin esconder errores |
| 7 | [Pruebas con pytest](lecciones/leccion_07_pruebas/README.md) | Escribir las pruebas que respaldan tu trabajo |
| 8 | [Guardar y consultar datos con SQLite](lecciones/leccion_08_sqlite/README.md) | Cargar a una base de datos y consultarla con SQL |
| P | [Proyecto final: Flujo de ventas](proyecto/README.md) | Unir todo en un flujo de datos completo |

Son unas 24 horas de trabajo. El detalle y el porqué de cada tema están en el [plan de estudios](docs/plan-de-estudios.md). Las diapositivas de cada lección están en [esta carpeta de Drive](https://drive.google.com/drive/folders/19aPe8Ya0xx4FG9uqNOr6ITV6ym_KvzM9?usp=sharing).

## Qué necesitas

- Una computadora con **Windows, macOS o Linux**. El curso corre igual en los tres y las pruebas se ejecutan en cada uno.
- **Python 3.10 o más reciente**. Las pruebas corren en GitHub con 3.10 y 3.13 en los tres sistemas.
- **Git** y una cuenta de GitHub.
- Un editor. Recomendamos Visual Studio Code.

No necesitas Docker, ni una base de datos instalada, ni una cuenta en la nube.

## Empieza aquí

1. Presiona **Use this template** y crea tu propia copia del repositorio.
2. Sigue la [lección 0](lecciones/leccion_00_preparacion/README.md). Te lleva paso a paso en Windows, macOS y Linux. Si prefieres instalar desde la terminal, está la [guía de instalación](docs/instalacion.md).

Si ya tienes Python 3.10 o superior y Git:

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
python -m venv .venv
```

Activa el entorno (`.venv\Scripts\Activate.ps1` en Windows, `source .venv/bin/activate` en macOS y Linux) y después:

```bash
python -m pip install -r requirements.txt
pytest lecciones/leccion_00_preparacion
```

## Comandos de todos los días

| Comando | Para qué |
| --- | --- |
| `pytest lecciones/leccion_01_variables_y_texto` | Evaluar una lección |
| `pytest lecciones/leccion_01_variables_y_texto -k ejercicio_3` | Evaluar un solo ejercicio |
| `python lecciones/leccion_01_variables_y_texto/ejemplos.py` | Correr los ejemplos resueltos |
| `python progreso.py` | Ver tu avance en todo el curso |
| `python actualizar.py` | Traer las novedades del curso sin tocar tu trabajo |
| `ruff check .` | Revisar el estilo de tu código |
| `ruff format .` | Dar formato a tu código |

## Recibir actualizaciones del curso

Tu copia se creó con **Use this template**, así que no comparte historial con el repositorio del curso y `git pull` no trae las novedades. Cuando anunciemos cambios (guías o pruebas corregidas, datos, una lección nueva), corre esto desde la carpeta de tu copia, con el entorno virtual activo:

```bash
python actualizar.py
```

El script se conecta con el repositorio del curso, descarga lo nuevo y copia solo los archivos del curso. **Tu trabajo no se toca:** los `ejercicios.py`, `limpieza.py` de la lección 5, tus pruebas de la lección 7 (`test_mis_pruebas.py`) y tu código del proyecto (`proyecto/flujo_ventas/`). Si el curso agrega una lección nueva, llega completa.

Al terminar te dice qué cambió y qué comandos siguen: reinstalar dependencias, `git commit` y `git push`. Si cambiaron las pruebas de una lección que ya resolviste, te avisa para que vuelvas a correrlas. Si tienes cambios sin guardar en algún archivo del curso, se detiene antes de reemplazarlos.

> Si modificaste un `ejemplos.py` para experimentar y lo guardaste con `git commit`, la actualización lo reemplaza por la versión del curso. Tu versión sigue en el historial de Git.

## Reglas del curso

- **Escribe tú el código.** Durante el curso, sin asistentes de IA. [Aquí explicamos por qué](docs/por-que-sin-ia.md).
- **No modifiques las pruebas.** Si una prueba falla, se corrige el código.
- **Avanza en orden.** Cada lección usa lo de las anteriores.
- **Lee los errores.** [Esta guía](docs/como-leer-un-error.md) te enseña cómo.
- **Pregunta cuando te atores.** La comunidad del curso vive en [Discord](https://discord.gg/tWtUXnAMuQ). Di qué lección, qué intentaste y pega el error completo.

## Cómo está organizado

```text
├── lecciones/          una carpeta por lección: guía, ejemplos, ejercicios y pruebas
├── proyecto/           el proyecto final
├── docs/               plan de estudios, glosario y guías de apoyo
├── progreso.py         muestra tu avance
├── actualizar.py       trae las novedades del curso
├── pyproject.toml      configuración de pytest y ruff
└── requirements.txt    dependencias del curso
```

Todo corre con Python y dos dependencias.

## Licencia

El código es MIT y las guías son CC BY-NC-SA 4.0. El detalle está en [LICENCIA-CONTENIDO.md](LICENCIA-CONTENIDO.md). Lo que tú escribas al resolver el curso es tuyo.

## Más de EL INGENIERO DE DATOS

- Sitio: [elingenierodedatos.com](https://elingenierodedatos.com)
- YouTube: [@elingenierodedatos](https://www.youtube.com/@elingenierodedatos)
- Discord: [comunidad del curso](https://discord.gg/tWtUXnAMuQ)
- GitHub: [github.com/elingenierodedatos](https://github.com/elingenierodedatos)
