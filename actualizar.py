"""Trae las novedades del curso a tu copia sin tocar tu trabajo.

Tu copia se creó con "Use this template", así que no comparte historial con el
repositorio del curso y `git pull` no trae las novedades. Este script copia los
archivos del curso (guías, ejemplos, pruebas, datos y configuración) y respeta
los que escribes tú.

Uso, desde la carpeta principal del curso:
    python actualizar.py

Después revisa los cambios y guárdalos con `git commit` y `git push`.
"""

import fnmatch
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
REMOTO = "curso"
URL = "https://github.com/elingenierodedatos/curso-python-basico.git"
RAMA = "main"

# Archivos que escribes tú. Si ya existen en tu copia, nunca se reemplazan.
# Si el curso agrega uno nuevo (por ejemplo, una lección nueva), se copia.
TUYOS = [
    "lecciones/*/ejercicios.py",
    "lecciones/leccion_05_funciones_y_modulos/limpieza.py",
    "lecciones/leccion_07_pruebas/test_mis_pruebas.py",
    "proyecto/flujo_ventas/*.py",
]


def git(*argumentos):
    """Corre un comando de git en la carpeta del curso y devuelve el resultado."""
    return subprocess.run(
        ["git", *argumentos],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def es_tuyo(ruta):
    return any(fnmatch.fnmatch(ruta, patron) for patron in TUYOS)


def detener(mensaje):
    print(f"\n  {mensaje}\n")
    sys.exit(1)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        detener("Corre este comando desde la carpeta principal de tu copia del curso.")

    if REMOTO not in git("remote").stdout.split():
        git("remote", "add", "-t", RAMA, REMOTO, URL)
        print(f"\n  Conecté tu copia con el repositorio del curso ({REMOTO}).")

    descarga = git("fetch", REMOTO, RAMA)
    if descarga.returncode != 0:
        detener(
            "No pude descargar las novedades del curso. Revisa tu conexión a "
            f"internet.\n  Detalle: {descarga.stderr.strip()}"
        )

    referencia = f"{REMOTO}/{RAMA}"
    archivos = git("ls-tree", "-r", "--name-only", referencia).stdout.splitlines()

    actualizar = []
    respetados = []
    for ruta in archivos:
        if es_tuyo(ruta) and (RAIZ / ruta).exists():
            respetados.append(ruta)
        else:
            actualizar.append(ruta)

    # Cambios sin guardar en archivos del curso: se perderían al actualizar.
    sin_guardar = git("status", "--porcelain", "--", *actualizar).stdout.splitlines()
    if sin_guardar and "--forzar" not in sys.argv:
        lista = "\n    ".join(linea[3:] for linea in sin_guardar)
        detener(
            "Tienes cambios sin guardar en archivos del curso que se van a "
            f"reemplazar:\n    {lista}\n\n  Guárdalos con git commit, o corre "
            "`python actualizar.py --forzar` para descartarlos."
        )

    git("checkout", referencia, "--", *actualizar)
    cambiados = git("diff", "--cached", "--name-only").stdout.splitlines()

    if not cambiados:
        print("\n  Ya tenías todo al día. No hay nada que guardar.\n")
        return

    print(f"\n  Se actualizaron {len(cambiados)} archivos del curso:")
    for ruta in cambiados:
        print(f"    {ruta}")
    print(f"\n  Tus archivos no se tocaron ({len(respetados)}).")
    print("\n  Para terminar:")
    print("    python -m pip install -r requirements.txt")
    print('    git commit -m "Actualiza el material del curso"')
    print("    git push\n")


if __name__ == "__main__":
    main()
