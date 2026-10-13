"""Lección 1: ejemplos resueltos.

Corre este archivo y compara lo que imprime con el código:

    python lecciones/leccion_01_variables_y_texto/ejemplos.py

Después cambia valores y vuelve a correrlo. Experimentar aquí no afecta tus pruebas.
"""

# --- Variables: un nombre que apunta a un valor ---
producto = "Café de olla"
cantidad = 3
precio_unitario = 45.5

print("Producto:", producto)
print("Cantidad:", cantidad)
print("Precio unitario:", precio_unitario)

# --- Tipos: cada valor tiene uno ---
print(type(producto))  # str: texto
print(type(cantidad))  # int: número entero
print(type(precio_unitario))  # float: número con decimales

# --- Métodos de texto: devuelven un texto nuevo, no cambian el original ---
ciudad_cruda = "  ciudad de méxico  "
ciudad_limpia = ciudad_cruda.strip().title()

print(repr(ciudad_cruda))  # '  ciudad de méxico  '
print(repr(ciudad_limpia))  # 'Ciudad De México'

# --- f-strings: texto con valores dentro ---
mensaje = f"{cantidad} piezas de {producto}"
print(mensaje)

# --- De texto a número ---
precio_crudo = "$1,250.00"
precio_sin_simbolos = precio_crudo.replace("$", "").replace(",", "")
precio = float(precio_sin_simbolos)

print(precio)  # 1250.0
print(precio + 100)  # 1350.0

# --- Operaciones y redondeo ---
total = cantidad * precio_unitario
print(total)  # 136.5

tercio = 100 / 3
print(tercio)  # 33.333333333333336
print(round(tercio, 2))  # 33.33

# --- Formato para mostrar un importe ---
importe = 1250.5
print(f"${importe:,.2f}")  # $1,250.50
