# gancho_local.py
# Gancho de la Clase 5: una IA que lee un informe financiero SIN internet
import json               # para enviar y leer datos en formato JSON
import time               # para medir cuánto tarda la respuesta
import urllib.error       # tipos de error de conexión
import urllib.request     # para enviar peticiones a Ollama
 
URL = "http://localhost:11434/api/chat"   # dirección LOCAL de Ollama (tu computadora)
MODELO = "llama3.2:3b"                    # modelo que descargamos con: ollama pull llama3.2:3b
 
INFORME = """Informe del 3.er trimestre 2026 - Andina Demo S.R.L. (empresa ficticia)
Ingresos: julio Bs 120.000, agosto Bs 135.000, septiembre Bs 128.000.
Total de ingresos del trimestre: Bs 395.000.
Gastos: sueldos Bs 150.000, alquiler Bs 36.000, servicios Bs 18.000, marketing Bs 22.000.
Total de gastos: Bs 226.000. Utilidad: Bs 169.000.
Comentario de gerencia: las ventas de septiembre fueron las más altas del trimestre."""
 
PROMPT = (
    "Eres un asistente financiero. Analiza este informe y responde en español en 3 secciones:\n"
    "1) Resumen en 3 líneas. 2) Puntos clave. "
    "3) Posibles inconsistencias para revisar manualmente (no inventes datos).\n\n" + INFORME
)
 
print("Enviando el informe al modelo LOCAL (sin internet)...")   # aviso
datos = {"model": MODELO, "messages": [{"role": "user", "content": PROMPT}], "stream": False}
peticion = urllib.request.Request(   # arma la petición para Ollama
    URL, data=json.dumps(datos).encode("utf-8"), headers={"Content-Type": "application/json"})
abridor = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # sin proxy
inicio = time.perf_counter()   # marca la hora de inicio
try:   # intenta hablar con Ollama
    with abridor.open(peticion, timeout=180) as respuesta:   # envía la petición
        texto = json.loads(respuesta.read().decode("utf-8"))["message"]["content"]   # respuesta
except urllib.error.URLError:   # si Ollama no está activo...
    print("No se pudo conectar. Abre la aplicación Ollama o ejecuta: ollama serve")
    raise SystemExit(1)   # termina el programa
segundos = time.perf_counter() - inicio   # tiempo total
print("\n" + texto)   # muestra la respuesta del modelo
print(f"\nListo en {segundos:.1f} segundos. Ningún dato salió de esta computadora.")
