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
from pathlib import Path, PurePosixPath

RAIZ = Path(__file__).resolve().parent
REMOTO = "curso"
URL = "https://github.com/elingenierodedatos/curso-python-basico.git"
RAMA = "main"
REFERENCIA = f"{REMOTO}/{RAMA}"

# Archivos que escribes tú. Si ya existen en tu copia, nunca se reemplazan.
# Si el curso agrega uno nuevo (por ejemplo, una lección nueva), se copia.
#
# Regla para quien mantiene el curso: no agregues ni renombres funciones en un
# archivo de esta lista que ya esté publicado. La copia del alumno no recibe ese
# cambio y las pruebas nuevas no podrían importar la función. Los ejercicios
# nuevos van en lecciones nuevas.
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


def detener(mensaje, resultado=None):
    if resultado is not None and resultado.stderr.strip():
        mensaje += f"\n  Detalle: {resultado.stderr.strip()}"
    print(f"\n  {mensaje}\n")
    sys.exit(1)


def pruebas_de(ruta):
    """Devuelve la carpeta cuyas pruebas dependen de un archivo tuyo."""
    if ruta.startswith("proyecto/"):
        return "proyecto/tests/"
    return str(PurePosixPath(ruta).parent) + "/test_"


def distinto_al_curso(ruta):
    """Indica si tu copia de un archivo difiere de la versión del curso."""
    if not (RAIZ / ruta).is_file():
        return False
    tuyo = git("hash-object", "--", ruta).stdout.strip()
    del_curso = git("rev-parse", f"{REFERENCIA}:{ruta}").stdout.strip()
    return tuyo != del_curso


def conectar_remoto():
    """Crea el remoto del curso, o corrige su dirección si apunta a otro lado."""
    if REMOTO not in git("remote").stdout.split():
        git("remote", "add", "-t", RAMA, REMOTO, URL)
        print(f"\n  Conecté tu copia con el repositorio del curso ({REMOTO}).")
    elif git("remote", "get-url", REMOTO).stdout.strip() != URL:
        git("remote", "set-url", REMOTO, URL)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        detener("Corre este comando desde la carpeta principal de tu copia del curso.")

    conectar_remoto()

    descarga = git("fetch", REMOTO, f"+refs/heads/{RAMA}:refs/remotes/{REFERENCIA}")
    if descarga.returncode != 0:
        detener(
            "No pude descargar las novedades del curso. Revisa tu conexión a internet.",
            descarga,
        )

    listado = git("ls-tree", "-r", "--name-only", REFERENCIA)
    archivos = listado.stdout.splitlines()
    if listado.returncode != 0 or not archivos:
        detener(f"No encontré los archivos del curso en {REFERENCIA}.", listado)

    actualizar = []
    respetados = []
    for ruta in archivos:
        if es_tuyo(ruta) and (RAIZ / ruta).exists():
            respetados.append(ruta)
        else:
            actualizar.append(ruta)

    # Cambios sin guardar en archivos del curso: se perderían al actualizar.
    # Los que ya son iguales a la versión del curso (por ejemplo, si corres el
    # script dos veces antes de hacer commit) no cuentan.
    sin_guardar = [
        ruta
        for ruta in (
            linea[3:].split(" -> ")[-1].strip('"')
            for linea in git(
                "status", "--porcelain", "--", *actualizar
            ).stdout.splitlines()
        )
        if distinto_al_curso(ruta)
    ]
    if sin_guardar and "--forzar" not in sys.argv:
        lista = "\n    ".join(sin_guardar)
        detener(
            "Tienes cambios sin guardar en archivos del curso que se van a "
            f"reemplazar:\n    {lista}\n\n  Guárdalos con git commit, o corre "
            "`python actualizar.py --forzar` para descartarlos."
        )

    copia = git("checkout", REFERENCIA, "--", *actualizar)
    if copia.returncode != 0:
        detener(
            "No pude copiar los archivos del curso. Si tienes VS Code u otro "
            "programa usando Git, ciérralo y vuelve a intentar.",
            copia,
        )

    cambiados = git(
        "diff", "--cached", "--name-only", "--", *actualizar
    ).stdout.splitlines()

    if not cambiados:
        print("\n  Ya tenías todo al día. No hay nada que guardar.\n")
        return

    print(f"\n  Se actualizaron {len(cambiados)} archivos del curso:")
    for ruta in cambiados:
        print(f"    {ruta}")
    print(f"\n  Tus archivos no se tocaron ({len(respetados)}).")

    # Si cambiaron las pruebas de un archivo tuyo, revisa que siga al día.
    revisar = [
        ruta
        for ruta in respetados
        if any(cambio.startswith(pruebas_de(ruta)) for cambio in cambiados)
        and git("diff", "--quiet", REFERENCIA, "--", ruta).returncode != 0
    ]
    if revisar:
        print(
            "\n  Cambiaron las pruebas de estos archivos tuyos, y la versión del "
            "curso es distinta a la tuya:"
        )
        for ruta in revisar:
            print(f"    {ruta}")
        print(
            "  Corre sus pruebas. Si alguna falla porque falta una función, "
            "mira la versión del curso con:"
        )
        print(f"    git show {REFERENCIA}:RUTA_DEL_ARCHIVO")

    if any(ruta.startswith(".github/workflows/") for ruta in cambiados):
        print(
            "\n  Esta actualización cambia las pruebas automáticas de GitHub "
            "(.github/workflows). Si `git push` responde que falta el permiso "
            "`workflow`, crea un token con los permisos repo y workflow, como "
            "en la lección 0."
        )

    print("\n  Para terminar:")
    print("    python -m pip install -r requirements.txt")
    print('    git commit -m "Actualiza el material del curso"')
    print("    git push\n")


if __name__ == "__main__":
    main()
