"""Lección 6: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_06_archivos_y_errores/ejemplos.py

Después cambia valores y vuelve a correrlo. Experimentar aquí no afecta tus pruebas.
Este archivo solo lee datos/pedidos_ejemplo.csv; todo lo que escribe va a una
carpeta temporal que se borra al terminar.
"""

import csv
import json
import tempfile
from pathlib import Path

# --- Rutas: se arman con Path y el operador / ---
carpeta_leccion = Path(__file__).parent
ruta_pedidos = carpeta_leccion / "datos" / "pedidos_ejemplo.csv"

print(ruta_pedidos.name)  # pedidos_ejemplo.csv
print(ruta_pedidos.parent.name)  # datos
print(ruta_pedidos.exists())  # True

# --- Leer un archivo de texto completo ---
texto = ruta_pedidos.read_text(encoding="utf-8")
lineas = texto.splitlines()

print(len(lineas))  # 10: el encabezado y 9 pedidos
print(lineas[0])
print(lineas[1])

# split() parte un texto en una lista, usando el separador que le indiques.
print(lineas[1].split(","))

# --- Por qué siempre encoding="utf-8" ---
# Así se ve el mismo archivo si se lee con otra codificación.
texto_danado = ruta_pedidos.read_text(encoding="cp1252")
print(texto_danado.splitlines()[1])  # 1001,2024-03-01,Ana LÃ³pez,MÃ©rida,...

# --- Excepciones: atrapar solo el error esperado ---
ruta_inexistente = carpeta_leccion / "datos" / "no_existe.csv"

try:
    ruta_inexistente.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"No se encontró el archivo: {ruta_inexistente.name}")

for cantidad_cruda in ["3", "dos", "N/D"]:
    try:
        cantidad = int(cantidad_cruda)
    except ValueError:
        print(f"'{cantidad_cruda}' no es un número entero")
    else:
        print(f"'{cantidad_cruda}' se convirtió en el número {cantidad}")

# --- raise: rechazar un dato inválido con un mensaje claro ---
precio = -45.5

try:
    if precio < 0:
        raise ValueError(f"El precio no puede ser negativo: {precio}")
except ValueError as error:
    print("Dato rechazado:", error)

# --- CSV: cada fila llega como un diccionario de textos ---
pedidos = []
with ruta_pedidos.open(encoding="utf-8", newline="") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        pedidos.append(fila)

print(len(pedidos))  # 9
print(pedidos[0])
print(pedidos[1]["precio_unitario"])  # $1,250.50: la coma no partió la columna

# Sumar las cantidades sin callar los errores: lo que no se puede convertir
# se cuenta y se informa.
total_piezas = 0
filas_rechazadas = []
for pedido in pedidos:
    try:
        cantidad = int(pedido["cantidad"])
    except ValueError:
        filas_rechazadas.append(pedido["id_pedido"])
    else:
        total_piezas += cantidad

print("Piezas:", total_piezas)  # 18
print("Pedidos con cantidad inválida:", filas_rechazadas)  # ['1005', '1007']

# --- Escribir CSV y JSON, en una carpeta temporal ---
with tempfile.TemporaryDirectory() as temporal:
    carpeta_salida = Path(temporal) / "salida" / "marzo"
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    # CSV: una tabla, todas las filas con las mismas columnas.
    ruta_csv = carpeta_salida / "pedidos_merida.csv"
    columnas = ["id_pedido", "cliente", "ciudad"]
    with ruta_csv.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerow(
            {"id_pedido": "1001", "cliente": "Ana López", "ciudad": "Mérida"}
        )
        escritor.writerow(
            {"id_pedido": "1007", "cliente": "Ana López", "ciudad": "Mérida"}
        )

    print(ruta_csv.read_text(encoding="utf-8"))

    # JSON: una estructura anidada, como el resumen de un reporte.
    resumen = {
        "archivo": ruta_pedidos.name,
        "pedidos": len(pedidos),
        "piezas": total_piezas,
        "rechazados": filas_rechazadas,
        "ciudad_principal": "Mérida",
    }
    ruta_json = carpeta_salida / "resumen.json"
    ruta_json.write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    texto_json = ruta_json.read_text(encoding="utf-8")
    print(texto_json)

    resumen_leido = json.loads(texto_json)
    print(resumen_leido["rechazados"])  # ['1005', '1007']
    print(resumen_leido == resumen)  # True

# Al salir del bloque with, la carpeta temporal ya no existe.
print(Path(temporal).exists())  # False
