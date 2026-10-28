from herramientas import ejecutar   # las herramientas que ya construimos
 
while True:   # repite hasta que el usuario escriba salir
    pedido = input("¿Qué necesitas? (salir para terminar): ").strip().lower()   # pide el pedido
    if pedido == "salir":   # si escribe salir...
        break   # sale del while
    if "archivos" in pedido:   # si el pedido contiene la palabra "archivos"
        print(ejecutar("listar_archivos", {}))   # usa listar_archivos
    elif "leer" in pedido:   # si contiene "leer"
        print(ejecutar("leer_archivo", {"nombre": "notas.txt"}))   # siempre lee notas.txt
    elif "total" in pedido:   # si contiene "total"
        print(ejecutar("total_ventas", {"nombre": "ventas_enero.csv"}))   # siempre enero
    else:   # si no reconoce ninguna palabra...
        print("No entendí tu pedido.")
