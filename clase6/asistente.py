# asistente.py
# Etapa 3: asistente conversacional que responde preguntas sobre el PDF (RAG local)
from pathlib import Path             # herramienta para trabajar con rutas de archivos
import chromadb                      # base de datos vectorial local
from chromadb.config import Settings   # ajustes de ChromaDB
from ollama_api import MODELO_CHAT, crear_embeddings, responder, servicio_activo
 
CARPETA_DB = Path(__file__).parent / "memoria_vectorial"   # debe ser igual que en crear_memoria.py
NOMBRE_COLECCION = "manual_politicas"   # debe ser igual que en crear_memoria.py
N_RESULTADOS = 4   # cuántos fragmentos se recuperan por pregunta
 
SISTEMA = (   # instrucciones fijas para el modelo
    "Eres un asistente documental. Responde en español usando SOLO los fragmentos del documento "
    "que se entregan. Si la respuesta no aparece en los fragmentos, responde exactamente: "
    "'No encontré esa información en el documento.' Cita las páginas usadas con el formato (pág. N). "
    "No inventes datos."
)
 
 
def abrir_coleccion():   # abre la memoria vectorial creada en la Etapa 2
    cliente = chromadb.PersistentClient(   # abre la base en disco
        path=str(CARPETA_DB), settings=Settings(anonymized_telemetry=False))
    return cliente.get_collection(NOMBRE_COLECCION)   # devuelve la colección
 
 
def buscar(coleccion, pregunta):   # busca los fragmentos más parecidos a la pregunta
    vector = crear_embeddings([pregunta], prefijo="search_query: ")[0]   # convierte la pregunta en vector
    resultado = coleccion.query(query_embeddings=[vector], n_results=N_RESULTADOS)   # busca por parecido
    fragmentos = []   # lista de resultados
    for texto, meta, distancia in zip(   # recorre los resultados de la primera (y única) consulta
            resultado["documents"][0], resultado["metadatas"][0], resultado["distances"][0]):
        fragmentos.append({"texto": texto, "pagina": meta["pagina"], "distancia": distancia})
    return fragmentos   # devuelve la lista
 
 
def armar_prompt(pregunta, fragmentos):   # junta los fragmentos y la pregunta en un solo mensaje
    contexto = "\n\n".join(f"[Página {f['pagina']}] {f['texto']}" for f in fragmentos)   # fragmentos
    return f"FRAGMENTOS DEL DOCUMENTO:\n{contexto}\n\nPREGUNTA: {pregunta}"   # mensaje final
 
 
def main():   # función principal
    print("=== ASISTENTE DOCUMENTAL LOCAL ===")   # título
    if not servicio_activo():   # si Ollama no responde...
        print("Ollama no responde. Abre la aplicación Ollama o ejecuta: ollama serve")
        return   # termina el programa
    try:   # intenta abrir la memoria
        coleccion = abrir_coleccion()   # abre la colección
    except Exception:   # si no existe la memoria...
        print("No existe la memoria vectorial. Ejecuta primero: python crear_memoria.py")
        return   # termina el programa
    print(f"Memoria cargada: {coleccion.count()} fragmentos. Modelo: {MODELO_CHAT}")
    print("Escribe tu pregunta. Comandos: /fuentes (ver fragmentos usados) y salir.")
    ultimos = []   # fragmentos de la última pregunta
    while True:   # repite hasta que el usuario escriba salir
        pregunta = input("\nTu pregunta: ").strip()   # pide la pregunta
        if pregunta.lower() == "salir":   # si escribe salir...
            print("Hasta pronto.")
            break   # sale del while
        if pregunta == "":   # si no escribe nada...
            continue   # vuelve a preguntar
        if pregunta == "/fuentes":   # si pide ver las fuentes...
            if not ultimos:   # si todavía no hay ninguna...
                print("  Aún no hiciste ninguna pregunta.")
            for f in ultimos:   # muestra cada fragmento usado
                print(f"  [Página {f['pagina']}] (distancia {f['distancia']:.2f}) {f['texto'][:150]}...")
            continue   # vuelve a preguntar
        try:   # intenta buscar y responder
            ultimos = buscar(coleccion, pregunta)   # busca fragmentos relacionados
            respuesta = responder(armar_prompt(pregunta, ultimos), SISTEMA)   # el modelo redacta
        except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
            print(f"  Error: {error}")
            continue   # vuelve a preguntar
        print("\nRespuesta:\n" + respuesta)   # muestra la respuesta
        paginas = sorted({f["pagina"] for f in ultimos})   # páginas consultadas, sin repetir
        print(f"\nPáginas consultadas: {', '.join(str(p) for p in paginas)}")
        print("(Verifica siempre en el PDF. Escribe /fuentes para ver los fragmentos.)")
 
 
if __name__ == "__main__":   # solo ejecuta main() si abrimos ESTE archivo directamente
    main()
