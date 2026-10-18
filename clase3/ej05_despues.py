"""Mejora este programa: mueve todos los PDF a la carpeta Documentos (créala si no existe), muestra cada movimiento y el total, y avisa si no había PDF. Usa una función y comenta el código línea por línea."""
# Mover todos los PDF a Documentos - versión mejorada con IA
import shutil              # herramienta para copiar y mover archivos
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
BASE = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
 
 
def mover_pdfs(base):   # mueve todos los PDF a la carpeta Documentos
    destino = base / "Documentos"   # carpeta de destino
    destino.mkdir(exist_ok=True)   # la crea si no existe
    movidos = 0   # contador de archivos movidos
    for archivo in sorted(base.glob("*.pdf")):   # recorre todos los PDF
        shutil.move(archivo, destino / archivo.name)   # mueve el archivo
        print(f"Movido: {archivo.name} -> Documentos")   # muestra qué movió
        movidos += 1   # suma 1 al contador
    return movidos   # devuelve cuántos movió
 
 
def main():   # función principal
    total = mover_pdfs(BASE)   # mueve los PDF
    if total == 0:   # si no había PDF...
        print("No había PDF para mover.")   # lo avisa
    else:   # si movió algo...
        print(f"Total movidos: {total}")   # resumen
 
 
main()   # ejecuta el programa
