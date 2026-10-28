# ollama_api.py
# Funciones para hablar con Ollama (servicio local). Solo usa módulos que ya trae Python.
import json              # para convertir datos a JSON y leer respuestas JSON
import urllib.error      # tipos de error de conexión
import urllib.request    # para enviar peticiones HTTP
 
OLLAMA_URL = "http://localhost:11434"   # dirección local del servicio de Ollama
MODELO_CHAT = "llama3.2:3b"             # modelo que redacta las respuestas
MODELO_EMBEDDING = "nomic-embed-text"   # modelo que convierte textos en números (embeddings)
TIEMPO_MAXIMO = 180                     # segundos máximos de espera
 
ABRIDOR = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # conexión directa, sin proxy
 
 
def llamar_ollama(ruta, datos=None):   # envía una petición a Ollama y devuelve la respuesta en JSON
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
        raise TimeoutError("Ollama tardó demasiado en responder.") from error
    except json.JSONDecodeError as error:   # la respuesta no era JSON válido
        raise RuntimeError("Respuesta inesperada de Ollama (no es JSON válido).") from error
 
 
def servicio_activo():   # revisa si Ollama está funcionando
    try:   # intenta conectarse
        with ABRIDOR.open(OLLAMA_URL, timeout=5) as respuesta:   # abre la dirección local
            return respuesta.status == 200   # True si respondió bien
    except (urllib.error.URLError, TimeoutError):   # si no se pudo conectar...
        return False   # el servicio no está activo
 
 
def modelos_instalados():   # devuelve la lista de modelos descargados
    datos = llamar_ollama("/api/tags")   # pide la lista de modelos
    return [modelo["name"] for modelo in datos.get("models", [])]   # solo los nombres
 
 
def modelo_disponible(nombre, instalados):   # True si el modelo está descargado
    return nombre in instalados or f"{nombre}:latest" in instalados   # acepta el sufijo ":latest"
 
 
def crear_embeddings(textos, prefijo=""):   # convierte una lista de textos en una lista de vectores
    datos = {"model": MODELO_EMBEDDING, "input": [prefijo + texto for texto in textos]}   # petición
    respuesta = llamar_ollama("/api/embed", datos)   # envía los textos
    try:   # intenta leer los vectores
        return respuesta["embeddings"]   # lista de vectores (uno por texto)
    except (KeyError, TypeError) as error:   # si el formato no es el esperado...
        raise RuntimeError("Respuesta inesperada de Ollama (embeddings).") from error
 
 
def responder(prompt, sistema):   # pide al modelo de chat que redacte una respuesta
    datos = {   # datos que se envían a Ollama
        "model": MODELO_CHAT,   # modelo de chat
        "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": prompt}],
        "stream": False,   # pide la respuesta completa de una vez
        "options": {"temperature": 0},   # 0 = respuestas más estables y precisas
    }
    respuesta = llamar_ollama("/api/chat", datos)   # envía la consulta
    try:   # intenta leer el texto
        return respuesta["message"]["content"]   # texto generado por el modelo
    except (KeyError, TypeError) as error:   # si el formato no es el esperado...
        raise RuntimeError("Respuesta inesperada de Ollama (chat).") from error
