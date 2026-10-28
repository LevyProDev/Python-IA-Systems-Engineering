"""Actúa como programador senior de Python 3.13. Soy profesional independiente (contador, abogado o notario) y quiero un facturador que no se cierre cuando me equivoco al escribir. Problema: calcular IVA y cuotas sin que el programa se caiga. Entradas: cliente, monto sin IVA y número de cuotas. Proceso: IVA del 13%, total y valor de cada cuota. Decisiones: si el monto no es un número o las cuotas son 0, mostrar un mensaje amigable y volver a pedir el dato; guardar cada error en diagnostico.txt con tipo de error, mensaje, línea y código. Salidas: factura con monto, IVA, total y cuotas en Bs. Restricciones: nivel básico-intermedio, usar funciones, try/except y while, sin librerías externas. Primero muéstrame el diseño y luego el código comentado línea por línea."""
# facturador_seguro.py
# Facturador que se recupera de errores y prepara un diagnóstico para la IA
# Funciona con Python 3.13 y 3.14
import traceback   # módulo para leer los datos del Traceback
 
TASA_IVA = 0.13   # IVA del 13% (se cambia en un solo lugar)
MONEDA = "Bs"     # moneda que se muestra
 
# Mini "IA local": explicaciones listas para los errores más comunes
EXPLICACIONES = {
    "ValueError": "El texto escrito no se puede convertir a número.",
    "ZeroDivisionError": "No se puede dividir entre cero.",
}
 
 
def explicar(error):   # devuelve una explicación sencilla del error
    nombre = type(error).__name__   # obtiene el nombre del tipo de error
    return EXPLICACIONES.get(nombre, "Error desconocido: pega el reporte en la IA.")
 
 
def guardar_diagnostico(error, contexto):   # guarda un reporte listo para la IA
    ultimo = traceback.extract_tb(error.__traceback__)[-1]   # último paso del Traceback
    reporte = (
        f"Tipo de error: {type(error).__name__}\n"   # nombre del error
        f"Mensaje: {error}\n"                        # mensaje original de Python
        f"Línea: {ultimo.lineno}\n"                  # número de línea donde ocurrió
        f"Código: {ultimo.line}\n"                   # texto de esa línea
        f"Contexto: {contexto}\n"                    # qué estaba pasando
        + "-" * 30 + "\n"                            # línea separadora
    )
    with open("diagnostico.txt", "a", encoding="utf-8") as archivo:   # "a" = agregar al final
        archivo.write(reporte)   # escribe el reporte en el archivo
 
 
def pedir_numero(mensaje):   # pide un número y repite hasta que sea válido
    while True:   # se repite hasta que se ejecute un return
        texto = input(mensaje).strip().replace(",", ".")   # limpia y acepta coma
        try:   # intenta convertir el texto a número
            return float(texto)   # si funciona, devuelve el número y termina
        except ValueError as error:   # si el texto no es un número...
            guardar_diagnostico(error, f"El usuario escribió: {texto!r}")   # guarda reporte
            print("  Eso no es un número. Ejemplo válido: 1500.50")   # mensaje amigable
            print("  Tip:", explicar(error))   # explicación breve
 
 
def calcular_cuota(total, cuotas):   # reparte el total en cuotas
    return total / cuotas   # si cuotas es 0, aquí ocurre ZeroDivisionError
 
 
def main():   # función principal del programa
    print("=== FACTURADOR A PRUEBA DE ERRORES ===")   # título
    cliente = input("Cliente: ").strip()   # pide el nombre del cliente
    monto = pedir_numero("Monto sin IVA (Bs): ")   # pide el monto (ya validado)
    iva = monto * TASA_IVA   # calcula el IVA
    total = monto + iva   # calcula el total con IVA
    while True:   # repite hasta tener unas cuotas válidas
        cuotas = int(pedir_numero("Número de cuotas: "))   # pide cuotas, las pasa a entero
        try:   # intenta calcular la cuota
            cuota = calcular_cuota(total, cuotas)   # puede fallar si cuotas es 0
            break   # si no falló, sale del while
        except ZeroDivisionError as error:   # si se dividió entre cero...
            guardar_diagnostico(error, f"Cuotas ingresadas: {cuotas}")   # guarda reporte
            print("  Las cuotas no pueden ser 0.")   # mensaje amigable
            print("  Tip:", explicar(error))   # explicación breve
    print()   # línea en blanco
    print("===== FACTURA =====")   # encabezado de la factura
    print(f"Cliente   : {cliente}")   # muestra el cliente
    print(f"Monto     : {MONEDA} {monto:,.2f}")   # muestra el monto
    print(f"IVA ({TASA_IVA:.0%}) : {MONEDA} {iva:,.2f}")   # muestra el IVA
    print(f"Total     : {MONEDA} {total:,.2f}")   # muestra el total
    print(f"Cuotas    : {cuotas} de {MONEDA} {cuota:,.2f}")   # muestra las cuotas
 
 
main()   # ejecuta el programa
