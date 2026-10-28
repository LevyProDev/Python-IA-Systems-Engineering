"""Mejora este programa para un profesional de salud: separa el cálculo y la clasificación en dos funciones, agrega la categoría Obesidad, muestra el IMC con 1 decimal, acepta coma decimal y agrega un aviso de que el dato es orientativo. Comenta el código línea por línea.
"""
# Calculadora de IMC - versión mejorada con IA
def calcular_imc(peso, altura):   # función: recibe peso (kg) y altura (m)
    return peso / (altura ** 2)   # devuelve el IMC (altura al cuadrado)
 
 
def clasificar_imc(imc):   # función: recibe el IMC y devuelve su categoría
    if imc < 18.5:   # menor a 18.5
        return "Bajo peso"
    elif imc < 25:   # de 18.5 a 24.9
        return "Peso normal"
    elif imc < 30:   # de 25 a 29.9
        return "Sobrepeso"
    else:   # 30 o más
        return "Obesidad"
 
 
def main():   # función principal
    print("=== CALCULADORA DE IMC ===")   # título
    peso = float(input("Peso (kg): ").replace(",", "."))   # pide el peso, acepta coma
    altura = float(input("Altura (m): ").replace(",", "."))   # pide la altura, acepta coma
    imc = calcular_imc(peso, altura)   # calcula el IMC con la función
    categoria = clasificar_imc(imc)   # obtiene la categoría con la otra función
    print("-" * 30)   # línea separadora
    print(f"IMC      : {imc:.1f}")   # muestra el IMC con 1 decimal
    print(f"Categoría: {categoria}")   # muestra la categoría
    print("Dato orientativo: no reemplaza una consulta profesional.")   # aviso
 
 
main()   # ejecuta el programa
