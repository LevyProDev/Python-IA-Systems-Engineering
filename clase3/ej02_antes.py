from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
base = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
(base / "Documentos").mkdir()                       # crea la carpeta Documentos dentro de base
print("Carpeta Documentos creada")                  # avisa que se creó
