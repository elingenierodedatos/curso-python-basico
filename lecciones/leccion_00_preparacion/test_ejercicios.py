"""Pruebas de la lección 0. No modifiques este archivo."""

from lecciones.leccion_00_preparacion.ejercicios import saludar


def test_ejercicio_1_saludar_devuelve_un_texto():
    resultado = saludar()

    assert isinstance(resultado, str), (
        "saludar() debe devolver un texto (str). "
        f"Devolvió {resultado!r}, que es de tipo {type(resultado).__name__}. "
        "¿Usaste print() en lugar de return?"
    )


def test_ejercicio_1_saludar_devuelve_el_texto_exacto():
    resultado = saludar()

    assert resultado == "Hola, datos", (
        f"Se esperaba 'Hola, datos' y se obtuvo {resultado!r}. "
        "Revisa mayúsculas, la coma y los espacios."
    )
