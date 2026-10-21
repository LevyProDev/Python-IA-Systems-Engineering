"""Mi archivo datos/ventas_desordenadas.csv tiene las columnas: fecha, producto, region, vendedor, cantidad, precio_unitario. Mejora este código de Pandas: crea la columna total (cantidad por precio_unitario); muestra ventas registradas, total vendido, venta promedio, máxima y mínima con formato de dinero; pide un producto por teclado, filtra sus ventas y muestra las 3 más grandes ordenadas de mayor a menor; si el producto no existe, avisa. Usa una función principal y comenta el código línea por línea."""
# Estadísticas, filtro y orden - versión mejorada con IA
from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
RUTA = Path(__file__).parent / "datos" / "ventas_desordenadas.csv"   # ubicación del CSV
 
 
def main():   # función principal
    df = pd.read_csv(RUTA)   # lee el CSV
    df["total"] = df["cantidad"] * df["precio_unitario"]   # nueva columna: total de cada venta
    print("=== ESTADÍSTICAS GENERALES ===")   # título
    print(f"Ventas registradas : {len(df)}")   # cantidad de filas
    print(f"Total vendido      : Bs {df['total'].sum():,.0f}")   # suma de totales
    print(f"Venta promedio     : Bs {df['total'].mean():,.0f}")   # promedio de totales
    print(f"Venta máxima       : Bs {df['total'].max():,.0f}")   # máximo
    print(f"Venta mínima       : Bs {df['total'].min():,.0f}")   # mínimo
    producto = input("¿Qué producto quieres ver? (ej: Laptop): ").strip().title()   # pide
    filtro = df[df["producto"] == producto]   # se queda solo con las filas de ese producto
    if filtro.empty:   # si no hay filas...
        print(f"No hay ventas de '{producto}'.")
        return   # termina el programa
    print(f"\nVentas de {producto}: {len(filtro)}")   # cuántas ventas tiene
    print("Las 3 más grandes:")   # encabezado
    top = filtro.sort_values("total", ascending=False).head(3)   # ordena de mayor a menor
    print(top[["fecha", "region", "cantidad", "total"]])   # muestra solo algunas columnas
 
 
main()   # ejecuta el programa
