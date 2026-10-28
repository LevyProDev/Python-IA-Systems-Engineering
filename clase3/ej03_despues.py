"""Este es mi código y este es el error: [pega el código] [pega el error]. Explica por qué falla. Luego mejóralo: crea la carpeta Respaldo si no existe, copia todos los PDF, muestra cuáles copió y el total. Comenta el código línea por línea."""
# Respaldo de todos los PDF - versión mejorada con IA
import shutil              # herramienta para copiar y mover archivos
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
BASE = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
 
 
def respaldar_pdfs(base):   # copia todos los PDF a la carpeta Respaldo
    destino = base / "Respaldo"   # carpeta donde irán las copias
    destino.mkdir(exist_ok=True)   # la crea si no existe (así no falla)
    copiados = 0   # contador de copias
    for archivo in sorted(base.glob("*.pdf")):   # busca los archivos .pdf
        shutil.copy2(archivo, destino / archivo.name)   # copia el archivo
        print(f"Copiado: {archivo.name}")   # muestra cuál copió
        copiados += 1   # suma 1 al contador
    return copiados   # devuelve cuántos copió
 
 
def main():   # función principal
    total = respaldar_pdfs(BASE)   # hace el respaldo
    print(f"Respaldo terminado: {total} archivo(s)")   # resumen
 
 
main()   # ejecuta el programa
