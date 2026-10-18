"""Este es mi código en Python 3.13 y este es el error: [pega el código] [pega el SyntaxError]. Explícame qué significa, en qué línea está el problema y por qué ocurre. Luego corrígelo, agrega un segundo nivel de aprobación para montos mayores a 5000 y usa constantes para los límites. Comenta el código línea por línea."""
# Aprobación de gastos - versión corregida y mejorada con IA
LIMITE_GERENTE = 1000     # hasta este monto el gasto se aprueba solo
LIMITE_DIRECCION = 5000   # sobre este monto decide la dirección
 
monto = float(input("Monto del gasto (Bs): "))   # pide el monto y lo convierte a número
if monto > LIMITE_DIRECCION:                     # si supera 5000 (ahora lleva ":" al final)
    print(f"Bs {monto:,.2f}: requiere aprobación de la dirección")   # nivel más alto
elif monto > LIMITE_GERENTE:                     # si no, y supera 1000...
    print(f"Bs {monto:,.2f}: requiere aprobación del gerente")       # nivel intermedio
else:                                            # en cualquier otro caso...
    print(f"Bs {monto:,.2f}: gasto aprobado")                        # se aprueba solo
