"""Corre el flujo de ventas con los datos del proyecto.

Uso, desde la carpeta principal del curso:

    python proyecto/ejecutar.py

Deja los resultados en proyecto/salida/.
"""

import sys
from pathlib import Path

from flujo_ventas import principal

CARPETA = Path(__file__).resolve().parent


def main():
    # En algunas terminales de Windows los acentos fallan si no se indica UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    reporte = principal.ejecutar_flujo(
        CARPETA / "datos" / "pedidos_crudos.csv", CARPETA / "salida"
    )

    print("\nFlujo de ventas terminado\n")
    print(f"  Pedidos cargados:   {reporte['pedidos_cargados']}")
    print(f"  Pedidos rechazados: {reporte['pedidos_rechazados']}")
    print(f"  Ventas totales:     ${reporte['ventas_totales']:,.2f} MXN\n")
    print("  Ventas por ciudad")
    for fila in reporte["ventas_por_ciudad"]:
        print(f"    {fila['ciudad']:<20} ${fila['total']:>12,.2f}")
    print(f"\n  Resultados en: {CARPETA / 'salida'}\n")


if __name__ == "__main__":
    main()
