"""Este código falla si la carpeta ya existe [pega el error]. Explica por qué y mejóralo: crea varias carpetas desde una lista, avisa si ya existen y que no falle al ejecutarlo dos veces. Comenta el código línea por línea."""
# Crear carpetas de trabajo - versión mejorada con IA
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
BASE = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
CARPETAS = ["Documentos", "Reportes", "Imágenes", "Respaldos", "Otros"]   # carpetas a crear
 
 
def main():   # función principal
    for nombre in CARPETAS:   # recorre cada nombre de carpeta
        carpeta = BASE / nombre   # arma la ruta completa
        if carpeta.exists():   # si ya existe...
            print(f"Ya existe: {nombre}")   # lo avisa y no falla
        else:   # si no existe...
            carpeta.mkdir(parents=True, exist_ok=True)   # la crea
            print(f"Creada   : {nombre}")   # avisa que la creó
 
 
main()   # ejecuta el programa
