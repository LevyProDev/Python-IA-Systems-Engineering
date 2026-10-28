import csv
from pathlib import Path
 
carpeta = Path("datos")
total_general = 0.0
for archivo in sorted(carpeta.glob("ventas_*.csv")):
    subtotal = 0.0
    with open(archivo, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            subtotal += float(fila["total"])
    print(f"{archivo.name}: Bs {subtotal:,.2f}")
    total_general += subtotal
print(f"TOTAL GENERAL: Bs {total_general:,.2f}")
