"""Mejora el proyecto como un ingeniero senior con enfoque en privacidad. 1) Crea privacidad.py con: host_es_local() (la dirección de Ollama debe ser localhost, 127.0.0.1 o ::1), modelo_es_local() (rechaza modelos cuyo nombre contenga “cloud”), verificar_privacidad() que devuelva si es seguro y un mensaje, registrar() que anote fecha, modelo, documento, tarea y segundos en registro.log SIN guardar el contenido de los documentos, y ejecutar_pruebas() que muestre OK o FALLA para cada comprobación. 2) Actualiza main.py para que bloquee la ejecución si la verificación de privacidad falla, muestre el tiempo de cada respuesta, registre cada uso y permita ejecutar “python main.py --probar”. Comenta el código línea por línea."""
# privacidad.py
# Etapa 4: comprobaciones de privacidad, registro de uso y pruebas del sistema
from datetime import datetime         # fecha y hora para el registro
from pathlib import Path              # herramienta para trabajar con carpetas y archivos
from urllib.parse import urlparse     # para leer la dirección del servicio
from ollama_cliente import MODELO, OLLAMA_URL, modelos_instalados, servicio_activo
 
REGISTRO = Path(__file__).parent / "registro.log"   # archivo con el historial de uso
HOSTS_LOCALES = ("localhost", "127.0.0.1", "::1")   # direcciones que significan "esta computadora"
 
 
def host_es_local(url=OLLAMA_URL):   # True si la dirección apunta a esta computadora
    return urlparse(url).hostname in HOSTS_LOCALES
 
 
def modelo_es_local(modelo=MODELO):   # True si el modelo no parece de la nube
    return "cloud" not in modelo.lower()   # los modelos "cloud" no se ejecutan en tu equipo
 
 
def verificar_privacidad():   # devuelve (ok, mensaje)
    if not host_es_local():   # si la dirección no es local...
        return False, f"La dirección {OLLAMA_URL} no es local. El programa no enviará documentos."
    if not modelo_es_local():   # si el modelo parece de la nube...
        return False, f"El modelo {MODELO} parece ser un modelo en la nube. Usa un modelo local."
    return True, f"Procesamiento local: {OLLAMA_URL} · modelo {MODELO}"   # todo bien
 
 
def registrar(documento, tarea, segundos):   # anota el uso (sin el contenido del documento)
    ahora = datetime.now()   # fecha y hora actuales
    with open(REGISTRO, "a", encoding="utf-8") as archivo:   # "a" = agregar al final
        linea = f"{ahora:%Y-%m-%d %H:%M} | {MODELO} | {documento} | {tarea} | {segundos:.1f}s"
        archivo.write(linea + "\n")
 
 
def ejecutar_pruebas(carpeta_docs):   # revisa que todo esté en orden; devuelve True si pasa todo
    print("=== PRUEBAS DEL SISTEMA ===")   # título
    activo = servicio_activo()   # ¿Ollama responde?
    instalado = False   # ¿está el modelo?
    if activo:   # solo revisa modelos si el servicio responde
        try:   # intenta leer la lista de modelos
            instalado = MODELO in modelos_instalados()
        except (ConnectionError, RuntimeError):   # si falla...
            instalado = False
    hay_docs = carpeta_docs.exists() and any(carpeta_docs.iterdir())   # ¿hay documentos?
    pruebas = [   # (nombre de la prueba, resultado)
        ("Dirección del servicio es local", host_es_local()),
        ("Modelo no es de la nube", modelo_es_local()),
        ("Ollama está activo", activo),
        (f"Modelo {MODELO} instalado", instalado),
        ("Carpeta documentos con archivos", hay_docs),
    ]
    for nombre, resultado in pruebas:   # muestra cada prueba
        print(f"  [{'OK' if resultado else 'FALLA'}] {nombre}")
    todo_bien = all(resultado for _, resultado in pruebas)   # ¿pasaron todas?
    print("Resultado:", "todo en orden" if todo_bien else "hay pruebas que fallaron")
    return todo_bien
