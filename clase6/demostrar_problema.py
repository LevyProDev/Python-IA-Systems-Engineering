# demostrar_problema.py
# Muestra por qué NO conviene pegar un manual gigante en una IA, ni buscarlo a mano
import json                 # para enviar y leer datos en formato JSON
import time                 # para medir cuánto tarda la respuesta
import unicodedata          # para ignorar tildes al buscar
import urllib.error         # tipos de error de conexión
import urllib.request       # para enviar peticiones a Ollama
from pathlib import Path    # herramienta para trabajar con rutas de archivos
from pypdf import PdfReader   # librería para leer PDF
 
PDF = Path(__file__).parent / "manual_politicas_2026.pdf"   # el PDF que creamos
URL = "http://localhost:11434/api/chat"   # dirección LOCAL de Ollama
MODELO = "llama3.2:3b"   # modelo local
CONTEXTO_APROX = 4096   # tamaño aproximado de "memoria de trabajo" de un modelo pequeño (tokens)
 
 
def sin_tildes(texto):   # pasa a minúsculas y quita tildes: "Pagó" -> "pago"
    descompuesto = unicodedata.normalize("NFD", texto.lower())   # separa letras y tildes
    return descompuesto.encode("ascii", "ignore").decode("ascii")   # se queda solo con las letras
 
 
def preguntar_con_todo(texto, pregunta):   # envía TODO el manual al modelo (mala idea)
    prompt = f"Responde con base en este manual.\n\n{texto}\n\nPregunta: {pregunta}"   # manual + pregunta
    datos = {"model": MODELO, "messages": [{"role": "user", "content": prompt}], "stream": False}
    peticion = urllib.request.Request(
        URL, data=json.dumps(datos).encode("utf-8"), headers={"Content-Type": "application/json"})
    abridor = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # conexión directa, sin proxy
    with abridor.open(peticion, timeout=300) as respuesta:   # envía y espera
        return json.loads(respuesta.read().decode("utf-8"))["message"]["content"]   # texto de la respuesta
 
 
def main():   # función principal
    if not PDF.exists():   # si falta el PDF...
        print("No se encontró el PDF. Ejecuta primero: python crear_pdf_prueba.py")
        return   # termina el programa
    lector = PdfReader(str(PDF))   # abre el PDF
    paginas = [pagina.extract_text() or "" for pagina in lector.pages]   # texto de cada página
    texto = "\n".join(paginas)   # todo el texto junto
    tokens = len(texto) // 4   # regla práctica: 1 token ≈ 4 caracteres
    print("=== EL PROBLEMA ===")   # título
    print(f"Páginas del manual      : {len(paginas)}")
    print(f"Caracteres              : {len(texto):,}".replace(",", "."))
    print(f"Palabras (aprox.)       : {len(texto.split()):,}".replace(",", "."))
    print(f"Tokens (aprox.)         : {tokens:,}".replace(",", "."))
    print(f"Memoria del modelo      : ~{CONTEXTO_APROX:,} tokens".replace(",", "."))
    print(f"El manual equivale a {tokens / CONTEXTO_APROX:.1f} veces esa memoria.")
    print("\n--- Búsqueda por palabra clave (como Ctrl+F) ---")   # parte 2
    while True:   # repite hasta que el usuario pulse Enter
        palabra = input("Palabra o frase a buscar (Enter para terminar): ").strip()   # pide la palabra
        if palabra == "":   # si no escribe nada...
            break   # sale del while
        buscada = sin_tildes(palabra)   # palabra sin tildes
        encontradas = [n for n, t in enumerate(paginas, start=1) if buscada in sin_tildes(t)]   # páginas
        if encontradas:   # si hay coincidencias...
            print(f"  '{palabra}' aparece en {len(encontradas)} páginas: {encontradas[:8]}...")
        else:   # si no hay...
            print(f"  '{palabra}' no aparece en ninguna página (aunque la idea sí esté en el manual).")
    respuesta = input("\n¿Enviar el manual COMPLETO al modelo local? (si/no): ").strip().lower()
    if respuesta != "si":   # si no quiere...
        print("Fin de la demostración.")
        return   # termina el programa
    pregunta = input("Pregunta (Enter = ¿Cuál es el plazo de pago a proveedores?): ").strip()
    if pregunta == "":   # si no escribe nada...
        pregunta = "¿Cuál es el plazo de pago a proveedores?"   # usa la pregunta por defecto
    print("Enviando el manual completo... esto puede tardar.")   # aviso
    inicio = time.perf_counter()   # marca la hora de inicio
    try:   # intenta consultar al modelo
        respuesta_ia = preguntar_con_todo(texto, pregunta)   # envía todo el manual
    except (urllib.error.URLError, TimeoutError):   # si falla la conexión o tarda demasiado...
        print("No se pudo obtener respuesta (Ollama apagado o demasiado lento).")
        return   # termina el programa
    print(f"\nRespuesta ({time.perf_counter() - inicio:.1f} s):\n{respuesta_ia}")
    print("\nCompara con el manual: ¿es correcta y completa? ¿Se mareó?")
 
 
main()   # ejecuta el programa
