"""Lección 7: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_07_pruebas/ejemplos.py

Aquí ves las piezas sueltas, sin pytest de por medio: qué hace `assert`,
qué hace `pytest.raises` y cómo una comprobación recibe la función que revisa.
Las pruebas completas, como las escribirías en un proyecto, están en
`ejemplos_de_pruebas.py`.
"""

import pytest

# --- Dos versiones de la misma función: una correcta y una con un defecto ---


def calcular_total(cantidad, precio_unitario):
    """Multiplica cantidad por precio unitario y redondea a dos decimales."""
    if cantidad < 0:
        raise ValueError(f"La cantidad no puede ser negativa: {cantidad}")
    return round(cantidad * precio_unitario, 2)


def calcular_total_sin_redondeo(cantidad, precio_unitario):
    """Igual que la anterior, pero alguien olvidó el redondeo."""
    if cantidad < 0:
        raise ValueError(f"La cantidad no puede ser negativa: {cantidad}")
    return cantidad * precio_unitario


# --- assert: si la condición es verdadera, no pasa nada ---
assert calcular_total(2, 50.0) == 100.0
print("El primer assert pasó sin decir nada.")

# --- assert: si la condición es falsa, lanza AssertionError ---
# pytest atrapa ese error por ti y lo muestra con detalle. Aquí lo atrapamos
# a mano solo para que el archivo siga corriendo.
try:
    assert calcular_total_sin_redondeo(3, 0.1) == 0.3
except AssertionError:
    print("El segundo assert falló:", calcular_total_sin_redondeo(3, 0.1), "no es 0.3")

# --- pytest.raises: comprobar que una función lanza el error esperado ---
with pytest.raises(ValueError):
    calcular_total(-1, 50.0)
print("calcular_total(-1, 50.0) lanzó ValueError, como debía.")

# Con `match` se revisa además una parte del mensaje del error.
with pytest.raises(ValueError, match="no puede ser negativa"):
    calcular_total(-1, 50.0)
print("Y el mensaje del error contiene 'no puede ser negativa'.")

# --- Una función es un valor: se puede guardar y pasar como argumento ---
funcion_elegida = calcular_total  # sin paréntesis: no se llama, solo se nombra
print(funcion_elegida(2, 19.99))  # 39.98


# --- Una comprobación: recibe la función que revisa ---
def comprobar_calcular_total(funcion):
    """Revisa con assert la función recibida. Si todo va bien, no devuelve nada."""
    assert funcion(2, 50.0) == 100.0
    assert funcion(3, 0.1) == 0.3
    assert funcion(0, 99.9) == 0.0


comprobar_calcular_total(calcular_total)
print("La comprobación pasó con la función correcta.")

try:
    comprobar_calcular_total(calcular_total_sin_redondeo)
except AssertionError:
    print("La comprobación atrapó a la función sin redondeo.")


# --- Una comprobación débil deja pasar el defecto ---
def comprobacion_debil(funcion):
    """Solo revisa un caso fácil, donde el redondeo no importa."""
    assert funcion(2, 50.0) == 100.0


comprobacion_debil(calcular_total_sin_redondeo)
print("La comprobación débil no notó nada: el defecto se le escapó.")

# --- Casos listos para parametrizar: una lista de tuplas (entrada, esperado) ---
casos = [
    (2, 50.0, 100.0),
    (3, 0.1, 0.3),
    (0, 99.9, 0.0),
]
for cantidad, precio_unitario, esperado in casos:
    assert calcular_total(cantidad, precio_unitario) == esperado
print("Los", len(casos), "casos pasaron.")
