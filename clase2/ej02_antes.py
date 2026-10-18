#Calcula el total de unos horarios
horarios = float(input("Horarios (Bs): ")) #pide los horarios como numero
iva = horarios * 0.13 # calcula el 13% del iva
total = horarios + iva #suma el iva a los horarios
print("Horarios:", horarios) #muestra los horarios
print("IVA:", iva) #muestra el iva
print("Total:", total) # muestra el total