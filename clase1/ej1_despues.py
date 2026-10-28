"""
Mejora este código para un contador: usa constantes para el IVA y la moneda, crea una función que calcule el IVA y devuelva el total, acepta coma decimal, muestra los montos con 2 decimales y un resumen ordenado. Comenta el código línea por línea.
"""
# Calculadora de IVA - versión mejorada con IA
TASA_IVA = 0.13   # constante: tasa de IVA (se cambia en un solo lugar)
MONEDA = "Bs"     # constante: moneda que se muestra
 
 
def calcular_iva(monto):   # función: recibe el monto sin IVA
    iva = monto * TASA_IVA   # calcula el IVA
    total = monto + iva      # calcula el total con IVA
    return iva, total        # devuelve los dos resultados
 
 
def main():   # función principal: ordena todo el programa
    print("=== CALCULADORA DE IVA ===")   # título del programa
    texto = input("Monto de la factura (sin IVA): ")   # pide el monto (llega como texto)
    monto = float(texto.replace(",", "."))   # cambia coma por punto y convierte a decimal
    iva, total = calcular_iva(monto)   # usa la función y guarda los 2 resultados
    print("-" * 28)   # dibuja una línea de 28 guiones
    print(f"Monto : {MONEDA} {monto:,.2f}")   # muestra el monto con 2 decimales
    print(f"IVA   : {MONEDA} {iva:,.2f} ({TASA_IVA:.0%})")   # IVA y su porcentaje
    print(f"TOTAL : {MONEDA} {total:,.2f}")   # muestra el total con 2 decimales
 
 
main()   # ejecuta el programa
