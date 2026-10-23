# main.py - Asistente privado de documentos (Etapa 4: versión final, privada y verificada)
import csv                     # para leer archivos CSV
import re                      # para buscar patrones de texto
import sys                     # para leer opciones al ejecutar el programa
import time                    # para medir cuánto tarda cada respuesta
from datetime import datetime  # fecha y hora para los resultados
from pathlib import Path       # herramienta para trabajar con carpetas y archivos
from ollama_cliente import MODELO, consultar, modelos_instalados, servicio_activo   # conector
from privacidad import ejecutar_pruebas, registrar, verificar_privacidad   # privacidad
 
BASE = Path(__file__).parent   # carpeta donde está este programa
CARPETA_DOCS = BASE / "documentos"   # documentos de prueba
CARPETA_RESULTADOS = BASE / "resultados"   # aquí se guardan las respuestas
RUTA_CSV = CARPETA_DOCS / "movimientos_bancarios.csv"   # movimientos bancarios ficticios
MAX_CARACTERES = 12000   # límite de texto que enviaremos al modelo
 
SISTEMA = (   # instrucciones fijas para el modelo
    "Eres un asistente privado de análisis de documentos para una oficina. "
    "Responde en español, con claridad y SOLO con base en el documento entregado. "
    "Si un dato no aparece en el documento, dilo. No inventes cifras. "
    "Todo hallazgo es una sugerencia para revisión manual, no un hecho."
)
TAREAS = {   # clave -> (nombre, instrucción para el modelo)
    "resumen": ("Resumen ejecutivo",
                "Resume el documento en un máximo de 5 líneas para un directivo. "
                "Termina con una línea que empiece con 'Conclusión:'."),
    "puntos": ("Puntos importantes",
               "Devuelve una lista numerada de máximo 7 puntos, de una línea cada uno, "
               "ordenados de mayor a menor importancia."),
    "inconsistencias": ("Posibles inconsistencias",
                        "Revisa solo con base en el documento. Para cada inconsistencia indica: "
                        "1) qué dice el documento (cita breve), 2) por qué parece no concordar, "
                        "3) qué habría que verificar. No hagas cálculos largos: "
                        "indica qué cuentas verificar. "
                        "Si no encuentras ninguna, responde: 'No encontré inconsistencias'."),
    "libre": ("Pregunta libre", None),
}
MENU = {"1": "resumen", "2": "puntos", "3": "inconsistencias", "4": "libre"}   # opción -> tarea
 
 
def formatear_bs(valor):   # da formato de dinero: 80150 -> 80.150
    return f"{valor:,.0f}".replace(",", ".")
 
 
def listar_documentos():   # devuelve los documentos .md y .txt de la carpeta
    if not CARPETA_DOCS.exists():   # si la carpeta no existe...
        return []   # no hay documentos
    return sorted(p for p in CARPETA_DOCS.iterdir() if p.suffix.lower() in (".md", ".txt"))
 
 
def elegir_documento():   # muestra los documentos y devuelve el elegido (o None)
    documentos = listar_documentos()   # lista de documentos
    print("\nDocumentos disponibles:")   # encabezado
    for numero, documento in enumerate(documentos, start=1):   # numera cada documento
        print(f"  {numero}) {documento.name}")
    texto = input("Elige un documento (número): ").strip()   # pide el número
    if texto.isdigit() and 1 <= int(texto) <= len(documentos):   # si es un número válido...
        return documentos[int(texto) - 1]   # devuelve el documento elegido
    print("  Opción no válida.")   # si no, avisa
    return None   # no se eligió nada
 
 
def leer_documento(ruta):   # lee el texto y lo recorta si es muy largo
    texto = ruta.read_text(encoding="utf-8")   # lee el archivo
    if len(texto) > MAX_CARACTERES:   # si es demasiado largo...
        print(f"  Aviso: documento largo; se usarán los primeros {MAX_CARACTERES} caracteres.")
        texto = texto[:MAX_CARACTERES]   # lo recorta
    return texto   # devuelve el texto
 
 
def guardar_resultado(documento, clave, respuesta):   # guarda la respuesta en un archivo .md
    CARPETA_RESULTADOS.mkdir(exist_ok=True)   # crea la carpeta si no existe
    ahora = datetime.now()   # fecha y hora actuales
    nombre = f"{ahora:%Y-%m-%d_%H-%M}_{Path(documento).stem}_{clave}.md"   # nombre con fecha
    contenido = (   # contenido del archivo
        f"# Resultado: {TAREAS[clave][0]}\n\n"
        f"- Documento: {documento}\n- Fecha: {ahora:%Y-%m-%d %H:%M}\n- Modelo: {MODELO} (local)\n\n"
        f"{respuesta}\n\n> Verifica este resultado contra el documento original antes de decidir.\n"
    )
    (CARPETA_RESULTADOS / nombre).write_text(contenido, encoding="utf-8")   # guarda el archivo
    return nombre   # devuelve el nombre del archivo
 
 
def consultar_y_guardar(documento, clave, prompt):   # consulta, muestra, guarda y registra
    print(f"\nProcesando con el modelo local ({TAREAS[clave][0]})...")   # aviso
    inicio = time.perf_counter()   # marca la hora de inicio
    try:   # intenta consultar al modelo
        respuesta = consultar(prompt, sistema=SISTEMA, temperatura=0)   # 0 = más estable
    except (ConnectionError, TimeoutError, RuntimeError) as error:   # si algo falla...
        print(f"  Error: {error}")   # muestra el motivo
        return   # vuelve al menú
    segundos = time.perf_counter() - inicio   # tiempo total
    print("\n" + respuesta)   # muestra la respuesta
    print(f"\nGenerada en {segundos:.1f} s con {MODELO} (local).")   # rendimiento
    print(f"Resultado guardado: resultados/{guardar_resultado(documento, clave, respuesta)}")
    print("Recuerda: verifica este resultado con el documento original antes de decidir.")
    registrar(documento, TAREAS[clave][0], segundos)   # anota el uso (sin el contenido)
 
 
def procesar_documento(clave):   # ejecuta una tarea sobre un documento
    documento = elegir_documento()   # el usuario elige el documento
    if documento is None:   # si no eligió bien...
        return   # vuelve al menú
    instruccion = TAREAS[clave][1]   # instrucción de la tarea
    if instruccion is None:   # si es pregunta libre...
        instruccion = input("Escribe tu pregunta sobre el documento: ").strip()   # la pide
        if instruccion == "":   # si no escribió nada...
            print("  No escribiste ninguna pregunta.")
            return   # vuelve al menú
    texto = leer_documento(documento)   # lee el documento
    prompt = f"{instruccion}\n\n--- DOCUMENTO ---\n{texto}\n--- FIN DEL DOCUMENTO ---"   # prompt
    consultar_y_guardar(documento.name, clave, prompt)   # consulta y guarda
 
 
def leer_monto(texto, etiqueta):   # busca "Saldo final ...: Bs 82.150" y devuelve 82150
    coincidencia = re.search(rf"{etiqueta}[^\n]*?Bs\s*([\d\.]+)", texto)   # busca el monto
    if coincidencia is None:   # si no lo encuentra...
        return None
    return float(coincidencia.group(1).rstrip(".").replace(".", ""))   # quita puntos de miles
 
 
def leer_movimientos():   # suma ingresos y egresos del CSV
    ingresos = 0.0   # acumulador de ingresos
    egresos = 0.0   # acumulador de egresos
    with open(RUTA_CSV, encoding="utf-8", newline="") as archivo:   # abre el CSV
        for fila in csv.DictReader(archivo):   # recorre cada fila
            monto = float(fila["monto"])   # monto como número
            if fila["tipo"] == "ingreso":   # si es ingreso...
                ingresos += monto
            else:   # si es egreso...
                egresos += monto
    return ingresos, egresos   # devuelve los totales
 
 
def conciliar_movimientos():   # Python calcula; la IA explica
    try:   # intenta leer los archivos
        informe = (CARPETA_DOCS / "informe_financiero.md").read_text(encoding="utf-8")
        ingresos, egresos = leer_movimientos()   # totales del CSV
    except FileNotFoundError:   # si falta algún archivo...
        print("  Faltan archivos. Ejecuta crear_documentos_prueba.py")
        return   # vuelve al menú
    inicial = leer_monto(informe, "Saldo bancario inicial")   # saldo inicial del informe
    declarado = leer_monto(informe, "Saldo bancario final")   # saldo final declarado
    if inicial is None or declarado is None:   # si no encontró los saldos...
        print("  No encontré los saldos en el informe.")
        return   # vuelve al menú
    calculado = inicial + ingresos - egresos   # saldo que sale de los movimientos
    diferencia = declarado - calculado   # diferencia entre lo declarado y lo calculado
    tabla = (   # tabla calculada por Python (exacta)
        f"Saldo inicial (informe)   : Bs {formatear_bs(inicial)}\n"
        f"Ingresos (movimientos)    : Bs {formatear_bs(ingresos)}\n"
        f"Egresos (movimientos)     : Bs {formatear_bs(egresos)}\n"
        f"Saldo calculado           : Bs {formatear_bs(calculado)}\n"
        f"Saldo final declarado     : Bs {formatear_bs(declarado)}\n"
        f"Diferencia                : Bs {formatear_bs(diferencia)}"
    )
    print("\n--- CÁLCULO HECHO POR PYTHON ---\n" + tabla)   # muestra la tabla
    prompt = (   # prompt para que la IA explique
        "Datos calculados por Python (son exactos, no los recalcules):\n" + tabla +
        "\n\nExplica en máximo 4 líneas, para un gerente, qué significan estos datos. "
        "Si hay diferencia entre el saldo calculado y el declarado, indícalo como punto a revisar "
        "manualmente y sugiere 2 posibles causas."
    )
    consultar_y_guardar("movimientos_bancarios.csv", "resumen", prompt)   # consulta y guarda
 
 
def main():   # función principal
    if "--probar" in sys.argv:   # si se ejecuta con: python main.py --probar
        ejecutar_pruebas(CARPETA_DOCS)   # solo corre las pruebas del sistema
        return   # y termina
    print("=== ASISTENTE PRIVADO DE DOCUMENTOS (local) ===")   # título
    privado, mensaje = verificar_privacidad()   # revisa que todo sea local
    if not privado:   # si no es privado...
        print(f"BLOQUEADO: {mensaje}")
        return   # termina sin enviar nada
    print(mensaje)   # muestra la confirmación de privacidad
    try:   # intenta revisar el servicio y el modelo
        if not servicio_activo():   # si Ollama no responde...
            print("Ollama no responde. Abre la aplicación Ollama o ejecuta: ollama serve")
            return   # termina el programa
        if MODELO not in modelos_instalados():   # si falta el modelo...
            print(f"Falta el modelo {MODELO}. Descárgalo con: ollama pull {MODELO}")
            return   # termina el programa
    except (ConnectionError, RuntimeError) as error:   # si falla la revisión...
        print(f"Error: {error}")
        return   # termina el programa
    if not listar_documentos():   # si no hay documentos...
        print("No hay documentos. Ejecuta primero crear_documentos_prueba.py")
        return   # termina el programa
    while True:   # repite hasta que el usuario quiera salir
        print("\n1) Resumen  2) Puntos  3) Inconsistencias  4) Pregunta libre")
        print("5) Conciliar movimientos bancarios (Python calcula, la IA explica)  0) Salir")
        opcion = input("Elige una opción: ").strip()   # pide la opción
        if opcion == "0":   # si quiere salir...
            print("Hasta pronto.")
            break   # sale del while
        if opcion in MENU:   # si es una tarea sobre un documento...
            procesar_documento(MENU[opcion])   # la ejecuta
        elif opcion == "5":   # si es la conciliación...
            conciliar_movimientos()   # la ejecuta
        else:   # si no existe...
            print("  Opción no válida.")
 
 
main()   # ejecuta el programa
