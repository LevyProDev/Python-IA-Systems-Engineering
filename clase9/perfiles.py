# perfiles.py
# Perfiles profesionales: cambian las instrucciones que recibe la IA y las preguntas de ejemplo.
# Para adaptar la aplicación a una profesión, solo hay que agregar un perfil en este diccionario.
 
PERFILES = {
    "General": {   # perfil por defecto
        "rol": "un asistente documental profesional",   # quién es la IA
        "enfoque": "Responde de forma clara, neutral y ordenada.",   # cómo debe responder
        "extra_titulo": "Puntos a revisar manualmente",   # sección extra del resumen
        "extra_detalle": "(algo ambiguo o que requiera revisión; si no hay, escribe 'Ninguno evidente')",
        "ejemplos": [   # preguntas de ejemplo que se muestran en pantalla
            "¿Cuál es el tema principal del documento?",
            "¿Qué fechas o plazos se mencionan?",
        ],
    },
}
