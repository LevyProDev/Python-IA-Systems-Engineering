"""Este es mi código y este es el error: [pega el código] [pega el Traceback]. Explícame la diferencia entre TypeError y ValueError. Luego corrígelo SIN usar try/except todavía: valida el texto antes de convertir, acepta decimales con punto o coma y muestra un mensaje amigable. Comenta el código línea por línea."""
# Pago por horas - versión corregida y mejorada con IA
TARIFA = 40   # Bs por hora
 
texto = input("Horas trabajadas: ").strip().replace(",", ".")   # limpia y acepta coma
if texto.replace(".", "", 1).isdigit():   # quita 1 punto y revisa que sean solo dígitos
    horas = float(texto)                  # si es válido, lo convierte a decimal
    pago = horas * TARIFA                 # calcula el pago
    print(f"Pago: Bs {pago:,.2f}")        # muestra el pago con 2 decimales
else:                                     # si no son solo números...
    print("Escribe solo números, por ejemplo 3.5")   # mensaje amigable
