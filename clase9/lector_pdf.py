# lector_pdf.py
# Lee un PDF, extrae su texto y lo divide en fragmentos. No usa Streamlit: es lógica pura de Python.
import io                        # para leer el PDF desde la memoria
from pypdf import PdfReader      # librería para leer PDF
 
MAX_MB = 25   # tamaño máximo permitido (en megabytes)
TAMANO_FRAGMENTO = 900   # caracteres por fragmento
SOLAPAMIENTO = 150   # caracteres que se repiten entre fragmentos vecinos
 
 
def dividir_texto(texto):   # corta un texto largo en fragmentos pequeños
    fragmentos = []   # lista de fragmentos
    inicio = 0   # posición donde empieza el fragmento actual
    while inicio < len(texto):   # mientras queden caracteres...
        fin = inicio + TAMANO_FRAGMENTO   # posición final del fragmento
        trozo = texto[inicio:fin].strip()   # corta el fragmento
        if trozo:   # si no está vacío...
            fragmentos.append(trozo)   # lo guarda
        if fin >= len(texto):   # si llegamos al final...
            break   # termina
        inicio = fin - SOLAPAMIENTO   # el siguiente empieza un poco antes
    return fragmentos   # devuelve la lista
 
 
def leer_pdf(datos, nombre):   # lee el PDF y devuelve un diccionario con su información
    if not nombre.lower().endswith(".pdf"):   # si no termina en .pdf...
        raise ValueError("El archivo debe ser un PDF (.pdf).")
    if len(datos) > MAX_MB * 1024 * 1024:   # si pesa demasiado...
        raise ValueError(f"El archivo pesa {len(datos) / 1024 / 1024:.1f} MB; el máximo es {MAX_MB} MB.")
    try:   # intenta abrir el PDF
        lector = PdfReader(io.BytesIO(datos))   # abre el PDF desde la memoria
        if lector.is_encrypted and lector.decrypt("") == 0:   # si está protegido con contraseña...
            raise ValueError("El PDF está protegido con contraseña. Quita la protección e inténtalo de nuevo.")
        paginas = []   # texto de cada página
        for pagina in lector.pages:   # recorre cada página
            paginas.append(" ".join((pagina.extract_text() or "").split()))   # extrae y limpia el texto
    except ValueError:   # nuestros propios avisos se dejan pasar
        raise
    except Exception as error:   # cualquier otro problema al abrir o leer el PDF
        raise ValueError("No se pudo leer el PDF: parece dañado o no es un PDF válido.") from error
    if not any(paginas):   # si ninguna página tiene texto...
        raise ValueError("El PDF no tiene texto legible. Puede ser un documento escaneado (necesitaría OCR).")
    fragmentos = []   # fragmentos de todo el documento
    for numero, texto in enumerate(paginas, start=1):   # recorre las páginas (desde la 1)
        for trozo in dividir_texto(texto):   # divide el texto de la página
            fragmentos.append({"pagina": numero, "texto": trozo})   # guarda página y texto
    return {   # información del documento
        "nombre": nombre,
        "paginas": paginas,   # lista con el texto de cada página
        "n_paginas": len(paginas),
        "n_palabras": sum(len(p.split()) for p in paginas),
        "fragmentos": fragmentos,
    }
