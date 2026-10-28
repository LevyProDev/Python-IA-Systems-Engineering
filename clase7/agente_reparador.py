# agente_reparador.py
# Fase 3: el agente ejecuta un script, lee el error, pide una corrección al modelo y reintenta
import re                      # para buscar patrones de texto
from pathlib import Path       # herramienta para trabajar con rutas de archivos
from herramientas import CARPETA_DATOS, limpiar_monto   # carpeta de datos y montos
from ollama_chat import chat, servicio_activo   # conexión con el modelo
from seguridad import ejecutar_script, revisar_codigo   # controles de seguridad
 
BASE = Path(__file__).parent   # carpeta del proyecto (clase7)
SCRIPT_ORIGINAL = BASE / "scripts" / "resumen_ventas.py"   # script con errores
MAX_INTENTOS = 3   # límite de reparaciones antes de pedir ayuda humana
PEDIR_CONFIRMACION = True   # True = pregunta antes de ejecutar código escrito por la IA
 
SISTEMA = (   # instrucciones fijas para el modelo
    "Eres un asistente que corrige scripts de Python 3.13. Responde SOLO con el script completo corregido "
    "dentro de un bloque ```python. Usa solo los módulos csv, pathlib, re, statistics, decimal, json, "
    "datetime y math. No uses input(), no escribas, borres ni renombres archivos."
)
 
 
def muestra_de_datos():   # devuelve las primeras líneas de cada CSV (contexto para el modelo)
    partes = []   # lista de textos
    for archivo in sorted(CARPETA_DATOS.glob("ventas_*.csv")):   # recorre los CSV de ventas
        lineas = archivo.read_text(encoding="utf-8").splitlines()[:4]   # primeras 4 líneas
        partes.append(f"{archivo.name}:\n" + "\n".join(lineas))
    return "\n\n".join(partes)   # todo junto
 
 
def total_esperado():   # calcula el total con un método independiente (para verificar al agente)
    total = 0.0   # acumulador
    for archivo in CARPETA_DATOS.glob("ventas_*.csv"):   # recorre los CSV de ventas
        for linea in archivo.read_text(encoding="utf-8").splitlines()[1:]:   # salta el encabezado
            total += limpiar_monto(linea.split(",")[2])   # suma la tercera columna (monto)
    return total   # total esperado
 
 
def verificar(salida):   # comprueba si la salida cumple el objetivo
    coincidencia = re.search(r"TOTAL GENERAL: Bs ([\d,\.]+)", salida)   # busca la línea del total
    if coincidencia is None:   # si no aparece...
        return False, "no aparece la línea 'TOTAL GENERAL'"
    obtenido = float(coincidencia.group(1).replace(",", ""))   # total que calculó el script
    esperado = total_esperado()   # total calculado de forma independiente
    if abs(obtenido - esperado) > 0.01:   # si no coinciden...
        return False, f"el total {obtenido:,.2f} no coincide con el esperado {esperado:,.2f}"
    return True, f"el total {obtenido:,.2f} coincide con el cálculo independiente"
 
 
def extraer_codigo(texto):   # saca el código del bloque ```python de la respuesta del modelo
    coincidencia = re.search(r"```(?:python)?\n(.*?)```", texto, re.S)   # busca el bloque
    return coincidencia.group(1).strip() + "\n" if coincidencia else None
 
 
def pedir_correccion(codigo, error):   # pide al modelo el script corregido
    prompt = (   # mensaje para el modelo
        "OBJETIVO: el script debe imprimir el subtotal de cada archivo ventas_*.csv de la carpeta datos "
        "y una última línea 'TOTAL GENERAL: Bs X'.\n\n"
        f"SCRIPT ACTUAL:\n```python\n{codigo}```\n\n"
        f"ERROR AL EJECUTARLO (Traceback):\n{error[-1200:]}\n\n"
        f"MUESTRA DE LOS DATOS:\n{muestra_de_datos()}\n\n"
        "Explica nada: devuelve solo el script corregido completo."
    )
    respuesta = chat([{"role": "system", "content": SISTEMA}, {"role": "user", "content": prompt}])
    return extraer_codigo(respuesta.get("content", ""))   # devuelve solo el código
 
 
def mostrar_error(error):   # muestra DÓNDE y QUÉ error ocurrió (lo que aprendimos en la Clase 2)
    lineas = error.strip().splitlines()   # líneas del Traceback
    ubicacion = next((l.strip() for l in reversed(lineas) if l.strip().startswith("File")), "")
    print(f"    Dónde: {ubicacion}")   # archivo y número de línea
    print(f"    Qué  : {lineas[-1] if lineas else 'sin mensaje'}")   # tipo y mensaje del error
 
 
def ejecutar_y_verificar(ruta):   # ejecuta un script y comprueba si cumple el objetivo
    codigo_salida, salida, error = ejecutar_script(ruta, BASE)   # EJECUTAR
    if codigo_salida != 0:   # si falló...
        print("  FALLÓ:")
        mostrar_error(error)   # OBSERVAR el error
        return False, error   # no se cumplió el objetivo
    print(salida.rstrip())   # muestra lo que imprimió
    correcto, motivo = verificar(salida)   # VERIFICAR el resultado
    print(f"  Verificación: {motivo}")
    return correcto, f"El script no falló, pero {motivo}."   # éxito o error de verificación
 
 
def main():   # función principal
    print("=== AGENTE AUTO-REPARADOR ===")   # título
    if not servicio_activo():   # si Ollama no responde...
        print("Ollama no responde. Abre la aplicación Ollama o ejecuta: ollama serve")
        return   # termina el programa
    if not SCRIPT_ORIGINAL.exists():   # si falta el script...
        print("Falta scripts/resumen_ventas.py. Ejecuta primero crear_datos_prueba.py")
        return   # termina el programa
    print("OBJETIVO: obtener el resumen de ventas sin errores y con el total correcto.")
    print(f"\n[Ejecutando el script original: {SCRIPT_ORIGINAL.name}]")
    correcto, error = ejecutar_y_verificar(SCRIPT_ORIGINAL)   # intento 0: el script original
    if correcto:   # si ya funcionaba...
        print("\nOBJETIVO CUMPLIDO sin necesidad de reparar.")
        return   # termina: éxito
    ruta = SCRIPT_ORIGINAL   # script que vamos a corregir
    for intento in range(1, MAX_INTENTOS + 1):   # BUCLE: máximo 3 reparaciones
        print(f"\n[Reparación {intento} de {MAX_INTENTOS}] Pidiendo una corrección al modelo local...")
        try:   # intenta consultar al modelo
            nuevo = pedir_correccion(ruta.read_text(encoding="utf-8"), error)   # DECIDIR
        except (ConnectionError, TimeoutError, RuntimeError) as problema:   # si algo falla...
            print(f"  Error: {problema}")
            break   # deja de intentar
        if nuevo is None:   # si no devolvió código...
            print("  El modelo no devolvió un bloque de código.")
            continue   # pasa al siguiente intento
        problemas = revisar_codigo(nuevo)   # CONTROL DE SEGURIDAD
        if problemas:   # si el código no pasa el filtro...
            print("  Código RECHAZADO por seguridad: " + "; ".join(problemas))
            continue   # no lo ejecuta; pasa al siguiente intento
        print("  Código propuesto:")
        for linea in nuevo.splitlines():   # muestra el código
            print(f"    | {linea}")
        if PEDIR_CONFIRMACION:   # si hay que pedir permiso...
            if input("  ¿Ejecutar este código corregido? (si/no): ").strip().lower() != "si":
                print("  Cancelado por el usuario.")
                return   # termina sin ejecutar
        ruta = BASE / "scripts" / f"resumen_ventas_v{intento}.py"   # nunca pisa el original
        ruta.write_text(nuevo, encoding="utf-8")   # guarda la versión nueva
        print(f"\n[Ejecutando la versión reparada: {ruta.name}]")
        correcto, error = ejecutar_y_verificar(ruta)   # EJECUTAR y VERIFICAR
        if correcto:   # si cumplió el objetivo...
            print(f"\nOBJETIVO CUMPLIDO con {ruta.name} (reparaciones: {intento}).")
            return   # termina: éxito
    print(f"\nNO SE PUDO REPARAR en {MAX_INTENTOS} intentos. Se necesita intervención humana.")
    print("Revisa la carpeta scripts y el último error mostrado.")
 
 
main()   # ejecuta el programa
