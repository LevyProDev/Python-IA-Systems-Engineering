# elegir_herramienta.py
# Fase 1: el modelo ELIGE la herramienta (el "menú del mayordomo")
from herramientas import ESQUEMAS, ejecutar   # el menú y el ejecutor seguro
from ollama_chat import chat, servicio_activo   # conexión con el modelo
 
SISTEMA = ("Eres un asistente de oficina. Elige la herramienta adecuada para el pedido del usuario. "
           "Si ninguna herramienta sirve, responde en una línea que no puedes ayudar con eso.")
 
 
def main():   # función principal
    print("=== EL MAYORDOMO ELIGE LA HERRAMIENTA ===")   # título
    if not servicio_activo():   # si Ollama no responde...
        print("Ollama no responde. Abre la aplicación Ollama o ejecuta: ollama serve")
        return   # termina el programa
    while True:   # repite hasta que el usuario escriba salir
        pedido = input("\n¿Qué necesitas? (salir para terminar): ").strip()   # pide el pedido
        if pedido.lower() == "salir":   # si escribe salir...
            print("Hasta pronto.")
            break   # sale del while
        if pedido == "":   # si no escribe nada...
            continue   # vuelve a preguntar
        mensajes = [{"role": "system", "content": SISTEMA}, {"role": "user", "content": pedido}]
        try:   # intenta consultar al modelo
            respuesta = chat(mensajes, ESQUEMAS)   # le enseña el menú de herramientas
        except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
            print(f"  Error: {error}")
            continue   # vuelve a preguntar
        llamadas = respuesta.get("tool_calls")   # ¿el modelo eligió herramientas?
        if not llamadas:   # si no eligió ninguna...
            print(f"  El modelo no eligió herramienta: {respuesta.get('content', '')}")
            continue   # vuelve a preguntar
        for llamada in llamadas:   # recorre cada herramienta elegida
            nombre = llamada["function"]["name"]   # nombre de la herramienta
            argumentos = llamada["function"]["arguments"]   # argumentos (diccionario)
            print(f"  Herramienta elegida: {nombre} {argumentos}")
            print("  Resultado:")
            for linea in ejecutar(nombre, argumentos).splitlines():   # ejecuta con controles
                print(f"    {linea}")   # muestra el resultado
 
 
main()   # ejecuta el programa
