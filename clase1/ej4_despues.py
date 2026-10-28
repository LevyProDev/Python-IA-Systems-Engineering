"""Mejora este programa para un negocio: usa funciones para evaluar el estado del stock (AGOTADO, REPONER, EN LÍMITE u OK) y para calcular cuántas unidades pedir hasta llegar al doble del mínimo. Usa una constante para ese factor y muestra el resultado ordenado. Comenta el código línea por línea"""
# Control de inventario - versión mejorada con IA
FACTOR_OBJETIVO = 2   # constante: queremos tener el doble del mínimo
 
 
def evaluar_stock(stock, minimo):   # función: devuelve el estado del producto
    if stock == 0:   # no queda nada
        return "AGOTADO"
    elif stock < minimo:   # queda menos del mínimo
        return "REPONER"
    elif stock == minimo:   # justo en el límite
        return "EN LÍMITE"
    else:   # hay de sobra
        return "OK"
 
 
def cantidad_a_pedir(stock, minimo):   # función: calcula cuánto comprar
    objetivo = minimo * FACTOR_OBJETIVO   # cantidad ideal que queremos tener
    return objetivo - stock               # lo que falta para llegar al ideal
 
 
def main():   # función principal
    print("=== CONTROL DE INVENTARIO ===")   # título
    producto = input("Producto: ").strip()   # pide el producto
    stock = int(input("Stock actual: "))   # pide el stock actual
    minimo = int(input("Stock mínimo: "))   # pide el stock mínimo
    estado = evaluar_stock(stock, minimo)   # obtiene el estado con la función
    print("-" * 30)   # línea separadora
    print(f"Producto: {producto}")   # muestra el producto
    print(f"Estado  : {estado}")   # muestra el estado
    if estado == "AGOTADO" or estado == "REPONER":   # si hay que comprar...
        pedido = cantidad_a_pedir(stock, minimo)   # calcula cuánto
        print(f"Pedido sugerido: {pedido} unidades")   # ...y lo muestra
 
 
main()   # ejecuta el programa
