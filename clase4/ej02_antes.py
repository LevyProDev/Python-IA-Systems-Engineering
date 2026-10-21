from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
ruta = Path(__file__).parent / "datos" / "ventas_desordenadas.csv"   # ubicación del CSV
df = pd.read_csv(ruta)                                # lee el CSV
print("Unidades vendidas:", df["cantidad"].sum())    # suma de la columna cantidad
print("Precio promedio:", df["precio_unitario"].mean())   # promedio de la columna precio
print("Precio máximo:", df["precio_unitario"].max())      # valor máximo de la columna precio
