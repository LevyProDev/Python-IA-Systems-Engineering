"""Actúa como programador senior de Python 3.13. Soy profesional de oficina (contador, abogado o administrador) y mi carpeta de descargas está desordenada. Problema: organizar archivos automáticamente. Entradas: una carpeta con archivos mezclados. Proceso: detectar los archivos y decidir la carpeta según la extensión (PDF, Word y TXT a Documentos; Excel y CSV a Reportes; imágenes a Imágenes; ZIP a Respaldos; el resto a Otros). Decisiones: mostrar el plan y pedir confirmación antes de mover; no sobrescribir archivos existentes; si un archivo falla, seguir con los demás. Salidas: archivos movidos a sus carpetas y un reporte con fecha y hora en el nombre. Restricciones: nivel básico-intermedio, usar pathlib, shutil, funciones y try/except, trabajar solo en una carpeta de prueba. Primero muéstrame el diseño en pasos y luego el código comentado línea por línea."""
# crear_archivos_prueba.py
# Crea (o reinicia) una carpeta de PRUEBA con archivos de ejemplo
import shutil                # herramienta para borrar una carpeta completa
from pathlib import Path     # herramienta para trabajar con carpetas y archivos
 
CARPETA = Path(__file__).parent / "Descargas_Prueba"   # carpeta de prueba junto a este script
 
ARCHIVOS = [                 # lista con los nombres de los archivos de ejemplo
    "factura_001.pdf", "factura_002.pdf", "contrato_alquiler.pdf",
    "informe_final.docx", "notas_reunion.txt",
    "ventas_enero.xlsx", "presupuesto_2026.xlsx",
    "logo_empresa.png", "foto_equipo.jpg",
    "respaldo_viejo.zip", "borrador.tmp", "datos_raros.xyz",
]
 
 
def main():   # función principal
    if CARPETA.exists():   # si la carpeta de prueba ya existe...
        shutil.rmtree(CARPETA)   # borra SOLO esta carpeta de prueba
    CARPETA.mkdir()   # crea la carpeta vacía
    for nombre in ARCHIVOS:   # recorre cada nombre de la lista
        ruta = CARPETA / nombre   # ruta del archivo nuevo
        ruta.write_text(f"Archivo de prueba: {nombre}\n", encoding="utf-8")   # lo crea
    print(f"Carpeta de prueba lista: {CARPETA.name}")   # avisa que terminó
    print(f"Archivos creados: {len(ARCHIVOS)}")   # muestra cuántos archivos hay
 
 
main()   # ejecuta el programa
