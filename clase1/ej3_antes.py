# Calcula el IMC (índice de masa corporal)
peso = float(input("Peso en kg: "))          # pide el peso (texto -> decimal)
altura = float(input("Altura en metros: "))  # pide la altura (texto -> decimal)
imc = peso / (altura * altura)               # fórmula: peso / altura al cuadrado
print("Tu IMC es:", imc)                     # muestra el IMC
if imc < 18.5:                               # si el IMC es menor a 18.5...
    print("Bajo peso")                       # ...bajo peso
elif imc < 25:                               # si no, y es menor a 25...
    print("Normal")                          # ...normal
else:                                        # en cualquier otro caso...
    print("Sobrepeso")                       # ...sobrepeso
