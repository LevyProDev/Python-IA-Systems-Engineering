# Revisa si hay que reponer un producto
producto = input("Producto: ")                # pide el nombre del producto
stock = int(input("Stock actual: "))          # pide cuántas unidades hay
minimo = int(input("Stock mínimo: "))         # pide el mínimo que debe haber
if stock < minimo:                            # si hay menos del mínimo...
    print("Hay que reponer", producto)        # ...avisa que hay que reponer
else:                                         # si no...
    print("Stock suficiente")                 # ...el stock alcanza
