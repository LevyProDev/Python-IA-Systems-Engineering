# prueba_conexion.py
# Etapa 1: comprobar que Python puede hablar con el modelo local
from ollama_cliente import MODELO, consultar, modelos_instalados, servicio_activo
 
 
def main():   # función principal
    print("=== PRUEBA DE CONEXIÓN CON OLLAMA ===")   # título
    if not servicio_activo():   # si Ollama no responde...
        print("Ollama no responde. Abre la aplicación Ollama o ejecuta: ollama serve")
        return   # termina el programa
    print("Servicio de Ollama: ACTIVO")   # todo bien
    modelos = modelos_instalados()   # lista de modelos descargados
    print("Modelos instalados:", ", ".join(modelos) if modelos else "ninguno")
    if MODELO not in modelos:   # si falta el modelo que usamos...
        print(f"Falta el modelo {MODELO}. Descárgalo con: ollama pull {MODELO}")
        return   # termina el programa
    pregunta = input("Escribe una pregunta de prueba: ").strip()   # pide una pregunta
    if pregunta == "":   # si no escribió nada...
        print("No escribiste ninguna pregunta.")
        return   # termina el programa
    print("Consultando al modelo local...")   # aviso de espera
    try:   # intenta consultar al modelo
        respuesta = consultar(pregunta)   # envía la pregunta
    except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
        print(f"Error: {error}")   # muestra el motivo
        return   # termina el programa
    print("\nRespuesta:")   # encabezado
    print(respuesta)   # muestra la respuesta del modelo
 
 
main()   # ejecuta el programa
