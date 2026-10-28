# crear_memoria.py
# Etapa 2: guardar los fragmentos en una memoria vectorial local (ChromaDB)
import time                          # para medir cuánto tarda
from pathlib import Path             # herramienta para trabajar con rutas de archivos
import chromadb                      # base de datos vectorial local
from chromadb.config import Settings   # ajustes de ChromaDB
from leer_pdf import PDF, extraer_fragmentos   # reutilizamos lo que hicimos en la Etapa 1
from ollama_api import (MODELO_EMBEDDING, crear_embeddings, modelo_disponible,
                        modelos_instalados, servicio_activo)
 
CARPETA_DB = Path(__file__).parent / "memoria_vectorial"   # carpeta donde se guarda la memoria
NOMBRE_COLECCION = "manual_politicas"   # nombre de nuestra "colección" (como una carpeta de fichas)
LOTE = 16   # cuántos fragmentos se convierten a la vez
 
 
def main():   # función principal
    print("=== CREAR MEMORIA VECTORIAL ===")   # título
    if not PDF.exists():   # si falta el PDF...
        print("No se encontró el PDF. Ejecuta primero: python crear_pdf_prueba.py")
        return   # termina el programa
    if not servicio_activo():   # si Ollama no responde...
        print("Ollama no responde. Abre la aplicación Ollama o ejecuta: ollama serve")
        return   # termina el programa
    try:   # intenta revisar los modelos
        instalados = modelos_instalados()   # modelos descargados
    except (ConnectionError, RuntimeError) as error:   # si falla...
        print(f"Error: {error}")
        return   # termina el programa
    if not modelo_disponible(MODELO_EMBEDDING, instalados):   # si falta el modelo de embeddings...
        print(f"Falta el modelo {MODELO_EMBEDDING}. Descárgalo con: ollama pull {MODELO_EMBEDDING}")
        return   # termina el programa
    paginas, fragmentos = extraer_fragmentos()   # lee el PDF y lo divide (Etapa 1)
    print(f"PDF leído: {paginas} páginas, {len(fragmentos)} fragmentos")
    cliente = chromadb.PersistentClient(   # abre (o crea) la base en disco
        path=str(CARPETA_DB), settings=Settings(anonymized_telemetry=False))   # sin estadísticas de uso
    try:   # intenta borrar una colección anterior
        cliente.delete_collection(NOMBRE_COLECCION)   # empezamos desde cero
    except Exception:   # si no existía, no pasa nada
        pass
    coleccion = cliente.create_collection(NOMBRE_COLECCION)   # crea la colección vacía
    inicio = time.perf_counter()   # marca la hora de inicio
    for desde in range(0, len(fragmentos), LOTE):   # recorre los fragmentos de 16 en 16
        lote = fragmentos[desde:desde + LOTE]   # el grupo actual
        try:   # intenta convertir el grupo en vectores
            vectores = crear_embeddings([f["texto"] for f in lote], prefijo="search_document: ")
        except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
            print(f"Error: {error}")
            return   # termina el programa
        coleccion.add(   # guarda el grupo en la memoria
            ids=[f"frag-{desde + i}" for i in range(len(lote))],   # un identificador único por fragmento
            documents=[f["texto"] for f in lote],   # el texto
            embeddings=vectores,   # los vectores calculados por Ollama
            metadatas=[{"pagina": f["pagina"]} for f in lote],   # la página de cada fragmento
        )
        print(f"  Guardados {min(desde + LOTE, len(fragmentos))} de {len(fragmentos)} fragmentos")
    segundos = time.perf_counter() - inicio   # tiempo total
    print(f"Memoria lista: {coleccion.count()} fragmentos guardados en {segundos:.1f} s")
    print(f"Carpeta: {CARPETA_DB.name}")
 
 
if __name__ == "__main__":   # solo ejecuta main() si abrimos ESTE archivo directamente
    main()
