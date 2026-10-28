"""Este es mi código y este es el error: [pega el código] [pega el Traceback]. Explícame por qué falla. Luego corrígelo, muestra el tipo de dato antes y después de convertir con type(), acepta coma decimal y muestra el precio final con el descuento. Comenta el código línea por línea."""
# Descuento de un servicio - versión corregida y mejorada con IA
DESCUENTO = 0.10   # constante: 10% de descuento
 
texto = input("Precio del servicio (Bs): ")   # pide el precio (llega como texto)
print("Tipo recibido  :", type(texto))        # muestra el tipo: str (texto)
precio = float(texto.replace(",", "."))       # convierte el texto a número decimal
print("Tipo convertido:", type(precio))       # muestra el tipo: float (decimal)
descuento = precio * DESCUENTO                # ahora sí se puede multiplicar
final = precio - descuento                    # calcula el precio final
print(f"Descuento: Bs {descuento:,.2f}")      # muestra el descuento
print(f"A pagar  : Bs {final:,.2f}")          # muestra el precio final
