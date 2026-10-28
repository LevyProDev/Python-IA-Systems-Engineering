# crear_datos_prueba.py
# Crea los archivos de práctica de la Clase 4 (ventas desordenadas y gastos para el reto)
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
import pandas as pd        # librería para analizar datos (pd es su apodo)
 
CARPETA = Path(__file__).parent / "datos"   # carpeta donde se guardan los archivos
PRODUCTOS = {"Laptop": 5200, "Monitor": 1400, "Impresora": 1100, "Teclado": 150, "Mouse": 90}
REGIONES = ["La Paz", "Cochabamba", "Santa Cruz"]   # regiones de venta
VENDEDORES = ["Ana", "Luis", "Marta", "Carlos"]     # vendedores
 
 
def crear_ventas():   # crea la tabla de ventas con errores a propósito
    nombres = list(PRODUCTOS)   # lista con los nombres de los productos
    filas = []   # aquí guardaremos cada fila
    for i in range(60):   # 60 ventas
        producto = nombres[i % 5]   # el producto va rotando
        region = REGIONES[i % 3]   # la región va rotando
        cantidad = 1 + (i * 3) % 7   # cantidades entre 1 y 7
        vendedor = VENDEDORES[i % 4]   # el vendedor va rotando
        precio = PRODUCTOS[producto]   # precio según el producto
        if i in (4, 31):   # ERROR: región en mayúsculas
            region = region.upper()
        if i in (10, 37):   # ERROR: región con espacios y minúsculas
            region = f" {region.lower()} "
        if i == 14:   # ERROR: producto en minúsculas
            producto = producto.lower()
        if i in (8, 29, 50):   # ERROR: cantidad vacía
            cantidad = None
        if i in (13, 44):   # ERROR: vendedor vacío
            vendedor = None
        filas.append({
            "fecha": f"2026-{i % 6 + 1:02d}-{i % 27 + 1:02d}",
            "producto": producto,
            "region": region,
            "vendedor": vendedor,
            "cantidad": cantidad,
            "precio_unitario": precio,
        })
    df = pd.DataFrame(filas)   # convierte la lista en tabla
    return pd.concat([df, df.iloc[[0, 1, 2]]], ignore_index=True)   # ERROR: 3 filas duplicadas
 
 
def crear_gastos():   # crea la tabla de gastos para el reto
    departamentos = ["Contabilidad", "Legal", "Ventas", "Sistemas"]
    categorias = ["Viáticos", "Materiales", "Servicios"]
    filas = []   # aquí guardaremos cada fila
    for i in range(40):   # 40 gastos
        monto = 100 + (i * 37) % 900   # montos entre 100 y 999
        departamento = departamentos[i % 4]
        if i in (3, 18, 27):   # ERROR: monto escrito como texto
            monto = f"Bs {monto}"
        if i == 9:   # ERROR: monto vacío
            monto = None
        if i in (5, 22):   # ERROR: departamento en mayúsculas
            departamento = departamento.upper()
        filas.append({
            "fecha": f"2026-{i % 6 + 1:02d}-{i % 27 + 1:02d}",
            "departamento": departamento,
            "categoria": categorias[i % 3],
            "monto": monto,
            "responsable": ["Rosa", "Pedro", "Elena"][i % 3],
        })
    df = pd.DataFrame(filas)   # convierte la lista en tabla
    return pd.concat([df, df.iloc[[0, 1]]], ignore_index=True)   # ERROR: 2 filas duplicadas
 
 
def main():   # función principal
    CARPETA.mkdir(exist_ok=True)   # crea la carpeta datos si no existe
    ventas = crear_ventas()   # crea la tabla de ventas
    ventas.to_csv(CARPETA / "ventas_desordenadas.csv", index=False)   # guarda en CSV
    ruta_excel = CARPETA / "ventas_desordenadas.xlsx"   # ruta del Excel
    ventas.to_excel(ruta_excel, sheet_name="Ventas", index=False)   # lo guarda en Excel
    gastos = crear_gastos()   # crea la tabla de gastos
    gastos.to_csv(CARPETA / "reto_gastos.csv", index=False)   # guarda en CSV
    print("Archivos creados en la carpeta datos:")
    print(f"  ventas_desordenadas.csv  ({len(ventas)} filas)")
    print(f"  ventas_desordenadas.xlsx ({len(ventas)} filas)")
    print(f"  reto_gastos.csv          ({len(gastos)} filas)")
 
 
main()   # ejecuta el programa
