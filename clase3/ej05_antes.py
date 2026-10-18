import shutil              # herramienta para copiar y mover archivos
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
base = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
carpeta = base / "Documentos"                       # carpeta de destino
carpeta.mkdir(exist_ok=True)                        # la crea si no existe
shutil.move(base / "informe_final.docx", carpeta / "informe_final.docx")   # mueve un archivo
print("Archivo movido")                             # avisa que terminó
