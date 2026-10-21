# Instalar desde la terminal: Windows, macOS y Linux

La [lección 0](../lecciones/leccion_00_preparacion/README.md) instala todo con los instaladores gráficos y con eso basta para el curso. Esta guía es para quien prefiere hacerlo desde la terminal, como se ve en el video de la lección 0, o para quien quiere manejar varias versiones de Python. El resultado es el mismo: al terminar vuelves al paso 3 de la lección 0.

Todo lo que hay aquí se corre en una terminal **normal**, sin permisos de administrador. Si un paso necesita administrador, lo dice.

## 1. La terminal

| Sistema | Qué abrir |
| --- | --- |
| Windows | **PowerShell**. Busca "PowerShell" en Inicio. El azul (Windows PowerShell 5.1) sirve para todo el curso. Si quieres la versión moderna, instala PowerShell 7 y Windows Terminal: `winget install -e --id Microsoft.PowerShell` y `winget install -e --id Microsoft.WindowsTerminal`. No uses el **Símbolo del sistema (cmd)**: los comandos de activación del entorno cambian. |
| macOS | **Terminal**. Cmd + Espacio, escribe "Terminal". |
| Linux | **Terminal**. Casi siempre Ctrl + Alt + T. |

> **Windows:** `winget` es el instalador de paquetes que ya viene en Windows 10 y 11. Si un comando responde `No package found`, busca el nombre con `winget search nombre`.

## 2. Git

| Sistema | Comando |
| --- | --- |
| Windows | `winget install -e --id Git.Git` |
| macOS | `xcode-select --install` (lo trae Apple) o, si tienes [Homebrew](https://brew.sh): `brew install git` |
| Linux (Ubuntu, Debian) | `sudo apt install git` |

Cierra la terminal, ábrela de nuevo y comprueba:

```bash
git --version
```

### Configuración de Git

Las dos primeras líneas son obligatorias: sin nombre y correo, Git se niega a guardar. Las otras dos son recomendadas y te ahorran preguntas más adelante.

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
```

- Usa el mismo correo de tu cuenta de GitHub. Si no quieres mostrar tu correo personal en un repositorio público, GitHub te da una dirección `noreply` en **Settings → Emails**.
- No necesitas llaves SSH para este curso: clonar por HTTPS es suficiente. Si ya las usas, no cambies nada.
- Los saltos de línea ya los controla el archivo `.gitattributes` del curso, así que no hace falta configurar `core.autocrlf`.

## 3. Python

Necesitas Python 3.10 o más reciente. Elige **una** de las tres opciones.

> **Windows, antes de instalar Python por cualquier opción:** apaga los alias de la Microsoft Store. Abre **Inicio**, escribe "alias de ejecución", entra en **Administrar alias de ejecución de aplicaciones** y apaga **python.exe** y **python3.exe**. Si no lo haces, al escribir `python` se abre la tienda en lugar de Python.

**Opción A. Instalador oficial.** Es la de la lección 0: [python.org/downloads](https://www.python.org/downloads/). En Windows marca **Add python.exe to PATH**.

**Opción B. Desde la terminal.**

| Sistema | Comando |
| --- | --- |
| Windows | `winget install -e --id Python.Python.3.12` |
| macOS | `brew install python` (instala la versión estable más reciente y crea el comando `python3`) |
| Linux (Ubuntu, Debian) | `sudo apt install python3 python3-venv` (Ubuntu 24.04 trae 3.12) |

**Opción C. Con `uv`, un gestor de versiones.** Es lo que uso en el video. Sirve cuando un proyecto pide Python 3.12 y otro 3.13: instalas las versiones que quieras y eliges cuál es la predeterminada. No hace falta aprender `uv` para el curso; el resto de los comandos no cambian.

| Sistema | Instalar uv |
| --- | --- |
| Windows | `winget install -e --id astral-sh.uv` |
| macOS y Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` (o `brew install uv`) |

Cierra la terminal, ábrela de nuevo y después:

```bash
uv python install 3.12 --default
uv tool update-shell
```

Cierra la terminal otra vez para que tome el cambio. `uv python list` te muestra las versiones instaladas.

> Si `uv` responde que `--default` es una función en vista previa y pide `--preview`, repite el comando así: `uv python install 3.12 --default --preview`.

Comprueba:

```bash
python --version
```

En macOS y Linux, si `python` no existe, usa `python3`. La versión que aparezca debe ser **3.10 o mayor**. Si en macOS ves `Python 3.9`, es el Python que trae Apple: instala con la opción A o con `brew install python`, abre una terminal nueva y vuelve a comprobar. Después de activar el entorno virtual (paso 4 de la lección 0), `python` funciona en todos los sistemas.

## 4. Visual Studio Code

| Sistema | Comando |
| --- | --- |
| Windows | `winget install -e --id Microsoft.VisualStudioCode` |
| macOS | `brew install --cask visual-studio-code` o el instalador de [code.visualstudio.com](https://code.visualstudio.com/) |
| Linux | `sudo snap install code --classic` o el paquete `.deb` / `.rpm` de [code.visualstudio.com](https://code.visualstudio.com/) |

> **macOS sin Homebrew:** el instalador de la página no agrega el comando `code` a la terminal. Abre VS Code, presiona Cmd + Shift + P, escribe `Shell Command: Install 'code' command in PATH`, confirma y abre una terminal nueva.

Extensiones que usamos en el curso. La primera es la que importa; la segunda revisa el estilo de tu código con las mismas reglas que `ruff check .`:

```bash
code --install-extension ms-python.python
code --install-extension charliermarsh.ruff
```

Cuando abras la carpeta del curso, VS Code también te las va a sugerir solo: el curso trae un archivo `.vscode/extensions.json` con esa lista.

Dos ajustes que ayudan:

- **Elige el intérprete del entorno virtual.** Ctrl + Shift + P (Cmd + Shift + P en macOS), escribe `Python: Select Interpreter` y elige el que diga `.venv`. Así la terminal integrada y las pruebas usan el mismo Python que el curso.
- **Abre la carpeta, no un archivo.** File → Open Folder → la carpeta del curso. Si abres solo `ejercicios.py`, las pruebas no encuentran las lecciones.

Si te aparece una sugerencia de código de alguna inteligencia artificial (Copilot u otra), desactívala durante el curso. [Aquí explicamos por qué](por-que-sin-ia.md).

## 5. Comprobación final

Las tres líneas deben responder con una versión. En macOS y Linux, si `python` no existe, prueba `python3 --version`: también es válido.

```bash
git --version
python --version
code --version
```

Listo. Vuelve al [paso 3 de la lección 0](../lecciones/leccion_00_preparacion/README.md#paso-3-crea-tu-copia-del-curso) para crear tu copia del curso.

## Si algo no funciona

| Qué ves | Qué hacer |
| --- | --- |
| `winget` responde `No package found` | Busca el nombre exacto con `winget search nombre`. Si no existe, usa el instalador de la página oficial. |
| Instalaste algo y la terminal sigue sin reconocer el comando | Cierra **todas** las ventanas de la terminal y abre una nueva. En Windows, si sigue igual, cierra sesión y vuelve a entrar: la terminal hereda el PATH del Explorador y a veces no se actualiza. |
| `python` abre la Microsoft Store | Apaga los alias de la Store (aviso del punto 3) y abre una terminal nueva. |
| La terminal abre en `C:\WINDOWS\system32` | No estás en tu carpeta de usuario. Escribe `cd $HOME` antes de seguir. Para que siempre abra ahí: Windows Terminal → Configuración → Perfiles → Valores predeterminados → Directorio de inicio = `%USERPROFILE%`. |
| Estás en el Símbolo del sistema (cmd) y `Activate.ps1` no funciona | Cambia a PowerShell. Si prefieres quedarte en cmd, el comando de activación es `.venv\Scripts\activate.bat`. |
| macOS: `code: command not found` | Instalaste VS Code sin Homebrew. Sigue el aviso del punto 4 para agregar `code` a la terminal. |
| macOS: `brew: command not found` | Instala Homebrew desde [brew.sh](https://brew.sh) o usa los instaladores oficiales. |
| macOS: `xcrun: error: invalid active developer path` | Faltan las herramientas de Apple. Corre `xcode-select --install`. |
| Linux: `ensurepip is not available` al crear el entorno | Falta el paquete del entorno virtual: `sudo apt install python3-venv`. |
