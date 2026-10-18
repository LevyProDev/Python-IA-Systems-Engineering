#Contador 
#Calcular el IVA de una factura
monto = input("Monto de la factura: ") # el usuario escribir el monto que llega como texto
monto = float(monto)#convertir el texto a numero decimal
iva = monto * 0.13 # calcule el 13% del iva
total = monto + iva # suma del iva al monto
print("IVA:", iva) #muestre el iva
print("Total:", total) #muestre el total