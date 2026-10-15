# Lección 0: Preparación

Antes de escribir Python necesitas un lugar donde trabajar. En esta lección instalas lo necesario, corres tu primera prueba y aprendes a leer un error. Hazla con calma: todo el curso se apoya en lo que configures aquí.

**Tiempo estimado:** 45 minutos.

## Qué vas a lograr

- Tener Python y Git funcionando en tu computadora.
- Tener tu propia copia del curso, con un entorno virtual.
- Correr las pruebas y entender qué te dicen.
- Completar tu primer ejercicio.

## Paso 1. Instala Python

Necesitas Python 3.10 o más reciente.

| Sistema | Cómo instalarlo |
| --- | --- |
| Windows | Descarga el instalador desde [python.org/downloads](https://www.python.org/downloads/). En la primera pantalla marca la casilla **Add python.exe to PATH** antes de continuar. Al terminar, **cierra PowerShell y vuelve a abrirlo**: una terminal abierta antes de la instalación no reconoce el comando `python`. |
| macOS | Descarga el instalador desde [python.org/downloads](https://www.python.org/downloads/) y sigue los pasos. |
| Linux | Casi siempre ya viene instalado. Si no, en Ubuntu o Debian: `sudo apt install python3 python3-venv`. |

Abre una terminal para comprobarlo. En Windows busca **PowerShell**; en macOS y Linux, **Terminal**.

```bash
python --version
```

Debe aparecer algo como `Python 3.12.4`.

> En macOS y Linux, si el comando `python` no existe, usa `python3`. Solo lo necesitas así hasta el paso 4; después de activar el entorno virtual, `python` funciona en todos los sistemas.

> **Windows:** si al escribir `python` se abre la Microsoft Store en lugar de mostrarte la versión, Windows tiene un atajo que se interpone. Abre **Inicio**, escribe "alias de ejecución", entra en **Administrar alias de ejecución de aplicaciones** y apaga los interruptores de **python.exe** y **python3.exe**. Después abre una terminal nueva y vuelve a probar.

## Paso 2. Instala Git y un editor

- **Git** guarda el historial de tu trabajo y lo sube a GitHub. Descárgalo desde [git-scm.com](https://git-scm.com/downloads). Igual que con Python, cierra la terminal y ábrela de nuevo al terminar, y compruébalo con `git --version`.
- **Editor:** usa el que prefieras. Si no tienes uno, [Visual Studio Code](https://code.visualstudio.com/) es gratuito y funciona igual en los tres sistemas.

Antes de seguir, dile a Git quién eres. Cada cambio que guardes llevará este nombre y este correo. Es obligatorio: sin esto, Git se niega a guardar.

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
```

> Usa el mismo correo con el que creaste tu cuenta de GitHub. Si prefieres no mostrar tu correo personal, GitHub te da una dirección `noreply` en **Settings → Emails** que puedes usar aquí.

## Paso 3. Crea tu copia del curso

1. Entra al repositorio del curso en GitHub y presiona **Use this template** y luego **Create a new repository**.
2. Ponle un nombre, por ejemplo `mi-curso-python`, y créalo en tu cuenta.
3. Copia la dirección de **tu** repositorio y descárgalo:

```bash
git clone https://github.com/TU_USUARIO/mi-curso-python.git
cd mi-curso-python
```

Desde ahora, todos los comandos del curso se escriben dentro de esa carpeta.

## Paso 4. Crea y activa el entorno virtual

Un entorno virtual es una carpeta con una instalación de Python solo para este proyecto. Así, lo que instales aquí no se mezcla con otros proyectos de tu computadora.

Créalo una sola vez:

```bash
python -m venv .venv
```

**En Windows, una sola vez, antes de activar:** PowerShell bloquea por defecto la ejecución de scripts, y activar el entorno es correr un script. Este comando le da permiso para los scripts de tu usuario. Corre esto y responde `S` (o `Y`) cuando pregunte:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Actívalo **cada vez que abras una terminal nueva**:

| Sistema | Comando |
| --- | --- |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| macOS y Linux | `source .venv/bin/activate` |

Sabrás que está activo porque la línea de la terminal empieza con `(.venv)`.

## Paso 5. Instala las herramientas del curso

Con el entorno activo:

```bash
python -m pip install -r requirements.txt
```

Esto instala dos herramientas:

- **pytest**, que corre las pruebas con las que te vas a evaluar.
- **ruff**, que revisa el estilo de tu código.

## Paso 6. Corre las pruebas por primera vez

```bash
pytest lecciones/leccion_00_preparacion
```

Van a fallar, y eso es justo lo que esperamos: todavía no escribes nada. Verás algo parecido a esto:

```text
lecciones/leccion_00_preparacion/test_ejercicios.py FF                   [100%]

================================== FAILURES ===================================
_________________ test_ejercicio_1_saludar_devuelve_un_texto __________________
lecciones/leccion_00_preparacion/test_ejercicios.py:7: in test_ejercicio_1_saludar_devuelve_un_texto
    resultado = saludar()
lecciones/leccion_00_preparacion/ejercicios.py:21: in saludar
    raise NotImplementedError("Aún no completas la función saludar().")
E   NotImplementedError: Aún no completas la función saludar().
=========================== short test summary info ===========================
FAILED lecciones/leccion_00_preparacion/test_ejercicios.py::test_ejercicio_1_saludar_devuelve_un_texto
FAILED lecciones/leccion_00_preparacion/test_ejercicios.py::test_ejercicio_1_saludar_devuelve_el_texto_exacto
============================== 2 failed in 0.05s ==============================
```

### Cómo leer ese resultado

Un error no es un regaño: es información. Léelo siempre en este orden.

1. **La última línea.** `2 failed` te dice cuántas pruebas fallaron. Cuando termines dirá `2 passed`.
2. **Las letras de la primera línea.** Cada prueba deja una marca: `.` si pasó, `F` si falló, `E` si hubo un error antes de poder probar.
3. **La línea que empieza con `E`.** Es el motivo del fallo. Aquí dice que la función todavía no está completa.
4. **Las líneas con nombre de archivo y número.** `ejercicios.py:21` indica el archivo y el renglón exacto donde ocurrió el problema.

## Paso 7. Completa tu primer ejercicio

Abre `lecciones/leccion_00_preparacion/ejercicios.py`. Dentro está la función `saludar`.

1. Lee el texto entre comillas triples. Se llama *docstring* y explica qué debe hacer la función.
2. Borra la línea que empieza con `raise NotImplementedError`.
3. En su lugar, escribe una línea que devuelva el texto pedido. Recuerda que una función entrega su resultado con la palabra `return`.
4. Guarda el archivo y corre otra vez las pruebas.

Así se ve una función que devuelve un texto. La tuya tendrá la misma forma, con otro nombre y otro texto:

```python
def despedir():
    return "Hasta luego"
```

<details>
<summary>Pista, por si te atoras</summary>

La línea que necesitas empieza con `return` y termina con el texto entre comillas. Cuida que la sangría sea de cuatro espacios, igual que la línea que borraste.

</details>

Si algo no coincide, la prueba te lo dice con detalle. Por ejemplo, si olvidas la coma:

```text
E   AssertionError: Se esperaba 'Hola, datos' y se obtuvo 'Hola datos'. Revisa mayúsculas, la coma y los espacios.
```

Corrige y repite hasta ver `2 passed`.

## Paso 8. Mira tu avance y guarda tu trabajo

```bash
python progreso.py
```

Este comando resume cuántas pruebas llevas en cada lección. Úsalo cuando quieras saber dónde vas.

Para guardar tu trabajo y subirlo a GitHub:

```bash
git add .
git commit -m "Completa la lección 0"
git push
```

> La primera vez que hagas `git push`, Git te pedirá iniciar sesión en GitHub. Es normal: necesita comprobar que el repositorio es tuyo.
>
> - **Windows:** Git trae un administrador de credenciales que abre una ventana del navegador. Inicia sesión con tu cuenta y Git guardará el acceso.
> - **macOS, Linux, o si la terminal te pide usuario y contraseña:** el usuario es tu nombre de GitHub, pero la contraseña **no** es la de tu cuenta: GitHub ya no la acepta. Crea un token en GitHub, en **Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token**, marca el permiso **repo** y pégalo cuando te pida la contraseña (no se ve mientras lo pegas). Guárdalo en un lugar seguro: si tu sistema no lo recuerda, te lo volverá a pedir.

Hazlo al terminar cada lección. Cada vez que subes cambios, GitHub corre las mismas pruebas y deja el resultado en la pestaña **Actions** de tu repositorio.

## Antes de seguir

Responde de memoria, sin volver a leer. Intentar recordar es lo que fija lo aprendido.

1. ¿Para qué sirve un entorno virtual?
2. ¿Qué comando activa el entorno en tu sistema?
3. En el resultado de pytest, ¿qué línea te dice el motivo de un fallo?
4. ¿Qué diferencia hay entre `.`, `F` y `E`?

## Si algo no funciona

| Qué ves | Qué hacer |
| --- | --- |
| `python` no se reconoce como comando | Primero cierra la terminal y ábrela de nuevo. Si sigue igual, en Windows revisa los alias de la Microsoft Store (ver el aviso del paso 1) y, solo si nada de eso funciona, reinstala Python marcando **Add python.exe to PATH**. En macOS y Linux, prueba con `python3`. |
| `la ejecución de scripts está deshabilitada en este sistema` | Falta el permiso de PowerShell. Corre `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` como se explica en el paso 4 y vuelve a activar el entorno. |
| `pytest` no se reconoce como comando | El entorno virtual no está activo. Repite el paso 4. |
| `No module named pytest` | Faltó el paso 5, o lo corriste sin activar el entorno. |
| `ModuleNotFoundError: No module named 'lecciones'` | Estás en otra carpeta. Los comandos se corren desde la carpeta principal del curso. |

## Referencias

- Eric Matthes, *Python Crash Course*, 3.ª ed., capítulo 1 (instalación y primer programa) y capítulo 11 (instalar pytest y leer una prueba fallida).
- Brian Okken, *Python Testing with pytest*, capítulo 1 (cómo correr pytest y cómo leer su salida).
