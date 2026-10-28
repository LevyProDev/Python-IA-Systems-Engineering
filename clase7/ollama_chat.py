# ollama_chat.py
# Conexión con Ollama para chat con herramientas. Solo usa módulos estándar de Python.
import json              # para convertir datos a JSON y leer respuestas JSON
import urllib.error      # tipos de error de conexión
import urllib.request    # para enviar peticiones HTTP
 
OLLAMA_URL = "http://localhost:11434"   # dirección local del servicio de Ollama
MODELO = "llama3.2:3b"   # modelo local (si falla con herramientas, prueba llama3.1:8b)
TIEMPO_MAXIMO = 180   # segundos máximos de espera
 
ABRIDOR = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # conexión directa, sin proxy
 
 
def servicio_activo():   # revisa si Ollama está funcionando
    try:   # intenta conectarse
        with ABRIDOR.open(OLLAMA_URL, timeout=5) as respuesta:   # abre la dirección local
            return respuesta.status == 200   # True si respondió bien
    except (urllib.error.URLError, TimeoutError):   # si no se pudo conectar...
        return False   # el servicio no está activo
 
 
def chat(mensajes, herramientas=None):   # envía la conversación y devuelve el mensaje del modelo
    datos = {"model": MODELO, "messages": mensajes, "stream": False,
             "options": {"temperature": 0}}   # temperatura 0 = más estable
    if herramientas:   # si hay herramientas...
        datos["tools"] = herramientas   # las incluye en la petición
    peticion = urllib.request.Request(   # arma la petición (POST)
        f"{OLLAMA_URL}/api/chat", data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:   # intenta enviar la petición
        with ABRIDOR.open(peticion, timeout=TIEMPO_MAXIMO) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))["message"]   # mensaje del modelo
    except urllib.error.HTTPError as error:   # Ollama respondió con un error
        raise RuntimeError(f"Ollama respondió con error {error.code}") from error
    except urllib.error.URLError as error:   # no se pudo conectar
        raise ConnectionError("No se pudo conectar con Ollama. Ábrelo o ejecuta: ollama serve") from error
    except TimeoutError as error:   # tardó demasiado
        raise TimeoutError("El modelo tardó demasiado en responder.") from error
    except (KeyError, json.JSONDecodeError) as error:   # formato inesperado
        raise RuntimeError("Respuesta inesperada de Ollama.") from error
