from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
ruta = Path(__file__).parent / "datos" / "ventas_limpias.csv"   # CSV limpio (ejercicio 3)
df = pd.read_csv(ruta)                                   # lee el CSV
resumen = df.groupby("region")["total"].sum()            # total de ventas por región
resumen.to_csv(Path(__file__).parent / "resumen.csv")    # guarda el resumen en un CSV
print("Resumen guardado en resumen.csv")                 # avisa que terminó
