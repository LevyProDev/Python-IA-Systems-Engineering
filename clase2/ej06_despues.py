"""Mejora este programa para que vuelva a pedir el dato hasta que sea válido: crea una función pedir_numero con while True y try/except, cuenta los intentos, acepta coma decimal y muestra un mensaje claro en cada error. Comenta el código línea por línea."""
# Registro de horas - versión mejorada con IA (repite hasta que el dato sea válido)
TARIFA = 40   # Bs por hora
 
 
def pedir_numero(mensaje):   # función reutilizable: pide un número válido
    intentos = 0   # contador de intentos
    while True:   # repite hasta que se ejecute un return
        intentos = intentos + 1   # suma 1 en cada vuelta
        texto = input(mensaje).strip().replace(",", ".")   # limpia y acepta coma
        try:   # intenta convertir a número
            return float(texto)   # si funciona, devuelve el número y termina
        except ValueError:   # si falla...
            print(f"  '{texto}' no es un número (intento {intentos}). Prueba de nuevo.")
 
 
def main():   # función principal
    horas = pedir_numero("Horas trabajadas: ")   # pide las horas, ya validadas
    print(f"Registrado: {horas} horas")   # confirma el registro
    print(f"Pago: Bs {horas * TARIFA:,.2f}")   # calcula y muestra el pago
 
 
main()   # ejecuta el programa
