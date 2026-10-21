from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
ruta = Path(__file__).parent / "datos" / "ventas_limpias.csv"   # CSV ya limpio (ejercicio 3)
df = pd.read_csv(ruta)                       # lee el CSV
print(df.groupby("region")["total"].sum())   # suma el total de ventas por región
