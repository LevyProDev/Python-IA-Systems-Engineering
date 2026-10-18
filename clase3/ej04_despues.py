# Renombrar PDF con fecha - versión mejorada con IA
from datetime import datetime   # para obtener la fecha de hoy
from pathlib import Path        # herramienta para trabajar con carpetas y archivos
 
BASE = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
 
 
def renombrar_con_fecha(base):   # agrega la fecha de hoy al inicio del nombre
    fecha = datetime.now().strftime("%Y-%m-%d")   # fecha de hoy, ejemplo: 2026-10-07
    renombrados = 0   # contador de archivos renombrados
    for archivo in sorted(base.glob("*.pdf")):   # recorre todos los PDF
        if archivo.name.startswith(fecha):   # si ya empieza con la fecha...
            print(f"Omitido (ya tiene fecha): {archivo.name}")
            continue   # salta al siguiente archivo
        nuevo = archivo.with_name(f"{fecha}_{archivo.name}")   # arma el nombre nuevo
        if nuevo.exists():   # si ese nombre ya existe...
            print(f"Omitido (ya existe): {nuevo.name}")
            continue   # salta al siguiente archivo
        archivo.rename(nuevo)   # renombra el archivo
        print(f"{archivo.name} -> {nuevo.name}")   # muestra el cambio
        renombrados += 1   # suma 1 al contador
    return renombrados   # devuelve cuántos renombró
 
 
def main():   # función principal
    total = renombrar_con_fecha(BASE)   # renombra los PDF
    print(f"Archivos renombrados: {total}")   # resumen
 
 
main()   # ejecuta el programa
