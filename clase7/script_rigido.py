# script_rigido.py
# Un script "normal": hace SIEMPRE lo mismo, con el nombre de archivo exacto
import csv                 # para leer archivos CSV
from pathlib import Path   # herramienta para trabajar con rutas de archivos
 
RUTA = Path(__file__).parent / "demo" / "ventas_enero.csv"   # el nombre que el script espera
 
total = 0.0   # acumulador del total
with open(RUTA, encoding="utf-8", newline="") as archivo:   # abre el archivo (aquí se rompe)
    for fila in csv.DictReader(archivo):   # recorre cada venta
        total += float(fila["monto"])   # suma el monto
print(f"Total de ventas de enero: Bs {total:,.2f}")   # muestra el resultado
