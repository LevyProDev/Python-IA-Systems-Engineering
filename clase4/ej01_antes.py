from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos (pd es su apodo)
 
ruta = Path(__file__).parent / "datos" / "ventas_desordenadas.csv"   # ubicación del CSV
df = pd.read_csv(ruta)   # lee el CSV y lo convierte en una tabla (DataFrame)
print(df)                # muestra la tabla
