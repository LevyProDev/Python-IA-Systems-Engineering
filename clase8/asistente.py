# asistente.py
# Las dos funciones inteligentes: resumir un documento y responder preguntas sobre él
from buscador import buscar                  # búsqueda de fragmentos relacionados
from ollama_cliente import generar           # conexión con el modelo local
 
TAMANO_BLOQUE = 3500   # caracteres por bloque que se envían al modelo
MAX_BLOQUES = 8   # máximo de bloques a resumir (para no tardar demasiado)
 
SISTEMA_RESUMEN = (   # instrucciones fijas para resumir
    "Eres un asistente que resume documentos profesionales en español. Usa SOLO el texto entregado, "
    "no inventes datos y no agregues opiniones."
)
SISTEMA_PREGUNTAS = (   # instrucciones fijas para responder preguntas
    "Eres un asistente documental. Responde en español usando SOLO los fragmentos entregados. "
    "Si la respuesta no está en los fragmentos, responde exactamente: "
    "'No encontré esa información en el documento.' Cita las páginas con el formato (pág. N). No inventes datos."
)
FORMATO_FINAL = (   # cómo debe verse el resumen final
    "Devuelve el resumen en Markdown con estas secciones:\n"
    "## Resumen\n(máximo 5 líneas)\n## Puntos principales\n(lista de máximo 7 puntos)\n"
    "## Datos clave\n(cifras, plazos y fechas que aparezcan)\n"
    "## Puntos a revisar manualmente\n(algo ambiguo; si no hay, escribe 'Ninguno evidente')"
)
 
 
def armar_bloques(paginas):   # junta las páginas en bloques de tamaño razonable
    bloques = []   # lista de bloques
    actual = ""   # bloque que se está armando
    for numero, texto in enumerate(paginas, start=1):   # recorre las páginas
        linea = f"[Página {numero}] {texto}\n"   # texto con el número de página
        if actual and len(actual) + len(linea) > TAMANO_BLOQUE:   # si el bloque ya está lleno...
            bloques.append(actual)   # lo guarda
            actual = ""   # empieza uno nuevo
        actual += linea   # agrega la página al bloque
    if actual:   # si quedó un bloque a medias...
        bloques.append(actual)   # lo guarda
    return bloques   # devuelve la lista
 
 
def resumir_documento(doc, progreso=None):   # genera el resumen de todo el documento
    bloques = armar_bloques(doc["paginas"])   # divide el documento en bloques
    usados = bloques[:MAX_BLOQUES]   # usa solo los primeros bloques si son demasiados
    if len(usados) == 1:   # si el documento cabe en un solo bloque...
        texto_final = usados[0]   # lo usa directamente
    else:   # si hay varios bloques: se resume cada uno y luego se juntan
        parciales = []   # resúmenes parciales
        for i, bloque in enumerate(usados, start=1):   # recorre cada bloque
            if progreso:   # si hay barra de progreso...
                progreso(i - 1, len(usados) + 1, f"Leyendo la parte {i} de {len(usados)}...")
            parciales.append(generar(f"Resume en 5 viñetas este fragmento:\n\n{bloque}", SISTEMA_RESUMEN, 0))
        texto_final = "\n\n".join(parciales)   # junta los resúmenes parciales
    if progreso:   # actualiza la barra
        progreso(len(usados), len(usados) + 1, "Redactando el resumen final...")
    resumen = generar(f"{FORMATO_FINAL}\n\nTEXTO:\n{texto_final}", SISTEMA_RESUMEN, 0)   # resumen final
    if progreso:   # completa la barra
        progreso(len(usados) + 1, len(usados) + 1, "Listo")
    return {"texto": resumen, "bloques_usados": len(usados), "bloques_totales": len(bloques)}
 
 
def responder_pregunta(doc, pregunta):   # responde una pregunta usando solo el documento
    fragmentos = buscar(doc["fragmentos"], pregunta)   # busca los fragmentos relacionados
    if not fragmentos:   # si no encontró nada...
        return {"respuesta": "No encontré fragmentos relacionados con tu pregunta en el documento.",
                "fuentes": []}   # no gasta tiempo consultando a la IA
    contexto = "\n\n".join(f"[Página {f['pagina']}] {f['texto']}" for f in fragmentos)   # junta los fragmentos
    prompt = f"FRAGMENTOS DEL DOCUMENTO:\n{contexto}\n\nPREGUNTA: {pregunta}"   # mensaje para el modelo
    respuesta = generar(prompt, SISTEMA_PREGUNTAS, 0)   # el modelo redacta la respuesta
    return {"respuesta": respuesta, "fuentes": fragmentos}   # devuelve respuesta y fuentes
