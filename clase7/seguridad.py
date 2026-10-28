# seguridad.py
# Controles de seguridad para el código que escribe el agente (filtro básico, NO es un sandbox perfecto)
import ast          # para analizar el código sin ejecutarlo
import subprocess   # para ejecutar el script en un proceso aparte
import sys          # para usar el mismo Python que estamos usando
 
IMPORTS_PERMITIDOS = {"csv", "pathlib", "re", "statistics", "decimal", "json", "datetime", "math"}
LLAMADAS_PROHIBIDAS = {"eval", "exec", "compile", "__import__", "input", "breakpoint"}
ATRIBUTOS_PROHIBIDOS = {"write_text", "write_bytes", "unlink", "rmdir", "rename", "mkdir", "touch",
                        "chmod", "symlink_to", "hardlink_to", "system", "popen", "Popen", "rmtree"}
 
 
def revisar_codigo(codigo):   # devuelve una lista de problemas (vacía = pasa el filtro)
    try:   # intenta analizar el código
        arbol = ast.parse(codigo)   # convierte el texto en un árbol de instrucciones
    except SyntaxError as error:   # si tiene errores de sintaxis...
        return [f"error de sintaxis: {error.msg} (línea {error.lineno})"]
    problemas = []   # lista de problemas encontrados
    for nodo in ast.walk(arbol):   # recorre TODAS las instrucciones del código
        if isinstance(nodo, ast.Import):   # import xxx
            for alias in nodo.names:
                if alias.name.split(".")[0] not in IMPORTS_PERMITIDOS:
                    problemas.append(f"import no permitido: {alias.name}")
        elif isinstance(nodo, ast.ImportFrom):   # from xxx import yyy
            if (nodo.module or "").split(".")[0] not in IMPORTS_PERMITIDOS:
                problemas.append(f"import no permitido: {nodo.module}")
        elif isinstance(nodo, ast.Call):   # una llamada a función
            if isinstance(nodo.func, ast.Name) and nodo.func.id in LLAMADAS_PROHIBIDAS:
                problemas.append(f"llamada prohibida: {nodo.func.id}()")
            es_open = (isinstance(nodo.func, ast.Name) and nodo.func.id == "open") or (
                isinstance(nodo.func, ast.Attribute) and nodo.func.attr == "open")   # open() o ruta.open()
            if es_open:   # solo se permite abrir para LEER
                modo = nodo.args[1] if len(nodo.args) > 1 else None   # segundo argumento = modo
                for palabra in nodo.keywords:   # o el argumento mode=...
                    if palabra.arg == "mode":
                        modo = palabra.value
                if isinstance(modo, ast.Constant) and any(c in str(modo.value) for c in "wax+"):
                    problemas.append("open() en modo de escritura no permitido")
            if (isinstance(nodo.func, ast.Attribute) and nodo.func.attr == "replace"
                    and len(nodo.args) == 1 and not nodo.keywords):   # Path.replace(x) mueve archivos
                problemas.append("Path.replace() puede mover archivos")   # (str.replace usa 2 argumentos)
        elif isinstance(nodo, ast.Attribute):   # algo.atributo
            if nodo.attr in ATRIBUTOS_PROHIBIDOS or nodo.attr.startswith("__"):
                problemas.append(f"atributo prohibido: .{nodo.attr}")
        elif isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):   # textos
            if ".." in nodo.value or nodo.value.startswith(("/", "\\")) or ":\\" in nodo.value:
                problemas.append(f"ruta sospechosa: {nodo.value!r}")
    return problemas   # lista final
 
 
def ejecutar_script(ruta, carpeta_trabajo, tiempo=20):   # ejecuta el script y devuelve (código, salida, error)
    try:   # intenta ejecutarlo
        resultado = subprocess.run(   # lanza un proceso de Python aparte
            [sys.executable, "-I", str(ruta)],   # -I = modo aislado
            cwd=carpeta_trabajo, capture_output=True, text=True, encoding="utf-8", timeout=tiempo)
    except subprocess.TimeoutExpired:   # si tarda demasiado...
        return 1, "", f"TimeoutError: el script superó {tiempo} segundos"
    return resultado.returncode, resultado.stdout, resultado.stderr   # código, salida y errores
