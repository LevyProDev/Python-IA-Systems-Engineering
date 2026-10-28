# asistente_oficina.py
# Asistente de Oficina Automático (Python 3.13 / 3.14)
import shutil                    # para mover archivos
from datetime import datetime    # para la fecha y hora del reporte
from pathlib import Path         # para trabajar con carpetas y archivos
 
BASE = Path(__file__).parent                 # carpeta donde está este script
CARPETA = BASE / "Descargas_Prueba"          # carpeta de trabajo (¡de prueba!)
REPORTES = BASE / "Reportes_Generados"       # carpeta donde se guardan los reportes
 
REGLAS = {                                   # regla: extensión -> carpeta de destino
    ".pdf": "Documentos", ".docx": "Documentos", ".txt": "Documentos",
    ".xlsx": "Reportes", ".csv": "Reportes",
    ".png": "Imágenes", ".jpg": "Imágenes",
    ".zip": "Respaldos",
}
CARPETA_OTROS = "Otros"                      # destino de lo que no tiene regla
 
 
def carpeta_destino(archivo):   # decide a qué carpeta va un archivo
    return REGLAS.get(archivo.suffix.lower(), CARPETA_OTROS)   # busca en REGLAS
 
 
def detectar_archivos(carpeta):   # devuelve la lista de archivos de la carpeta
    return sorted(item for item in carpeta.iterdir() if item.is_file())   # solo archivos
 
 
def nombre_libre(destino):   # evita sobrescribir un archivo que ya existe
    if not destino.exists():   # si el nombre está libre...
        return destino   # lo usa tal cual
    contador = 2   # si no, prueba con _2, _3, ...
    while True:   # repite hasta encontrar un nombre libre
        candidato = destino.with_name(f"{destino.stem}_{contador}{destino.suffix}")   # nombre
        if not candidato.exists():   # si ese nombre está libre...
            return candidato   # lo devuelve
        contador += 1   # si no, suma 1 y vuelve a probar
 
 
def guardar_reporte(movidos, errores):   # crea el reporte de lo realizado
    REPORTES.mkdir(exist_ok=True)   # crea la carpeta de reportes si no existe
    ahora = datetime.now()   # fecha y hora actuales
    archivo = REPORTES / f"reporte_{ahora:%Y-%m-%d_%H-%M}.txt"   # nombre con fecha y hora
    lineas = [   # líneas del reporte
        "REPORTE DEL ASISTENTE DE OFICINA",
        f"Fecha: {ahora:%Y-%m-%d %H:%M}",
        f"Carpeta: {CARPETA.name}",
        f"Archivos movidos: {len(movidos)}",
        f"Errores: {len(errores)}",
        "-" * 32,
    ]
    for nombre, destino in movidos:   # agrega cada archivo movido
        lineas.append(f"{nombre} -> {destino}")
    for nombre, motivo in errores:   # agrega cada error
        lineas.append(f"ERROR en {nombre}: {motivo}")
    archivo.write_text("\n".join(lineas) + "\n", encoding="utf-8")   # escribe el reporte
    return archivo   # devuelve la ruta del reporte
 
 
def main():   # función principal
    print("=== ASISTENTE DE OFICINA AUTOMÁTICO ===")   # título
    if not CARPETA.exists():   # valida que la carpeta exista
        print("No existe la carpeta de prueba. Ejecuta primero crear_archivos_prueba.py")
        return   # termina el programa
    archivos = detectar_archivos(CARPETA)   # detecta los archivos
    if not archivos:   # si no hay archivos...
        print("No hay archivos para organizar.")
        return   # termina el programa
    print(f"Archivos detectados: {len(archivos)}")   # muestra cuántos hay
    print("Plan de organización:")   # encabezado del plan
    for archivo in archivos:   # muestra qué se haría con cada archivo
        print(f"  {archivo.name:<22} -> {carpeta_destino(archivo)}")
    respuesta = input("¿Mover los archivos? (si/no): ").strip().lower()   # pide confirmación
    if respuesta != "si":   # si no confirma...
        print("Cancelado. No se movió ningún archivo.")
        return   # termina sin tocar nada
    movidos = []   # lista de archivos movidos
    errores = []   # lista de errores
    conteo = {}   # cuántos archivos fueron a cada carpeta
    for archivo in archivos:   # procesa cada archivo
        destino = carpeta_destino(archivo)   # decide la carpeta
        try:   # intenta mover (aprendido en la Clase 2)
            carpeta_final = CARPETA / destino   # ruta de la carpeta destino
            carpeta_final.mkdir(exist_ok=True)   # la crea si no existe
            nuevo = nombre_libre(carpeta_final / archivo.name)   # sin pisar otro
            shutil.move(archivo, nuevo)   # mueve el archivo
            movidos.append((archivo.name, destino))   # lo anota como movido
            conteo[destino] = conteo.get(destino, 0) + 1   # suma 1 a esa carpeta
        except OSError as error:   # si falla (permisos, archivo abierto...)
            errores.append((archivo.name, str(error)))   # anota el error y sigue
    reporte = guardar_reporte(movidos, errores)   # guarda el reporte
    print()   # línea en blanco
    for destino, cantidad in sorted(conteo.items()):   # resumen por carpeta
        print(f"  {destino:<10}: {cantidad} archivo(s)")
    print(f"Listo: {len(movidos)} movidos, {len(errores)} con error.")   # resumen general
    print(f"Reporte guardado: {reporte.name}")   # nombre del reporte
 
 
main()   # ejecuta el programa
