import shutil              # herramienta para copiar y mover archivos
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
base = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
origen = base / "factura_001.pdf"                   # archivo que queremos copiar
destino = base / "Respaldo" / "factura_001.pdf"     # dónde queremos la copia
shutil.copy2(origen, destino)                       # copia el archivo (conserva fechas)
print("Copia lista")                                # avisa que terminó
