"""Actúa como programador senior de Python 3.13. Soy un profesional independiente (contador, abogado o consultor) y pierdo tiempo armando cotizaciones a mano. Problema: calcular cotizaciones rápido y sin errores. Entradas: nombre del cliente, servicio (1 contable, 2 legal, 3 consultoría), horas estimadas y si es urgente. Proceso: tarifa por hora según el servicio × horas; recargo del 20% si es urgente. Decisiones: descuento del 10% desde 10 horas y del 15% desde 20 horas; avisar si el servicio no es válido. Salidas: cotización con subtotal, recargo, descuento, IVA del 13% y total en Bs, y guardarla en cotizacion.txt. Restricciones: nivel básico-intermedio, usar funciones, if/elif/else, input() y print(), sin librerías externas. Primero muéstrame el diseño en pasos y luego el código comentado."""
# cotizador.py
# Cotizador profesional automático (Python 3.13 / 3.14)
 
# --- Datos que podemos cambiar fácilmente ---
TASA_IVA = 0.15          # IVA del 15%
RECARGO_URGENTE = 0.20   # 20% extra si el trabajo es urgente
MONEDA = "Bs"            # moneda que se muestra
 
 
def tarifa_por_servicio(opcion):
    """Devuelve el nombre del servicio y su tarifa por hora."""
    if opcion == "1":
        return "Asesoría contable", 150
    elif opcion == "2":
        return "Asesoría legal", 250
    elif opcion == "3":
        return "Consultoría de negocios", 200
    else:
        return "Servicio no válido", 0
 
 
def calcular_descuento(horas):
    """Más horas contratadas = más descuento."""
    if horas >= 20:
        return 0.15
    elif horas >= 10:
        return 0.10
    else:
        return 0.0
 
 
def main():
    print("=== COTIZADOR PROFESIONAL ===")
    cliente = input("Nombre del cliente: ").strip()
    print("1) Asesoría contable | 2) Asesoría legal | 3) Consultoría")
    opcion = input("Elige un servicio (1-3): ").strip()
 
    servicio, tarifa = tarifa_por_servicio(opcion)
    if tarifa == 0:
        print("Opción no válida. Ejecuta el programa otra vez.")
        return  # termina el programa aquí
 
    horas = int(input("Horas estimadas: "))
    urgente = input("¿Es urgente? (si/no): ").strip().lower() == "si"
 
    # --- Cálculos ---
    subtotal = tarifa * horas
    recargo = 0
    if urgente:
        recargo = subtotal * RECARGO_URGENTE
    porcentaje = calcular_descuento(horas)
    descuento = (subtotal + recargo) * porcentaje
    base = subtotal + recargo - descuento
    iva = base * TASA_IVA
    total = base + iva
 
    # --- Resultado ---
    resumen = f"""
==============================
        COTIZACIÓN
==============================
Cliente  : {cliente}
Servicio : {servicio}
Horas    : {horas} x {MONEDA} {tarifa}
------------------------------
Subtotal : {MONEDA} {subtotal:,.2f}
Recargo  : {MONEDA} {recargo:,.2f}
Descuento: {MONEDA} {descuento:,.2f} ({porcentaje:.0%})
IVA      : {MONEDA} {iva:,.2f} ({TASA_IVA:.0%})
------------------------------
TOTAL    : {MONEDA} {total:,.2f}
=============================="""
    print(resumen)
 
    # --- Guardar la cotización en un archivo de texto ---
    with open("cotizacion.txt", "w", encoding="utf-8") as archivo:
        archivo.write(resumen)
    print("Cotización guardada en cotizacion.txt")
 
 
main()
