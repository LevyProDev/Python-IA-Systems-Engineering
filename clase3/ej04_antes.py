from pathlib import Path # h. para trabajar con carpetas y archivos

base = Path(__file__).parent / "Descargas_Prueba" #carpeta de prueba
original = base / "factura_001.pdf" #archivo a renombrar
original.rename(base / "FAC-001.pdf") #renombra el archivo
print("Archivo renombrado") # avisa que termino