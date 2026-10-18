"""
Mejora este programa para un abogado: pide el nombre del caso, clasifica el plazo en 4 niveles (vencido, urgente si faltan 3 días o menos, próximo si faltan 10 o menos, en tiempo), usa una función que devuelva el estado y la acción recomendada, y muestra el resultado ordenado. Comenta el código línea por línea.
"""
# Semáforo de plazos - versión mejorada con IA
def clasificar_plazo(dias):   # función: recibe los días que faltan
    if dias < 0:   # ya pasó la fecha
        return "VENCIDO", "Actuar hoy: revisar las opciones disponibles"
    elif dias <= 3:   # faltan 3 días o menos
        return "URGENTE", "Priorizar este caso hoy"
    elif dias <= 10:   # faltan entre 4 y 10 días
        return "PRÓXIMO", "Programar la preparación esta semana"
    else:   # faltan más de 10 días
        return "EN TIEMPO", "Mantener en seguimiento"
 
 
def main():   # función principal
    print("=== SEMÁFORO DE PLAZOS ===")   # título
    caso = input("Nombre del caso: ").strip()   # pide el caso y quita espacios sobrantes
    dias = int(input("Días restantes para el plazo: "))   # pide los días (entero)
    estado, accion = clasificar_plazo(dias)   # la función devuelve estado y acción
    print("-" * 30)   # línea separadora
    print(f"Caso  : {caso}")   # muestra el caso
    print(f"Plazo : {dias} día(s)")   # muestra los días
    print(f"Estado: {estado}")   # muestra el estado
    print(f"Acción: {accion}")   # muestra la acción recomendada
 
 
main()   # ejecuta el programa
