# crear_demo.py
# Crea la carpeta demo con un archivo de ventas cuyo nombre CAMBIÓ (el imprevisto del gancho)
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
CARPETA = Path(__file__).parent / "demo"   # carpeta de la demostración
CONTENIDO = """fecha,producto,monto
2026-01-05,Laptop,1200
2026-01-09,Monitor,850.5
2026-01-14,Teclado,430
2026-01-20,Impresora,2100
2026-01-25,Mouse,975.25
2026-01-30,Cable,300
"""   # 6 ventas: el total es 5855.75
 
 
def main():   # función principal
    CARPETA.mkdir(exist_ok=True)   # crea la carpeta demo si no existe
    (CARPETA / "ventas_enero_FINAL.csv").write_text(CONTENIDO, encoding="utf-8")   # archivo con otro nombre
    (CARPETA / "notas.txt").write_text("Recordatorio: cierre contable el 5 de febrero.\n", encoding="utf-8")
    print("Carpeta demo lista con 2 archivos:")   # avisa que terminó
    print("  ventas_enero_FINAL.csv")
    print("  notas.txt")
 
 
main()   # ejecuta el programa
