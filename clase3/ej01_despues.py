"""Mejora este programa que lista el contenido de una carpeta: muestra solo archivos (no carpetas), ordenados por nombre, numerados, con su extensión y el total; si la carpeta no existe, avisa con un mensaje. Usa una función. Comenta el código línea por línea."""
# Lista ordenada de archivos - versión mejorada con IA
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
CARPETA = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
 
 
def listar_archivos(carpeta):   # devuelve solo los archivos, ordenados
    archivos = []   # lista vacía donde guardaremos los archivos
    for elemento in carpeta.iterdir():   # recorre todo lo que hay dentro
        if elemento.is_file():   # si es un archivo (no una carpeta)...
            archivos.append(elemento)   # lo agrega a la lista
    return sorted(archivos)   # devuelve la lista ordenada por nombre
 
 
def main():   # función principal
    if not CARPETA.exists():   # si la carpeta no existe...
        print("No existe la carpeta de prueba. Ejecuta crear_archivos_prueba.py")
        return   # termina el programa
    archivos = listar_archivos(CARPETA)   # obtiene la lista de archivos
    print(f"Carpeta: {CARPETA.name}")   # muestra el nombre de la carpeta
    print(f"Archivos encontrados: {len(archivos)}")   # muestra cuántos hay
    print("-" * 36)   # línea separadora
    for numero, archivo in enumerate(archivos, start=1):   # numera cada archivo desde 1
        print(f"{numero:>2}. {archivo.name:<24} {archivo.suffix}")   # n°, nombre, ext.
 
 
main()   # ejecuta el programa
