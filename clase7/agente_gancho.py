# agente_gancho.py
# Gancho de la Clase 7: un agente que PIENSA, usa herramientas y se recupera solo
import csv                 # para leer archivos CSV
import json                # para enviar y leer datos en formato JSON
import urllib.request      # para enviar peticiones a Ollama
from pathlib import Path   # herramienta para trabajar con rutas de archivos
 
URL = "http://localhost:11434/api/chat"   # dirección LOCAL de Ollama
MODELO = "llama3.2:3b"   # modelo local
CARPETA = Path(__file__).parent / "demo"   # la única carpeta que el agente puede tocar
MAX_PASOS = 6   # límite de pasos: evita bucles infinitos
 
 
def listar_archivos():   # herramienta 1: lista los archivos de la carpeta
    return "Archivos: " + ", ".join(sorted(p.name for p in CARPETA.iterdir() if p.is_file()))
 
 
def total_ventas(nombre):   # herramienta 2: suma la columna monto de un CSV
    ruta = CARPETA / Path(nombre).name   # Path(...).name evita salir de la carpeta
    if not ruta.exists():   # si el archivo no existe...
        return f"ERROR: no existe el archivo {nombre}"   # devuelve el error como texto
    with open(ruta, encoding="utf-8", newline="") as archivo:   # abre el archivo
        total = sum(float(fila["monto"]) for fila in csv.DictReader(archivo))   # suma los montos
    return f"Total de {ruta.name}: Bs {total:,.2f}"
 
 
HERRAMIENTAS = {"listar_archivos": listar_archivos, "total_ventas": total_ventas}   # herramientas permitidas
ESQUEMAS = [   # el "menú" que se le muestra al modelo
    {"type": "function", "function": {
        "name": "listar_archivos", "description": "Lista los archivos disponibles.",
        "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {
        "name": "total_ventas", "description": "Suma los montos de un archivo CSV de ventas.",
        "parameters": {"type": "object", "required": ["nombre"],
                       "properties": {"nombre": {"type": "string", "description": "Nombre del archivo"}}}}},
]
SISTEMA = ("Eres un agente de oficina. Cumple el objetivo usando las herramientas, una a la vez. "
           "Si una herramienta devuelve ERROR, investiga con listar_archivos y vuelve a intentar. "
           "Cuando tengas la respuesta final, responde sin llamar herramientas.")
 
 
def pensar(mensajes):   # envía la conversación al modelo y devuelve su mensaje
    datos = {"model": MODELO, "messages": mensajes, "tools": ESQUEMAS, "stream": False,
             "options": {"temperature": 0}}   # temperatura 0 = más estable
    peticion = urllib.request.Request(
        URL, data=json.dumps(datos).encode("utf-8"), headers={"Content-Type": "application/json"})
    abridor = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # conexión directa, sin proxy
    with abridor.open(peticion, timeout=180) as respuesta:   # envía y espera
        return json.loads(respuesta.read().decode("utf-8"))["message"]   # mensaje del modelo
 
 
def main():   # función principal
    objetivo = "Calcula el total de ventas de enero."   # el objetivo del agente
    print(f"OBJETIVO: {objetivo}")
    mensajes = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": objetivo}]
    for paso in range(1, MAX_PASOS + 1):   # bucle con límite de pasos
        print(f"\n--- PASO {paso} ---")
        try:   # intenta hablar con el modelo
            mensaje = pensar(mensajes)   # PENSAR
        except OSError:   # si Ollama no está activo...
            print("No se pudo conectar con Ollama. Ábrelo y vuelve a intentar.")
            return   # termina el programa
        mensajes.append(mensaje)   # guarda lo que dijo el modelo
        llamadas = mensaje.get("tool_calls")   # ¿pidió usar herramientas?
        if not llamadas:   # si no pidió ninguna...
            print(f"RESPUESTA FINAL: {mensaje.get('content', '')}")   # esa es la respuesta final
            return   # terminó el objetivo
        for llamada in llamadas:   # ACTUAR: ejecuta cada herramienta pedida
            nombre = llamada["function"]["name"]   # nombre de la herramienta
            argumentos = llamada["function"]["arguments"]   # argumentos (un diccionario)
            funcion = HERRAMIENTAS.get(nombre)   # busca la herramienta en la lista permitida
            try:   # intenta ejecutarla
                resultado = funcion(**argumentos) if funcion else f"ERROR: herramienta '{nombre}' no permitida"
            except TypeError as error:   # si los argumentos no sirven...
                resultado = f"ERROR: argumentos incorrectos ({error})"
            print(f"Acción       : {nombre}({argumentos})")
            print(f"Observación  : {resultado}")   # OBSERVAR
            mensajes.append({"role": "tool", "tool_name": nombre, "content": str(resultado)})
    print("\nLímite de pasos alcanzado: se necesita ayuda humana.")
 
 
main()   # ejecuta el programa
