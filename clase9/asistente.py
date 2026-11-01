# asistente.py (versión con perfiles profesionales)
# Las dos funciones inteligentes: resumir un documento y responder preguntas sobre él
from buscador import buscar                  # búsqueda de fragmentos relacionados
from ollama_cliente import generar           # conexión con el modelo local
 
TAMANO_BLOQUE = 3500   # caracteres por bloque que se envían al modelo
MAX_BLOQUES = 8   # máximo de bloques a resumir (para no tardar demasiado)
 
 
def sistema_resumen(perfil):   # instrucciones fijas para resumir, según el perfil
    return (f"Eres {perfil['rol']} que resume documentos en español. {perfil['enfoque']} "
            "Usa SOLO el texto entregado, no inventes datos y no agregues opiniones.")
 
 
def sistema_preguntas(perfil):   # instrucciones fijas para responder preguntas, según el perfil
    return (f"Eres {perfil['rol']}. {perfil['enfoque']} Responde en español usando SOLO los fragmentos "
            "entregados. Si la respuesta no está en los fragmentos, responde exactamente: "
            "'No encontré esa información en el documento.' Cita las páginas con el formato (pág. N). "
            "No inventes datos.")
 
 
def formato_final(perfil):   # cómo debe verse el resumen final, según el perfil
    return ("Devuelve el resumen en Markdown con estas secciones:\n"
            "## Resumen\n(máximo 5 líneas)\n## Puntos principales\n(lista de máximo 7 puntos)\n"
            "## Datos clave\n(cifras, plazos y fechas que aparezcan)\n"
            f"## {perfil['extra_titulo']}\n{perfil['extra_detalle']}")
 
 
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
 
 
def resumir_documento(doc, perfil, progreso=None):   # genera el resumen de todo el documento
    bloques = armar_bloques(doc["paginas"])   # divide el documento en bloques
    usados = bloques[:MAX_BLOQUES]   # usa solo los primeros bloques si son demasiados
    sistema = sistema_resumen(perfil)   # instrucciones según el perfil
    if len(usados) == 1:   # si el documento cabe en un solo bloque...
        texto_final = usados[0]   # lo usa directamente
    else:   # si hay varios bloques: se resume cada uno y luego se juntan
        parciales = []   # resúmenes parciales
        for i, bloque in enumerate(usados, start=1):   # recorre cada bloque
            if progreso:   # si hay barra de progreso...
                progreso(i - 1, len(usados) + 1, f"Leyendo la parte {i} de {len(usados)}...")
            parciales.append(generar(f"Resume en 5 viñetas este fragmento:\n\n{bloque}", sistema, 0))
        texto_final = "\n\n".join(parciales)   # junta los resúmenes parciales
    if progreso:   # actualiza la barra
        progreso(len(usados), len(usados) + 1, "Redactando el resumen final...")
    resumen = generar(f"{formato_final(perfil)}\n\nTEXTO:\n{texto_final}", sistema, 0)   # resumen final
    if progreso:   # completa la barra
        progreso(len(usados) + 1, len(usados) + 1, "Listo")
    return {"texto": resumen, "bloques_usados": len(usados), "bloques_totales": len(bloques)}
 
 
def responder_pregunta(doc, pregunta, perfil):   # responde una pregunta usando solo el documento
    fragmentos = buscar(doc["fragmentos"], pregunta)   # busca los fragmentos relacionados
    if not fragmentos:   # si no encontró nada...
        return {"respuesta": "No encontré fragmentos relacionados con tu pregunta en el documento.",
                "fuentes": []}   # no gasta tiempo consultando a la IA
    contexto = "\n\n".join(f"[Página {f['pagina']}] {f['texto']}" for f in fragmentos)   # junta fragmentos
    prompt = f"FRAGMENTOS DEL DOCUMENTO:\n{contexto}\n\nPREGUNTA: {pregunta}"   # mensaje para el modelo
    respuesta = generar(prompt, sistema_preguntas(perfil), 0)   # el modelo redacta la respuesta
    return {"respuesta": respuesta, "fuentes": fragmentos}   # devuelve respuesta y fuentes
