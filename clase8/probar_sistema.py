# probar_sistema.py
# Comprueba que todo está listo ANTES de abrir la aplicación (no necesita el navegador)
import sys                          # para ver la versión de Python
from importlib.util import find_spec   # para saber si una librería está instalada
from pathlib import Path            # herramienta para trabajar con rutas de archivos
 
from buscador import buscar         # búsqueda de fragmentos
from lector_pdf import leer_pdf     # lector de PDF
from ollama_cliente import MODELO, modelo_instalado, servicio_activo   # conexión con la IA local
 
DOCS = Path(__file__).parent / "documentos_prueba"   # carpeta de documentos de prueba
resultados = []   # lista de (nombre de la prueba, True/False)
 
 
def comprobar(nombre, condicion):   # anota y muestra el resultado de una prueba
    resultados.append(condicion)   # guarda True o False
    print(f"  [{'OK' if condicion else 'FALLA'}] {nombre}")   # muestra OK o FALLA
 
 
def lee_con_error(archivo):   # True si leer ese PDF produce un aviso claro (ValueError)
    try:   # intenta leerlo
        leer_pdf((DOCS / archivo).read_bytes(), archivo)
    except ValueError:   # si da el aviso esperado...
        return True
    return False   # si no dio error, la prueba falla
 
 
def main():   # función principal
    print("=== PRUEBA DEL SISTEMA ===")   # título
    print(f"  [INFO] Python {sys.version_info.major}.{sys.version_info.minor} (el curso usa 3.13.7)")   # solo informa
    for libreria in ("streamlit", "pypdf", "reportlab"):   # revisa cada librería
        comprobar(f"Librería instalada: {libreria}", find_spec(libreria) is not None)
    hay_docs = (DOCS / "contrato_servicios_demo.pdf").exists()   # ¿existen los documentos de prueba?
    comprobar("Documentos de prueba creados", hay_docs)
    if hay_docs:   # solo prueba el resto si existen los documentos
        doc = leer_pdf((DOCS / "contrato_servicios_demo.pdf").read_bytes(), "contrato_servicios_demo.pdf")
        comprobar("El contrato se lee completo (12 páginas)", doc["n_paginas"] == 12)
        mejor = buscar(doc["fragmentos"], "¿Cuál es el plazo de pago?")   # busca el plazo de pago
        comprobar("La búsqueda encuentra el plazo de pago en la página 4", bool(mejor) and mejor[0]["pagina"] == 4)
        comprobar("El PDF sin texto da un aviso claro", lee_con_error("pdf_sin_texto_demo.pdf"))
        comprobar("El archivo dañado da un aviso claro", lee_con_error("archivo_danado_demo.pdf"))
    activo = servicio_activo()   # ¿Ollama está funcionando?
    comprobar("Ollama está activo", activo)
    comprobar(f"Modelo {MODELO} descargado", activo and modelo_instalado())
    print(f"Resultado: {sum(resultados)} de {len(resultados)} pruebas correctas")
    if all(resultados):   # si todo está bien...
        print("Todo listo. Ejecuta: python -m streamlit run app.py")
    else:   # si algo falló...
        print("Corrige las pruebas que fallaron antes de abrir la aplicación.")
 
 
main()   # ejecuta el programa
