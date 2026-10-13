"""Datos y recursos compartidos por las pruebas. No modifiques este archivo."""

import csv
import sqlite3
from pathlib import Path

import pytest

COLUMNAS = [
    "id_pedido",
    "fecha",
    "cliente",
    "ciudad",
    "producto",
    "cantidad",
    "precio_unitario",
    "estado",
]

RUTA_DATOS = Path(__file__).resolve().parent.parent / "datos" / "pedidos_crudos.csv"


def crear_crudo(**cambios):
    """Devuelve un pedido crudo válido; los cambios sustituyen columnas."""
    crudo = {
        "id_pedido": "1001",
        "fecha": "2025-03-07",
        "cliente": "Ana Ruiz",
        "ciudad": "Puebla",
        "producto": "Café de olla",
        "cantidad": "2",
        "precio_unitario": "185.00",
        "estado": "entregado",
    }
    crudo.update(cambios)
    return crudo


def crear_limpio(id_pedido, ciudad, producto, cantidad, precio_unitario, estado):
    """Devuelve un pedido limpio, como los que produce la etapa de limpieza."""
    return {
        "id_pedido": id_pedido,
        "fecha": "2025-03-07",
        "cliente": "Ana Ruiz",
        "ciudad": ciudad,
        "producto": producto,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "estado": estado,
        "total": round(cantidad * precio_unitario, 2),
    }


def escribir_csv(ruta, filas, columnas=None):
    """Escribe un CSV de apoyo para las pruebas."""
    columnas = columnas or COLUMNAS
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)
    return ruta


@pytest.fixture
def conexion():
    """Base de datos en memoria, nueva para cada prueba."""
    conexion = sqlite3.connect(":memory:")
    yield conexion
    conexion.close()


@pytest.fixture
def pedidos_limpios():
    """Cinco pedidos limpios con totales fáciles de sumar a mano.

    Ventas (sin el cancelado): Puebla 370.00 + 645.00 = 1015.00,
    Mérida 2501.00, Tijuana 120.00. Total 3636.00.
    """
    return [
        crear_limpio(1, "Puebla", "Café de olla", 2, 185.0, "entregado"),
        crear_limpio(2, "Mérida", "Molinillo manual", 2, 1250.5, "enviado"),
        crear_limpio(3, "Puebla", "Prensa francesa", 1, 645.0, "entregado"),
        crear_limpio(4, "Mérida", "Café de olla", 10, 185.0, "cancelado"),
        crear_limpio(5, "Tijuana", "Taza de barro", 1, 120.0, "desconocido"),
    ]


@pytest.fixture
def csv_pequeno(tmp_path):
    """CSV de seis filas: tres válidas, dos rechazadas y una duplicada."""
    filas = [
        crear_crudo(id_pedido="1", ciudad=" cdmx ", precio_unitario="$1,250.50"),
        crear_crudo(id_pedido="2", ciudad="N/D"),
        crear_crudo(id_pedido="3", fecha="7/3/2025", estado="Cancelada"),
        crear_crudo(id_pedido="1", ciudad="Puebla"),
        crear_crudo(id_pedido="4", cantidad="cero"),
        crear_crudo(id_pedido="5", ciudad="mérida", producto="TAZA DE BARRO"),
    ]
    carpeta = tmp_path / "entrada"
    carpeta.mkdir()
    return escribir_csv(carpeta / "pedidos.csv", filas)
