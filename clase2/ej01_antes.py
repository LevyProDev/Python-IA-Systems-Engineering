# Aprueba un gasto según su monto
monto = float(input("Monto del gasto (Bs): ")) # pide el monto y lo convierte a numero
# si el monto es mayor a 1000...
if monto > 1000:
    print("Requiere aprobacion del gerente") #..necesita aprobacion
else: 
    print("Gasto aprobado") #..el gasto se apruba