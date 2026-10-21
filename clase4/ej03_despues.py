"""Mi tabla ventas_desordenadas.csv tiene estos problemas: filas duplicadas, cantidades vacías, vendedores vacíos, región y producto con espacios y mayúsculas distintas, y la fecha como texto. Mejora este código: elimina duplicados, elimina solo las filas sin cantidad, llena los vendedores vacíos con “Sin asignar”, estandariza región y producto, convierte la fecha a fecha real y crea la columna total. Usa una función limpiar, muestra cuántas filas se eliminaron y, antes de guardar datos/ventas_limpias.csv, pide confirmación. Comenta el código línea por línea."""
# Limpieza de datos - versión mejorada con IA
from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
CARPETA = Path(__file__).parent / "datos"   # carpeta de datos
 
 
def limpiar(df):   # recibe la tabla sucia y devuelve la tabla limpia
    df = df.drop_duplicates()   # elimina filas repetidas
    df = df.dropna(subset=["cantidad"])   # elimina solo las ventas sin cantidad
    df["region"] = df["region"].str.strip().str.title()   # estandariza el texto
    df["producto"] = df["producto"].str.strip().str.title()   # igual para el producto
    df["vendedor"] = df["vendedor"].fillna("Sin asignar")   # llena los vendedores vacíos
    df["fecha"] = pd.to_datetime(df["fecha"])   # convierte el texto en fecha real
    df["total"] = df["cantidad"] * df["precio_unitario"]   # nueva columna: total de cada venta
    return df   # devuelve la tabla limpia
 
 
def main():   # función principal
    df = pd.read_csv(CARPETA / "ventas_desordenadas.csv")   # lee el CSV sucio
    inicio = len(df)   # filas al inicio
    duplicados = df.duplicated().sum()   # filas repetidas
    sin_cantidad = df["cantidad"].isna().sum()   # filas sin cantidad
    limpio = limpiar(df)   # limpia la tabla
    print("=== LIMPIEZA DE DATOS ===")   # título
    print(f"Filas al inicio        : {inicio}")
    print(f"Duplicados eliminados  : {duplicados}")
    print(f"Sin cantidad eliminadas: {sin_cantidad}")
    print(f"Filas finales          : {len(limpio)}")
    print(f"Regiones: {sorted(limpio['region'].unique())}")   # regiones únicas
    print(f"Productos: {sorted(limpio['producto'].unique())}")   # productos únicos
    respuesta = input("¿Guardar ventas_limpias.csv? (si/no): ").strip().lower()   # confirma
    if respuesta == "si":   # si confirma...
        limpio.to_csv(CARPETA / "ventas_limpias.csv", index=False)   # guarda el CSV limpio
        print("Archivo guardado: datos/ventas_limpias.csv")
    else:   # si no confirma...
        print("No se guardó ningún archivo.")
 
 
main()   # ejecuta el programa
