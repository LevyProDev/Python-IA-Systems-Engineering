"""Actúa como programador senior de Python 3.13. Estoy en un proyecto llamado clase5 y quiero conectar Python con Ollama, que corre en http://localhost:11434, usando solo módulos estándar (json, urllib), sin instalar librerías. Crea ollama_cliente.py con: servicio_activo(), modelos_instalados() (usa /api/tags) y consultar(prompt, sistema=None, temperatura=0.2) (usa /api/chat con stream false). Controla estos errores con mensajes claros en español: Ollama apagado, tiempo de espera agotado, error HTTP y respuesta con formato inesperado. La conexión debe ignorar proxies porque es local. Luego crea prueba_conexion.py que verifique el servicio, liste los modelos, confirme que existe el modelo llama3.2:3b y envíe una pregunta escrita por el usuario. Comenta el código línea por línea y explícame cómo funciona."""

# ollama_cliente.py
# Funciones para hablar con Ollama (el servicio local). Solo usa módulos que ya trae Python.
import json              # para convertir datos a JSON y leer respuestas JSON
import urllib.error      # tipos de error de conexión
import urllib.request    # para enviar peticiones HTTP
 
OLLAMA_URL = "http://localhost:11434"   # dirección local del servicio de Ollama
MODELO = "llama3.2:3b"                  # modelo que vamos a usar
TIEMPO_MAXIMO = 180                     # segundos máximos de espera por una respuesta
 
# Conexión directa, sin proxy: la comunicación es local y no sale de la computadora
ABRIDOR = urllib.request.build_opener(urllib.request.ProxyHandler({}))
 
 
def servicio_activo():   # revisa si Ollama está funcionando
    try:   # intenta conectarse
        with ABRIDOR.open(OLLAMA_URL, timeout=5) as respuesta:   # abre la dirección local
            return respuesta.status == 200   # True si respondió bien
    except (urllib.error.URLError, TimeoutError):   # si no se pudo conectar...
        return False   # el servicio no está activo
 
 
def _enviar(ruta, datos=None):   # envía una petición a Ollama y devuelve la respuesta en JSON
    url = f"{OLLAMA_URL}{ruta}"   # dirección completa
    if datos is None:   # si no hay datos que enviar...
        peticion = urllib.request.Request(url)   # petición simple (GET)
    else:   # si hay datos...
        cuerpo = json.dumps(datos).encode("utf-8")   # los convierte a JSON en bytes
        peticion = urllib.request.Request(   # petición con datos (POST)
            url, data=cuerpo, headers={"Content-Type": "application/json"})
    try:   # intenta enviar la petición
        with ABRIDOR.open(peticion, timeout=TIEMPO_MAXIMO) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))   # lee y convierte la respuesta
    except urllib.error.HTTPError as error:   # Ollama respondió con un error
        detalle = error.read().decode("utf-8", errors="replace")   # texto del error
        raise RuntimeError(f"Ollama respondió con error {error.code}: {detalle}") from error
    except urllib.error.URLError as error:   # no se pudo conectar
        raise ConnectionError(
            "No se pudo conectar con Ollama. Abre la aplicación Ollama o ejecuta: ollama serve"
        ) from error
    except TimeoutError as error:   # tardó demasiado
        raise TimeoutError(
            "El modelo tardó demasiado en responder. Prueba con un texto más corto."
        ) from error
    except json.JSONDecodeError as error:   # la respuesta no era JSON válido
        raise RuntimeError("Respuesta inesperada de Ollama (no es JSON válido).") from error
 
 
def modelos_instalados():   # devuelve la lista de modelos descargados
    datos = _enviar("/api/tags")   # pide la lista de modelos
    return [modelo["name"] for modelo in datos.get("models", [])]   # solo los nombres
 
 
def consultar(prompt, sistema=None, temperatura=0.2):   # envía una pregunta y devuelve el texto
    mensajes = []   # lista de mensajes de la conversación
    if sistema:   # si hay instrucciones de sistema...
        mensajes.append({"role": "system", "content": sistema})   # las agrega primero
    mensajes.append({"role": "user", "content": prompt})   # agrega la pregunta del usuario
    datos = {   # datos que se envían a Ollama
        "model": MODELO,   # modelo a usar
        "messages": mensajes,   # conversación
        "stream": False,   # pide la respuesta completa de una vez
        "options": {"temperature": temperatura},   # 0 = más preciso, 1 = más creativo
    }
    respuesta = _enviar("/api/chat", datos)   # envía la consulta
    try:   # intenta leer el texto de la respuesta
        return respuesta["message"]["content"]   # texto generado por el modelo
    except (KeyError, TypeError) as error:   # si la respuesta no tiene el formato esperado...
        raise RuntimeError("Respuesta inesperada de Ollama (formato desconocido).") from error
