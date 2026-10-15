"""Lección 7, ejercicio 6: tu propio archivo de pruebas.

Este archivo es tuyo. Aquí escribes pruebas de verdad para las funciones de
`funciones.py`, siguiendo la guía del README de esta carpeta.

Para aprobar el ejercicio 6 necesitas:

- Al menos tres funciones cuyo nombre empiece con `test_`.
- Que cada una compruebe algo, con `assert` o con `pytest.raises`
  (un `assert True` no cuenta).
- Que al menos una esté parametrizada con `@pytest.mark.parametrize`.
- Que entre todas usen al menos tres de las cuatro funciones importadas.
- Que todas pasen con el `funciones.py` de la lección.
- Que detecten defectos: también las corremos con copias de `funciones.py`
  donde una función está mal, y con cada función que uses al menos una de
  esas copias debe hacer fallar alguna prueba tuya.

Para correr solo tus pruebas:

    pytest lecciones/leccion_07_pruebas/test_mis_pruebas.py
"""

# La línea siguiente le pide a ruff que no avise de los imports sin usar
# mientras el archivo está vacío. Bórrala cuando termines tus pruebas.
# ruff: noqa: F401

import pytest

from lecciones.leccion_07_pruebas.funciones import (
    clasificar_importe,
    contar_por_ciudad,
    limpiar_precio,
    validar_cantidad,
)

# Escribe tus pruebas debajo de esta línea.
