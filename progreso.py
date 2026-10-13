"""Muestra tu avance en el curso.

Corre las pruebas de cada lección y del proyecto, y resume cuántas pasan.

Uso:
    python progreso.py            muestra la tabla de avance
    python progreso.py --json     además guarda el resultado en progreso.json
"""

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ANCHO_BARRA = 20


def buscar_unidades():
    """Devuelve las carpetas que se evalúan: cada lección y el proyecto."""
    unidades = sorted(
        carpeta
        for carpeta in (RAIZ / "lecciones").iterdir()
        if carpeta.is_dir() and carpeta.name.startswith("leccion_")
    )
    proyecto = RAIZ / "proyecto"
    if (proyecto / "tests").is_dir():
        unidades.append(proyecto)
    return unidades


def evaluar(carpeta):
    """Corre las pruebas de una carpeta y devuelve (aprobadas, total)."""
    with tempfile.TemporaryDirectory() as temporal:
        reporte = Path(temporal) / "reporte.xml"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(carpeta),
                "-q",
                f"--junitxml={reporte}",
            ],
            cwd=RAIZ,
            capture_output=True,
            check=False,
        )
        if not reporte.exists():
            return 0, 0
        raiz_xml = ET.parse(reporte).getroot()

    conjunto = raiz_xml if raiz_xml.tag == "testsuite" else raiz_xml.find("testsuite")
    total = int(conjunto.get("tests", 0))
    no_aprobadas = sum(
        int(conjunto.get(campo, 0)) for campo in ("failures", "errors", "skipped")
    )
    return total - no_aprobadas, total


def nombre_legible(carpeta):
    """Toma el nombre de la unidad del primer título de su README."""
    guia = carpeta / "README.md"
    if guia.exists():
        primera_linea = guia.read_text(encoding="utf-8").splitlines()[0]
        return primera_linea.lstrip("# ").strip()
    return carpeta.name


def dibujar_barra(aprobadas, total):
    llenos = round(ANCHO_BARRA * aprobadas / total) if total else 0
    return "#" * llenos + "." * (ANCHO_BARRA - llenos)


def main():
    # En algunas terminales de Windows los acentos fallan si no se indica UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    resultados = []
    print("\nTu avance en el curso\n")
    for carpeta in buscar_unidades():
        aprobadas, total = evaluar(carpeta)
        resultados.append(
            {"unidad": carpeta.name, "aprobadas": aprobadas, "total": total}
        )
        estado = "completa" if total and aprobadas == total else "en curso"
        print(
            f"  {nombre_legible(carpeta):<48} "
            f"[{dibujar_barra(aprobadas, total)}] {aprobadas:>3}/{total:<3} {estado}"
        )

    aprobadas = sum(fila["aprobadas"] for fila in resultados)
    total = sum(fila["total"] for fila in resultados)
    porcentaje = round(100 * aprobadas / total) if total else 0
    print(f"\n  Total: {aprobadas} de {total} pruebas ({porcentaje} %)\n")

    if "--json" in sys.argv:
        salida = {"aprobadas": aprobadas, "total": total, "unidades": resultados}
        (RAIZ / "progreso.json").write_text(
            json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("  Resultado guardado en progreso.json\n")


if __name__ == "__main__":
    main()
