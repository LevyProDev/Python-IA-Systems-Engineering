from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
ruta = Path(__file__).parent / "datos" / "ventas_desordenadas.csv"   # ubicación del CSV
df = pd.read_csv(ruta)             # lee el CSV
print("Filas antes:", len(df))     # cuántas filas hay al inicio
df = df.dropna()                   # elimina TODA fila que tenga algún vacío
df = df.drop_duplicates()          # elimina filas repetidas
print("Filas después:", len(df))   # cuántas filas quedaron
