# Portal del Analista Inteligente

Aplicación web hecha con **Python y Streamlit** que permite cargar un documento PDF,
revisar su contenido, generar resúmenes y hacer preguntas con ayuda de una IA local (Ollama).

## Qué puede hacer

- Cargar un PDF arrastrándolo a la pantalla (con validación de archivos).
- Mostrar páginas, palabras y el texto de cada página.
- Generar un resumen con IA y descargarlo.
- Responder preguntas citando las páginas consultadas.
- Adaptar las instrucciones de la IA a distintas profesiones (perfiles).

## Cómo ejecutarla en tu computadora

1. Instala las librerías: `python -m pip install -r requirements.txt`
2. (Opcional, para usar la IA) Instala Ollama y descarga el modelo: `ollama pull llama3.2:3b`
3. Crea los documentos de prueba: `python crear_documentos_prueba.py`
4. Inicia la aplicación: `python -m streamlit run app.py`

## Versión publicada en internet

En la nube no hay un Ollama disponible, por eso la versión pública funciona en **modo búsqueda**:
muestra los fragmentos del documento más relacionados con la pregunta, sin generar texto con IA.
No subas documentos confidenciales a la versión pública.

## Estructura

- `app.py`: interfaz web.
- `lector_pdf.py`: lectura y fragmentación del PDF.
- `buscador.py`: búsqueda de fragmentos por palabras clave.
- `ollama_cliente.py`: conexión con la IA local.
- `asistente.py`: resumen y respuestas.
- `perfiles.py`: perfiles profesionales.
- `crear_documentos_prueba.py`: crea PDF ficticios para probar.
- `verificar_despliegue.py`: comprueba que el proyecto esté listo para publicarse.

## Limitaciones

Los resultados de la IA pueden contener errores. Verifica siempre contra el documento original.
