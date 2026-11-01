# app.py (versión lista para despliegue)
# El Portal del Analista Inteligente: funciona en tu computadora y en la nube
import os                                  # para leer variables de entorno
import streamlit as st                     # librería para crear la aplicación web
import ollama_cliente as ia                # conexión con la IA (la usamos como "ia")
from asistente import resumir_documento, responder_pregunta   # funciones inteligentes
from buscador import buscar                # búsqueda de fragmentos
from lector_pdf import leer_pdf            # lector de PDF
from perfiles import PERFILES              # perfiles profesionales
 
st.set_page_config(   # configura la pestaña del navegador (SIEMPRE debe ser lo primero)
    page_title="Portal del Analista Inteligente", page_icon="📄",
    layout="wide", initial_sidebar_state="expanded")
 
 
def leer_config(nombre, defecto):   # lee un ajuste: primero variable de entorno, luego "secretos" de Streamlit
    valor = os.environ.get(nombre)   # ¿hay una variable de entorno con ese nombre?
    if valor:   # si existe...
        return valor
    try:   # si no, intenta leer los secretos de Streamlit (en la nube se configuran en el panel)
        return str(st.secrets[nombre])
    except Exception:   # si no hay secretos o no está ese ajuste...
        return defecto   # usa el valor por defecto
 
 
ia.configurar(leer_config("OLLAMA_URL", ia.OLLAMA_URL), leer_config("OLLAMA_MODELO", ia.MODELO))
PUBLICO = leer_config("MODO_PUBLICO", "no").strip().lower() == "si"   # ¿es la versión publicada en internet?
 
ESTILO = """
<style>
.hero {background: linear-gradient(90deg, #1F4E79, #2E75B6); padding: 1.4rem 1.8rem;
       border-radius: 14px; color: white; margin-bottom: 1rem;}
.hero h1 {color: white; margin: 0; font-size: 2rem; padding: 0;}
.hero p {margin: 0.3rem 0 0 0; opacity: 0.92;}
</style>
"""   # estilos visuales (CSS) para la cabecera
 
 
def cargar_documento(archivo):   # lee el PDF una sola vez y lo guarda en la "memoria de la sesión"
    clave = f"{archivo.name}-{archivo.size}"   # identifica el archivo (nombre y tamaño)
    if st.session_state.get("clave_doc") != clave:   # si es un archivo distinto al anterior...
        st.session_state["clave_doc"] = clave   # recuerda cuál es
        try:   # intenta leer el PDF
            st.session_state["doc"] = leer_pdf(archivo.getvalue(), archivo.name)   # lee el PDF
            st.session_state["error_doc"] = None   # no hubo error
            st.session_state["resumen"] = None   # borra el resumen anterior
            st.session_state["historial"] = []   # borra las preguntas anteriores
        except ValueError as error:   # si el PDF no se puede leer...
            st.session_state["doc"] = None   # no hay documento
            st.session_state["error_doc"] = str(error)   # guarda el mensaje para mostrarlo
    return st.session_state["doc"], st.session_state["error_doc"]   # devuelve el documento y el error
 
 
def mostrar_fuentes(fuentes):   # muestra los fragmentos consultados en una sección desplegable
    with st.expander("Ver los fragmentos consultados"):   # sección desplegable
        for fuente in fuentes:
            st.caption(f"Página {fuente['pagina']}")
            st.write(fuente["texto"])
 
 
activo = ia.servicio_activo()   # ¿Ollama está funcionando?
instalado = ia.modelo_instalado() if activo else False   # ¿está descargado el modelo?
ia_lista = activo and instalado   # la IA está lista solo si ambas cosas son ciertas
st.session_state.setdefault("historial", [])   # lista de preguntas hechas (vacía al inicio)
st.session_state.setdefault("resumen", None)   # resumen generado (ninguno al inicio)
 
st.markdown(ESTILO, unsafe_allow_html=True)   # aplica los estilos
if PUBLICO:   # texto de la cabecera según el modo
    subtitulo = "Versión pública de demostración: los archivos se procesan en un servidor en la nube."
else:
    subtitulo = "Asistente de documentos con IA local: tu PDF no sale de tu computadora."
st.markdown(f'<div class="hero"><h1>📄 Portal del Analista Inteligente</h1><p>{subtitulo}</p></div>',
            unsafe_allow_html=True)   # dibuja la cabecera
 
with st.sidebar:   # barra lateral
    st.header("Estado del sistema")
    if not activo:   # si la IA no responde...
        if PUBLICO:   # en la versión pública es lo normal
            st.info("Modo búsqueda: en esta versión pública no hay IA conectada. Puedes buscar fragmentos del documento.")
        else:   # en tu computadora es un problema
            st.error("Ollama: apagado. Ábrelo y recarga la página.")
    elif not instalado:   # si falta el modelo...
        st.warning(f"Falta el modelo. En la terminal: ollama pull {ia.MODELO}")
    else:   # si todo está bien...
        st.success(f"IA lista ({ia.MODELO})")
    if PUBLICO:   # aviso de privacidad de la versión pública
        st.warning("No subas documentos confidenciales ni datos personales a esta versión pública.")
    else:
        st.caption("Tus documentos se procesan en tu computadora.")
    st.header("Perfil profesional")
    nombre_perfil = st.selectbox("Adapta las instrucciones de la IA", list(PERFILES), key="perfil")
    perfil = PERFILES[nombre_perfil]   # datos del perfil elegido
    st.header("Cómo usarlo")
    st.markdown("1. Carga un PDF.\n2. Revisa su información.\n3. Resume o pregunta.")
 
archivo = st.file_uploader(   # zona para arrastrar o seleccionar un archivo
    "Arrastra tu PDF aquí o haz clic para buscarlo", type=["pdf"],
    help="Máximo 25 MB. Usa documentos de ejemplo o ficticios.")
 
doc = None   # documento leído (si lo hay)
error_doc = None   # mensaje de error (si lo hay)
if archivo is None:   # si no hay archivo...
    for clave in ("clave_doc", "doc", "error_doc"):   # borra lo que se recordaba
        st.session_state.pop(clave, None)
else:   # si hay archivo...
    doc, error_doc = cargar_documento(archivo)   # lo lee
 
tab_documento, tab_resumen, tab_preguntas = st.tabs(["📄 Documento", "📝 Resumen", "💬 Preguntas"])
 
with tab_documento:   # pestaña Documento
    if archivo is None:   # si no hay archivo...
        st.info("Sube un PDF para comenzar. Puedes usar uno de la carpeta documentos_prueba.")
    elif error_doc:   # si hubo un error al leerlo...
        st.error(error_doc)   # muestra el mensaje claro
    else:   # si se leyó bien...
        st.success(f"Documento cargado: {doc['nombre']}")
        col1, col2, col3 = st.columns(3)   # tres columnas
        col1.metric("Páginas", doc["n_paginas"])   # número de páginas
        col2.metric("Palabras", f"{doc['n_palabras']:,}".replace(",", "."))   # número de palabras
        col3.metric("Fragmentos", len(doc["fragmentos"]))   # número de fragmentos
        pagina = st.selectbox("Ver el texto de una página", range(1, doc["n_paginas"] + 1),
                              format_func=lambda n: f"Página {n}")   # lista desplegable de páginas
        st.text_area("Texto extraído", doc["paginas"][pagina - 1], height=220,
                     disabled=True, key=f"vista_{pagina}")   # muestra el texto de esa página
 
with tab_resumen:   # pestaña Resumen
    if doc is None:   # si no hay documento válido...
        st.info("Primero carga un PDF válido en la pestaña Documento.")
    elif not ia_lista:   # si la IA no está lista...
        st.info("El resumen con IA necesita un modelo conectado. En esta versión puedes usar la pestaña Preguntas "
                "en modo búsqueda.")
    else:   # si todo está listo...
        if st.button("Generar resumen", type="primary", key="btn_resumen"):   # botón principal
            barra = st.progress(0.0, text="Preparando...")   # barra de progreso
 
            def actualizar(hecho, total, texto):   # función que mueve la barra de progreso
                barra.progress(hecho / total, text=texto)
 
            try:   # intenta generar el resumen
                resultado = resumir_documento(doc, perfil, actualizar)   # genera el resumen
                resultado["perfil"] = nombre_perfil   # recuerda con qué perfil se generó
                st.session_state["resumen"] = resultado
            except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
                st.error(f"No se pudo generar el resumen: {error}")
            finally:   # pase lo que pase...
                barra.empty()   # quita la barra de progreso
        resumen = st.session_state.get("resumen")   # resumen guardado (si existe)
        if resumen:   # si ya hay un resumen...
            st.caption(f"Resumen generado con el perfil: {resumen['perfil']}")
            if resumen["bloques_usados"] < resumen["bloques_totales"]:   # si el documento era muy largo...
                st.warning("El documento es largo: el resumen cubre solo las primeras partes.")
            st.markdown(resumen["texto"])   # muestra el resumen
            st.download_button("⬇️ Descargar resumen (.md)", data=resumen["texto"],
                               file_name="resumen.md", mime="text/markdown")   # botón de descarga
            st.caption("Verifica siempre el resumen con el documento original antes de usarlo.")
 
with tab_preguntas:   # pestaña Preguntas
    if doc is None:   # si no hay documento válido...
        st.info("Primero carga un PDF válido en la pestaña Documento.")
    else:   # si hay documento...
        st.caption("Ejemplos: " + " · ".join(perfil["ejemplos"]))   # preguntas de ejemplo del perfil
        modo = "con IA" if ia_lista else "en modo búsqueda (sin IA)"   # cómo se va a responder
        pregunta = st.text_input(f"Escribe tu pregunta ({modo})",
                                 placeholder="Ejemplo: ¿Cuál es el plazo de pago?", key="pregunta")
        if st.button("Preguntar" if ia_lista else "Buscar", type="primary", key="btn_pregunta"):
            if not pregunta.strip():   # si no escribió nada...
                st.warning("Escribe una pregunta primero.")
            elif ia_lista:   # con IA...
                with st.spinner("Buscando en el documento y consultando a la IA..."):   # animación de espera
                    try:   # intenta responder
                        resultado = responder_pregunta(doc, pregunta.strip(), perfil)   # busca y responde
                        st.session_state["historial"].insert(0, {"pregunta": pregunta.strip(), **resultado})
                    except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
                        st.error(f"No se pudo responder: {error}")
            else:   # sin IA: solo muestra los fragmentos más relacionados
                fuentes = buscar(doc["fragmentos"], pregunta.strip())   # busca fragmentos
                texto = ("Fragmentos más relacionados (sin IA). Léelos para encontrar la respuesta."
                         if fuentes else "No encontré fragmentos relacionados con tu pregunta.")
                st.session_state["historial"].insert(0, {"pregunta": pregunta.strip(), "respuesta": texto,
                                                         "fuentes": fuentes})
        for item in st.session_state["historial"]:   # muestra las preguntas anteriores (la última primero)
            st.markdown(f"**🙋 {item['pregunta']}**")
            st.markdown(item["respuesta"])   # respuesta (de la IA o aviso de búsqueda)
            if item["fuentes"]:   # si hubo fragmentos consultados...
                mostrar_fuentes(item["fuentes"])
            st.divider()   # línea separadora
