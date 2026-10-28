"""Mejora este programa para que no se cierre si el usuario escribe texto en vez de un número: usa try/except capturando solo ValueError, muestra un mensaje amigable y deja que el programa llegue hasta el final. Usa una constante para el IVA y comenta el código línea por línea."""
# Cálculo de IVA a prueba de errores - versión mejorada con IA
TASA_IVA = 0.13   # constante: tasa de IVA
 
try:                                                  # intenta ejecutar este bloque
    monto = float(input("Monto (Bs): "))              # pide el monto (puede fallar)
    iva = monto * TASA_IVA                            # calcula el IVA
    print(f"IVA: Bs {iva:,.2f}")                      # muestra el IVA
except ValueError:                                    # si el texto no era un número...
    print("Error: escribe solo números, por ejemplo 1500")   # mensaje amigable
print("Fin del programa")                             # se ejecuta SIEMPRE: no se cerró
