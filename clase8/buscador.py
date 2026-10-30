# buscador.py
# Busca los fragmentos del documento más relacionados con una pregunta (por palabras clave)
import math                      # para calcular logaritmos
import unicodedata               # para ignorar tildes
from collections import Counter  # para contar palabras
 
PALABRAS_VACIAS = {   # palabras muy comunes que no ayudan a buscar
    "que", "como", "cual", "cuales", "cuanto", "cuantos", "cuanta", "del", "los", "las", "una", "uno",
    "con", "por", "para", "sobre", "donde", "este", "esta", "son", "hay", "dice", "documento", "segun",
    "tiene", "establece", "seria", "debe", "puede", "entre", "desde", "hasta", "sus", "les", "mas",
}
 
 
def palabras_clave(texto):   # convierte un texto en una lista de "raíces"
    texto = unicodedata.normalize("NFD", texto.lower())   # separa letras y tildes
    texto = texto.encode("ascii", "ignore").decode("ascii")   # quita tildes y símbolos raros
    palabras = "".join(c if c.isalnum() else " " for c in texto).split()   # separa por palabras
    palabras = [p for p in palabras if len(p) >= 3 and p not in PALABRAS_VACIAS]   # quita palabras comunes
    return [p.rstrip("s")[:7] for p in palabras]   # quita la "s" del plural y deja 7 letras (la "raíz")
 
 
def buscar(fragmentos, pregunta, cantidad=4):   # devuelve los fragmentos más relacionados con la pregunta
    consulta = set(palabras_clave(pregunta))   # raíces de la pregunta (sin repetir)
    if not consulta or not fragmentos:   # si no hay nada que buscar...
        return []
    conteos = [Counter(palabras_clave(f["texto"])) for f in fragmentos]   # palabras de cada fragmento
    total = len(fragmentos)   # cuántos fragmentos hay
    resultados = []   # lista de resultados
    for fragmento, conteo in zip(fragmentos, conteos):   # recorre cada fragmento
        puntaje = 0.0   # puntaje inicial
        for palabra in consulta:   # recorre cada palabra de la pregunta
            if conteo[palabra]:   # si el fragmento la contiene...
                en_cuantos = sum(1 for c in conteos if c[palabra])   # en cuántos fragmentos aparece
                rareza = math.log(1 + total / en_cuantos)   # palabras raras valen más
                puntaje += conteo[palabra] * rareza   # suma al puntaje
        if puntaje > 0:   # si tiene alguna coincidencia...
            resultados.append({**fragmento, "puntaje": round(puntaje, 2)})   # guarda con su puntaje
    resultados.sort(key=lambda r: r["puntaje"], reverse=True)   # ordena de mayor a menor
    return resultados[:cantidad]   # devuelve los mejores
