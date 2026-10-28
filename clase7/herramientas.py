# herramientas.py
# Las "herramientas" que el agente puede usar: funciones de Python con permisos limitados
import csv                 # para leer archivos CSV
from pathlib import Path   # herramienta para trabajar con rutas de archivos
 
CARPETA_DATOS = Path(__file__).parent / "datos"   # la ÚNICA carpeta que las herramientas pueden tocar
 
 
def ruta_segura(nombre):   # convierte un nombre en una ruta dentro de datos (y nada más)
    ruta = (CARPETA_DATOS / nombre).resolve()   # ruta completa y real
    if ruta.parent != CARPETA_DATOS.resolve():   # si el archivo no está directamente en datos...
        raise ValueError("ruta fuera de la carpeta permitida")   # lo rechaza
    return ruta   # devuelve la ruta segura
 
 
def limpiar_monto(texto):   # convierte "Bs 350" o "350" en el número 350.0
    return float(texto.replace("Bs", "").replace(" ", "").strip())
 
 
def listar_archivos():   # herramienta: lista los archivos de datos
    if not CARPETA_DATOS.exists():   # si no existe la carpeta...
        return "ERROR: no existe la carpeta datos"
    nombres = sorted(p.name for p in CARPETA_DATOS.iterdir() if p.is_file())   # nombres ordenados
    return "Archivos: " + ", ".join(nombres) if nombres else "La carpeta datos está vacía"
 
 
def leer_archivo(nombre):   # herramienta: muestra las primeras líneas de un archivo
    ruta = ruta_segura(nombre)   # valida la ruta
    if not ruta.exists():   # si no existe...
        return f"ERROR: no existe el archivo {nombre}"
    return "\n".join(ruta.read_text(encoding="utf-8").splitlines()[:10])   # primeras 10 líneas
 
 
def total_ventas(nombre):   # herramienta: suma la columna monto de un CSV
    ruta = ruta_segura(nombre)   # valida la ruta
    if not ruta.exists():   # si no existe...
        return f"ERROR: no existe el archivo {nombre}"
    total = 0.0   # acumulador
    with open(ruta, encoding="utf-8", newline="") as archivo:   # abre el CSV
        for fila in csv.DictReader(archivo):   # recorre cada venta
            total += limpiar_monto(fila["monto"])   # suma el monto (acepta "Bs 350")
    return f"Total de {nombre}: Bs {total:,.2f}"
 
 
HERRAMIENTAS = {   # lista BLANCA: solo estas funciones se pueden ejecutar
    "listar_archivos": listar_archivos,
    "leer_archivo": leer_archivo,
    "total_ventas": total_ventas,
}
 
ESQUEMAS = [   # el "menú" en JSON que se le muestra al modelo
    {"type": "function", "function": {
        "name": "listar_archivos",
        "description": "Lista los archivos disponibles en la carpeta de datos.",
        "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {
        "name": "leer_archivo",
        "description": "Muestra las primeras líneas de un archivo de texto o CSV.",
        "parameters": {"type": "object", "required": ["nombre"],
                       "properties": {"nombre": {"type": "string", "description": "Ejemplo: notas.txt"}}}}},
    {"type": "function", "function": {
        "name": "total_ventas",
        "description": "Suma los montos de un archivo CSV de ventas.",
        "parameters": {"type": "object", "required": ["nombre"],
                       "properties": {"nombre": {"type": "string", "description": "Ejemplo: ventas_enero.csv"}}}}},
]
 
 
def ejecutar(nombre, argumentos):   # ejecuta una herramienta pedida por el modelo, con controles
    funcion = HERRAMIENTAS.get(nombre)   # busca la herramienta en la lista blanca
    if funcion is None:   # si no existe...
        validas = ", ".join(HERRAMIENTAS)   # nombres de herramientas válidas
        return f"ERROR: la herramienta '{nombre}' no existe. Válidas: {validas}"
    if not isinstance(argumentos, dict):   # si los argumentos no son un diccionario...
        return "ERROR: argumentos inválidos"
    try:   # intenta ejecutar la herramienta
        return str(funcion(**argumentos))   # ejecuta con los argumentos del modelo
    except TypeError as error:   # argumentos que no corresponden a la función
        return f"ERROR: argumentos incorrectos ({error})"
    except (OSError, ValueError, KeyError) as error:   # problemas con archivos o datos
        return f"ERROR: {error}"
