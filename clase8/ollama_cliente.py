# ollama_cliente.py
# Conexión con Ollama (IA local). Solo usa módulos que ya trae Python.
import json              # para convertir datos a JSON y leer respuestas JSON
import urllib.error      # tipos de error de conexión
import urllib.request    # para enviar peticiones HTTP
 
OLLAMA_URL = "http://localhost:11434"   # dirección local del servicio de Ollama
MODELO = "llama3.2:3b"   # modelo que redacta las respuestas
TIEMPO_MAXIMO = 240   # segundos máximos de espera
 
ABRIDOR = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # conexión directa, sin proxy
 
 
def _enviar(ruta, datos=None):   # envía una petición a Ollama y devuelve la respuesta en JSON
    url = f"{OLLAMA_URL}{ruta}"   # dirección completa
    if datos is None:   # si no hay datos que enviar...
        peticion = urllib.request.Request(url)   # petición simple (GET)
    else:   # si hay datos...
        cuerpo = json.dumps(datos).encode("utf-8")   # los convierte a JSON en bytes
        peticion = urllib.request.Request(url, data=cuerpo, headers={"Content-Type": "application/json"})
    try:   # intenta enviar la petición
        with ABRIDOR.open(peticion, timeout=TIEMPO_MAXIMO) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))   # lee y convierte la respuesta
    except urllib.error.HTTPError as error:   # Ollama respondió con un error
        raise RuntimeError(f"Ollama respondió con error {error.code}. ¿Está descargado el modelo {MODELO}?") from error
    except urllib.error.URLError as error:   # no se pudo conectar
        raise ConnectionError("No se pudo conectar con Ollama. Ábrelo o ejecuta: ollama serve") from error
    except TimeoutError as error:   # tardó demasiado
        raise TimeoutError("El modelo tardó demasiado en responder. Prueba con un documento más corto.") from error
    except json.JSONDecodeError as error:   # la respuesta no era JSON válido
        raise RuntimeError("Respuesta inesperada de Ollama.") from error
 
 
def servicio_activo():   # revisa si Ollama está funcionando
    try:   # intenta conectarse
        with ABRIDOR.open(OLLAMA_URL, timeout=3) as respuesta:   # abre la dirección local
            return respuesta.status == 200   # True si respondió bien
    except (urllib.error.URLError, TimeoutError):   # si no se pudo conectar...
        return False   # el servicio no está activo
 
 
def modelo_instalado():   # True si el modelo está descargado
    try:   # intenta pedir la lista de modelos
        datos = _enviar("/api/tags")
    except (ConnectionError, TimeoutError, RuntimeError):   # si falla...
        return False
    return MODELO in [m["name"] for m in datos.get("models", [])]   # ¿está nuestro modelo en la lista?
 
 
def generar(prompt, sistema, temperatura=0.2):   # envía un prompt y devuelve el texto de la respuesta
    datos = {   # datos que se envían a Ollama
        "model": MODELO,
        "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": prompt}],
        "stream": False,   # pide la respuesta completa de una vez
        "options": {"temperature": temperatura},   # 0 = más preciso
    }
    respuesta = _enviar("/api/chat", datos)   # envía la consulta
    try:   # intenta leer el texto
        return respuesta["message"]["content"].strip()   # texto generado por el modelo
    except (KeyError, TypeError, AttributeError) as error:   # si el formato no es el esperado...
        raise RuntimeError("Respuesta inesperada de Ollama.") from error
