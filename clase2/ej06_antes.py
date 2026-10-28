# Registra las horas trabajadas
try:                                                     # intenta ejecutar este bloque
    horas = float(input("Horas trabajadas: "))           # pide las horas
    print("Registrado:", horas)                          # confirma el registro
except ValueError:                                       # si no era un número...
    print("Valor no válido. Cierra y vuelve a ejecutar.")   # el usuario debe empezar de nuevo
