"""Tengo datos/ventas_limpias.csv con las columnas: fecha, producto, region, vendedor, cantidad, precio_unitario y total. Mejora este código de Pandas: crea un menú que permita resumir las ventas por región, producto, vendedor o mes; muestra el total, el promedio y el número de ventas con nombres de columna claros, ordenado de mayor a menor; repite hasta que el usuario escriba “salir” y controla las opciones no válidas. Comenta el código línea por línea."""
# Resumen por grupos - versión mejorada con IA (menú interactivo)
from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
RUTA = Path(__file__).parent / "datos" / "ventas_limpias.csv"   # CSV limpio (ejercicio 3)
OPCIONES = {"1": "region", "2": "producto", "3": "vendedor", "4": "mes"}   # menú -> columna
 
 
def resumir(df, columna):   # agrupa y calcula total, promedio y cantidad de ventas
    resumen = df.groupby(columna)["total"].agg(["sum", "mean", "count"])   # agrupa y calcula
    resumen.columns = ["Total (Bs)", "Promedio (Bs)", "N° ventas"]   # nombres claros
    return resumen.sort_values("Total (Bs)", ascending=False).round(0)   # de mayor a menor
 
 
def main():   # función principal
    if not RUTA.exists():   # si no existe el CSV limpio...
        print("Falta ventas_limpias.csv. Ejecuta primero ej03_despues.py")
        return   # termina el programa
    df = pd.read_csv(RUTA, parse_dates=["fecha"])   # lee el CSV y convierte la fecha
    df["mes"] = df["fecha"].dt.month   # nueva columna: número de mes
    print("=== RESUMEN POR GRUPOS ===")   # título
    while True:   # repite hasta que el usuario escriba salir
        print("1) Región  2) Producto  3) Vendedor  4) Mes  (salir para terminar)")   # menú
        opcion = input("Elige una opción: ").strip().lower()   # pide la opción
        if opcion == "salir":   # si escribe salir...
            print("Hasta pronto.")
            break   # sale del while
        if opcion not in OPCIONES:   # si la opción no existe...
            print("  Opción no válida.")
            continue   # vuelve a preguntar
        print(resumir(df, OPCIONES[opcion]))   # muestra el resumen del grupo elegido
        print()   # línea en blanco
 
 
main()   # ejecuta el programa
