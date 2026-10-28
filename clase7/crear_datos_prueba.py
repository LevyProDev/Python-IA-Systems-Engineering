# crear_datos_prueba.py
# Paso previo: crea los archivos de práctica (con un script que tiene errores a propósito)
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
BASE = Path(__file__).parent   # carpeta del proyecto (clase7)
DATOS = BASE / "datos"   # carpeta de datos
SCRIPTS = BASE / "scripts"   # carpeta de scripts
 
VENTAS = {   # nombre de archivo -> contenido
    "ventas_enero.csv": ("fecha,producto,monto\n2026-01-05,Laptop,5200\n2026-01-12,Mouse,90\n"
                         "2026-01-20,Teclado,150\n"),
    "ventas_febrero.csv": ("fecha,producto,monto\n2026-02-03,Monitor,1400\n2026-02-10,Impresora,1100\n"
                           "2026-02-17,Mouse,90\n2026-02-24,Mouse,90\n"),
    "ventas_marzo.csv": ("fecha,producto,monto\n2026-03-02,Laptop,5200\n2026-03-09,Monitor,1400\n"
                         "2026-03-16,Cable,Bs 350\n2026-03-23,Teclado,150\n"),   # ERROR: un monto trae "Bs"
}
NOTAS = "Recordatorio: el cierre contable de marzo es el 5 de abril.\n"
SCRIPT_CON_ERRORES = '''import csv
from pathlib import Path
 
carpeta = Path("datos")
total_general = 0.0
for archivo in sorted(carpeta.glob("ventas_*.csv")):
    subtotal = 0.0
    with open(archivo, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            subtotal += float(fila["total"])
    print(f"{archivo.name}: Bs {subtotal:,.2f}")
    total_general += subtotal
print(f"TOTAL GENERAL: Bs {total_general:,.2f}")
'''   # ERRORES: la columna se llama "monto", no "total"; y un valor trae "Bs"
 
 
def main():   # función principal
    DATOS.mkdir(exist_ok=True)   # crea la carpeta datos
    SCRIPTS.mkdir(exist_ok=True)   # crea la carpeta scripts
    for nombre, contenido in VENTAS.items():   # crea cada archivo de ventas
        (DATOS / nombre).write_text(contenido, encoding="utf-8")
    (DATOS / "notas.txt").write_text(NOTAS, encoding="utf-8")   # crea las notas
    (SCRIPTS / "resumen_ventas.py").write_text(SCRIPT_CON_ERRORES, encoding="utf-8")   # script con errores
    print("Archivos de práctica creados:")
    print("  datos/ventas_enero.csv, ventas_febrero.csv, ventas_marzo.csv, notas.txt")
    print("  scripts/resumen_ventas.py (tiene errores a propósito)")
 
 
main()   # ejecuta el programa
