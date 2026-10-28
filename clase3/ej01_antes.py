from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
carpeta = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
for elemento in carpeta.iterdir():                     # recorre todo lo que hay dentro
    print(elemento.name)                               # muestra el nombre de cada elemento
