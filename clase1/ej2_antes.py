#Clasificar un plazo segun los dias que faltan
dias = int(input("Cuantos dias faltan para el plazo? ")) # pide los dias (entero)
if dias < 0: # si los dias son negativos
    print("El plazo vencido") # .. el plazo ya se paso
elif dias <= 3: # si no, faltan 3 dias o menos
    print("Urgente") # ... es urgente
else: 
    print("En tiempo") # ... es un plazo normal