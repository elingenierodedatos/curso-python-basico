"""El flujo completo: une las cuatro etapas."""

import csv  # noqa: F401
from pathlib import Path  # noqa: F401

from flujo_ventas import cargar, extraer, limpiar, reportar  # noqa: F401


def guardar_rechazados(ruta, rechazados):
    """Guarda los pedidos rechazados en un CSV y devuelve cuántos escribió.

    Columnas: "fila", "motivo" y después todas las de extraer.COLUMNAS, con los
    datos crudos tal como llegaron. Crea la carpeta si no existe. Si no hay
    rechazados, el archivo se crea solo con el encabezado.
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función guardar_rechazados().")


def ejecutar_flujo(ruta_csv, carpeta_salida):
    """Corre el flujo completo y devuelve el reporte.

    Pasos:
        1. Lee los pedidos crudos de ruta_csv.
        2. Los limpia y separa los rechazados.
        3. Abre la base carpeta_salida/ventas.db, crea la tabla y carga los
           pedidos limpios.
        4. Construye el reporte.
        5. Guarda carpeta_salida/reporte.json y carpeta_salida/rechazados.csv.
        6. Cierra la conexión, aunque algún paso falle, y devuelve el reporte.

    Correr el flujo dos veces seguidas debe dar el mismo resultado.
    """
    # Borra la línea de abajo y escribe tu código en su lugar.
    raise NotImplementedError("Aún no completas la función ejecutar_flujo().")
