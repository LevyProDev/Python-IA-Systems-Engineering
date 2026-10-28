# leer_pdf.py
# Etapa 1: leer el PDF y dividirlo en fragmentos (chunks)
from pathlib import Path       # herramienta para trabajar con rutas de archivos
from pypdf import PdfReader    # librería para leer PDF
 
PDF = Path(__file__).parent / "manual_politicas_2026.pdf"   # PDF que vamos a leer
TAMANO_CHUNK = 400   # cuántos caracteres tiene cada fragmento
SOLAPAMIENTO = 80    # cuántos caracteres se repiten entre fragmentos vecinos
 
 
def dividir_texto(texto):   # corta un texto largo en fragmentos pequeños
    texto = " ".join(texto.split())   # quita saltos de línea y espacios repetidos
    fragmentos = []   # lista donde guardaremos los fragmentos
    inicio = 0   # posición donde empieza el fragmento actual
    while inicio < len(texto):   # mientras queden caracteres por cortar...
        fin = inicio + TAMANO_CHUNK   # posición donde termina este fragmento
        fragmento = texto[inicio:fin].strip()   # corta el fragmento
        if fragmento:   # si no está vacío...
            fragmentos.append(fragmento)   # lo guarda
        if fin >= len(texto):   # si ya llegamos al final del texto...
            break   # termina
        inicio = fin - SOLAPAMIENTO   # el siguiente empieza un poco antes (solapamiento)
    return fragmentos   # devuelve la lista
 
 
def extraer_fragmentos(ruta=PDF):   # lee el PDF y devuelve (número de páginas, fragmentos)
    lector = PdfReader(str(ruta))   # abre el PDF
    fragmentos = []   # lista de fragmentos de todo el PDF
    for numero, pagina in enumerate(lector.pages, start=1):   # recorre cada página (desde la 1)
        texto = pagina.extract_text() or ""   # extrae el texto de la página
        for trozo in dividir_texto(texto):   # divide el texto de la página
            fragmentos.append({"pagina": numero, "texto": trozo})   # guarda página y texto
    return len(lector.pages), fragmentos   # devuelve el resultado
 
 
def main():   # función principal
    if not PDF.exists():   # si no existe el PDF...
        print("No se encontró el PDF. Ejecuta primero: python crear_pdf_prueba.py")
        return   # termina el programa
    try:   # intenta leer el PDF
        paginas, fragmentos = extraer_fragmentos()   # lee y divide
    except Exception as error:   # si el PDF está dañado o no se puede leer...
        print(f"No se pudo leer el PDF: {error}")
        return   # termina el programa
    print("=== LECTURA DEL PDF ===")   # título
    print(f"Páginas leídas     : {paginas}")
    print(f"Fragmentos creados : {len(fragmentos)}")
    if not fragmentos:   # si no hay texto...
        print("El PDF no tiene texto legible (¿es una imagen escaneada? Necesitaría OCR).")
        return   # termina el programa
    print("\nEjemplo del primer fragmento:")
    print(fragmentos[0]["texto"])
    while True:   # repite hasta que el usuario pulse Enter
        entrada = input("\nNúmero de página a mostrar (Enter para terminar): ").strip()   # pide la página
        if entrada == "":   # si no escribe nada...
            break   # sale del while
        if not entrada.isdigit() or not 1 <= int(entrada) <= paginas:   # si no es válida...
            print(f"  Escribe un número entre 1 y {paginas}.")
            continue   # vuelve a preguntar
        for fragmento in fragmentos:   # recorre todos los fragmentos
            if fragmento["pagina"] == int(entrada):   # si es de la página pedida...
                print(f"  [Página {fragmento['pagina']}] {fragmento['texto']}")
 
 
if __name__ == "__main__":   # solo ejecuta main() si abrimos ESTE archivo directamente
    main()
