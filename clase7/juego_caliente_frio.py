# juego_caliente_frio.py
# Fase 2 (parte A): entender el bucle PENSAR -> ACTUAR -> OBSERVAR -> REPETIR con un juego
import random   # para elegir un número secreto
 
MAX_INTENTOS = 8   # límite de intentos (evita jugar para siempre)
 
 
def pista(distancia):   # convierte la distancia en una pista
    if distancia <= 5:   # muy cerca
        return "¡Muy caliente!"
    if distancia <= 15:   # cerca
        return "Caliente"
    if distancia <= 30:   # más o menos
        return "Tibio"
    return "Frío"   # lejos
 
 
def main():   # función principal
    secreto = random.randint(1, 100)   # número secreto entre 1 y 100
    intentos = 0   # contador de intentos
    print("Adivina el número secreto (1 a 100). ¡Te daré pistas!")   # instrucciones
    while intentos < MAX_INTENTOS:   # BUCLE: repite mientras queden intentos
        entrada = input(f"Intento {intentos + 1}/{MAX_INTENTOS}: ").strip()   # PENSAR + ACTUAR
        if not entrada.isdigit():   # si no es un número...
            print("  Escribe un número entero.")
            continue   # vuelve a preguntar (sin gastar intento)
        intentos += 1   # cuenta el intento
        numero = int(entrada)   # convierte el texto en número
        if numero == secreto:   # si acertó...
            print(f"  ¡Correcto! Lo lograste en {intentos} intentos.")
            return   # termina el juego (condición de finalización)
        print(f"  {pista(abs(numero - secreto))}")   # OBSERVAR: la pista; y se REPITE
    print(f"Se acabaron los intentos. El número era {secreto}.")   # si no acertó
 
 
main()   # ejecuta el programa
