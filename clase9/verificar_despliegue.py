# verificar_despliegue.py
# Valida que todos los archivos y configuraciones estén listos antes de subir a GitHub y desplegar.

from pathlib import Path

def verificar():
    print("=== VERIFICACIÓN ANTES DE DESPLEGAR ===\n")
    
    raiz = Path(__file__).parent
    checks = 0
    total = 11

    # 1. Existe app.py
    if (raiz / "app.py").is_file():
        print("  [OK] Existe app.py")
        checks += 1
    else:
        print("  [X] Falta app.py")

    # 2. Existe README.md
    if (raiz / "README.md").is_file():
        print("  [OK] Existe README.md")
        checks += 1
    else:
        print("  [X] Falta README.md")

    # 3. Existe requirements.txt
    req_path = raiz / "requirements.txt"
    if req_path.is_file():
        print("  [OK] Existe requirements.txt")
        checks += 1
        req_texto = req_path.read_text(encoding="utf-8").lower()
    else:
        print("  [X] Falta requirements.txt")
        req_texto = ""

    # 4. Librería 'pypdf' declarada
    if "pypdf" in req_texto:
        print("  [OK] Librería 'pypdf' declarada en requirements.txt")
        checks += 1
    else:
        print("  [X] Falta declarar 'pypdf' en requirements.txt")

    # 5. Librería 'streamlit' declarada
    if "streamlit" in req_texto:
        print("  [OK] Librería 'streamlit' declarada en requirements.txt")
        checks += 1
    else:
        print("  [X] Falta declarar 'streamlit' en requirements.txt")

    # 6. Existe .gitignore
    gitignore_path = raiz / ".gitignore"
    if gitignore_path.is_file():
        print("  [OK] Existe .gitignore")
        checks += 1
        git_texto = gitignore_path.read_text(encoding="utf-8")
    else:
        print("  [X] Falta .gitignore")
        git_texto = ""

    # 7. .gitignore ignora __pycache__
    if "__pycache__" in git_texto:
        print("  [OK] .gitignore ignora __pycache__")
        checks += 1
    else:
        print("  [X] .gitignore no incluye __pycache__")

    # 8. .gitignore ignora .venv
    if ".venv" in git_texto or "venv" in git_texto:
        print("  [OK] .gitignore ignora .venv")
        checks += 1
    else:
        print("  [X] .gitignore no incluye .venv")

    # 9. .gitignore ignora .streamlit/secrets.toml
    if "secrets.toml" in git_texto:
        print("  [OK] .gitignore ignora .streamlit/secrets.toml")
        checks += 1
    else:
        print("  [X] .gitignore no incluye secrets.toml")

    # 10. .gitignore ignora .env
    if ".env" in git_texto:
        print("  [OK] .gitignore ignora .env")
        checks += 1
    else:
        print("  [X] .gitignore no incluye .env")

    # 11. No hay rutas absolutas del computador en el código (ej. C:/Users o /home/)
    rutas_absolutas = False
    for archivo_py in raiz.glob("*.py"):
        if archivo_py.name == "verificar_despliegue.py":
            continue
        contenido = archivo_py.read_text(encoding="utf-8", errors="ignore")
        if "C:\\" in contenido or "C:/" in contenido or "/home/" in contenido or "/Users/" in contenido:
            rutas_absolutas = True
            break

    if not rutas_absolutas:
        print("  [OK] No hay rutas absolutas del computador en el código")
        checks += 1
    else:
        print("  [X] Se detectaron rutas absolutas en el código")

    print(f"\nResultado: {checks} de {total} comprobaciones correctas\n")
    
    if checks == total:
        print("Listo para subir a GitHub y desplegar.")
    else:
        print("Revisa los errores antes de continuar.")

if __name__ == "__main__":
    verificar()