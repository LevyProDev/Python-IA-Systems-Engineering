import csv
from pathlib import Path
import re
import statistics
import decimal
import json
import datetime
import math

carpeta = Path("datos")
total_general = 0.0
for archivo in sorted(carpeta.glob("ventas_*.csv")):
    subtotal = 0.0
    with open(archivo, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            # Revisa si el campo 'monto' existe en la fila
            if 'monto' in fila:
                # Extrae el valor del campo 'monto' y lo convierte a float
                monto = re.sub(r'[^\d\.]', '', fila["monto"])
                if monto:  # Verifica si el valor no es vacío
                    subtotal += float(monto)
    print(f"{archivo.name}: Bs {subtotal:,.2f}")
    total_general += subtotal
print(f"TOTAL GENERAL: Bs {total_general:,.2f}")
