# agente_bucle.py
# Fase 2 (parte B): el agente con bucle de control while (pensar -> actuar -> observar -> repetir)
import json   # para identificar llamadas repetidas
from herramientas import ESQUEMAS, ejecutar   # el menú y el ejecutor seguro
from ollama_chat import chat, servicio_activo   # conexión con el modelo
 
MAX_PASOS = 8   # límite de pasos: evita bucles infinitos y gasto innecesario
MAX_REPETICIONES = 2   # cuántas veces se tolera repetir la misma acción
OBJETIVO_BASE = "¿Cuál de los archivos de ventas tiene el mayor total?"   # objetivo por defecto
SISTEMA = ("Eres un agente de oficina. Cumple el objetivo usando las herramientas, una a la vez. "
           "Si una herramienta devuelve ERROR, investiga con listar_archivos. "
           "No repitas llamadas. Cuando tengas la respuesta final, responde SIN llamar herramientas.")
 
 
def ejecutar_agente(objetivo):   # corre el bucle del agente; devuelve True si cumplió el objetivo
    mensajes = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": objetivo}]
    hechas = set()   # acciones ya realizadas
    repeticiones = 0   # contador de acciones repetidas
    paso = 0   # contador de pasos
    while paso < MAX_PASOS:   # BUCLE: mientras no se pase del límite de pasos
        paso += 1   # suma un paso
        print(f"\n--- PASO {paso} ---")
        try:   # intenta consultar al modelo
            mensaje = chat(mensajes, ESQUEMAS)   # PENSAR: el modelo decide qué hacer
        except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
            print(f"Error: {error}")
            return False   # no se cumplió el objetivo
        mensajes.append(mensaje)   # guarda lo que dijo el modelo (memoria de la conversación)
        llamadas = mensaje.get("tool_calls")   # ¿pidió usar herramientas?
        if not llamadas:   # si no pidió ninguna, tiene la respuesta final
            print(f"RESPUESTA FINAL: {mensaje.get('content', '')}")
            return True   # condición de finalización: objetivo cumplido
        for llamada in llamadas:   # ACTUAR: ejecuta cada herramienta pedida
            nombre = llamada["function"]["name"]   # nombre de la herramienta
            argumentos = llamada["function"]["arguments"]   # argumentos
            clave = (nombre, json.dumps(argumentos, sort_keys=True))   # identifica la acción
            if clave in hechas:   # si ya se hizo exactamente lo mismo...
                repeticiones += 1   # cuenta la repetición
                observacion = "AVISO: ya hiciste esta misma llamada. Usa otra o da la respuesta final."
            else:   # si es nueva...
                hechas.add(clave)   # la recuerda
                observacion = ejecutar(nombre, argumentos)   # ejecuta la herramienta
            print(f"Acción       : {nombre}({argumentos})")
            print(f"Observación  : {observacion}")   # OBSERVAR el resultado
            mensajes.append({"role": "tool", "tool_name": nombre, "content": observacion})
        if repeticiones >= MAX_REPETICIONES:   # si se repite demasiado...
            print("\nEl agente repite acciones sin avanzar: se detiene. Se necesita ayuda humana.")
            return False   # corta el bucle
    print("\nLímite de pasos alcanzado: se necesita ayuda humana.")
    return False   # no se cumplió el objetivo
 
 
def main():   # función principal
    print("=== AGENTE CON BUCLE DE CONTROL ===")   # título
    if not servicio_activo():   # si Ollama no responde...
        print("Ollama no responde. Abre la aplicación Ollama o ejecuta: ollama serve")
        return   # termina el programa
    objetivo = input(f"Objetivo (Enter = {OBJETIVO_BASE}): ").strip()   # pide el objetivo
    if objetivo == "":   # si no escribe nada...
        objetivo = OBJETIVO_BASE   # usa el objetivo por defecto
    cumplido = ejecutar_agente(objetivo)   # ejecuta el agente
    print("\nResultado:", "objetivo cumplido" if cumplido else "objetivo NO cumplido")
 
 
main()   # ejecuta el programa
