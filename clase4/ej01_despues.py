"""Tengo dos archivos con las mismas ventas, ventas_desordenadas.csv y ventas_desordenadas.xlsx, en una carpeta datos. Columnas: fecha, producto, region, vendedor, cantidad, precio_unitario. Mejora este código de Pandas: crea un menú para elegir CSV o Excel, valida la opción, muestra cuántas filas y columnas tiene la tabla, los tipos de datos y las primeras 5 filas, y detecta los valores vacíos por columna y las filas duplicadas. Usa funciones, controla si el archivo no existe y comenta el código línea por línea."""
# Explorador de datos - versión mejorada con IA
from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
CARPETA = Path(__file__).parent / "datos"   # carpeta donde están los archivos
ARCHIVOS = {   # opción del menú -> (tipo, ruta del archivo)
    "1": ("CSV", CARPETA / "ventas_desordenadas.csv"),
    "2": ("Excel", CARPETA / "ventas_desordenadas.xlsx"),
}
 
 
def cargar(opcion):   # lee el archivo elegido y devuelve la tabla
    tipo, ruta = ARCHIVOS[opcion]   # obtiene el tipo y la ruta
    if tipo == "CSV":   # si es CSV...
        return pd.read_csv(ruta)   # lo lee con read_csv
    return pd.read_excel(ruta)   # si no, es Excel: lo lee con read_excel
 
 
def mostrar_problemas(df):   # detecta vacíos y duplicados
    vacios = df.isna().sum()   # cuenta los vacíos de cada columna
    vacios = vacios[vacios > 0]   # se queda solo con las columnas que tienen vacíos
    print("Valores vacíos por columna:")   # encabezado
    for columna, cantidad in vacios.items():   # recorre cada columna con vacíos
        print(f"  {columna}: {cantidad}")   # muestra columna y cantidad
    print(f"Filas duplicadas: {df.duplicated().sum()}")   # cuenta filas repetidas
 
 
def main():   # función principal
    print("=== EXPLORADOR DE DATOS ===")   # título
    opcion = input("Abrir archivo (1 = CSV, 2 = Excel): ").strip()   # pide la opción
    if opcion not in ARCHIVOS:   # si la opción no existe...
        print("Opción no válida. Escribe 1 o 2.")
        return   # termina el programa
    try:   # intenta cargar el archivo
        df = cargar(opcion)   # carga la tabla
    except FileNotFoundError:   # si el archivo no existe...
        print("No se encontró el archivo. Ejecuta primero crear_datos_prueba.py")
        return   # termina el programa
    filas, columnas = df.shape   # shape = (filas, columnas)
    print(f"Tabla cargada: {filas} filas y {columnas} columnas")   # tamaño de la tabla
    print("Tipos de datos:")   # encabezado
    print(df.dtypes)   # tipo de dato de cada columna
    print("Primeras 5 filas:")   # encabezado
    print(df.head())   # muestra las primeras 5 filas
    mostrar_problemas(df)   # muestra vacíos y duplicados
 
 
main()   # ejecuta el programa
