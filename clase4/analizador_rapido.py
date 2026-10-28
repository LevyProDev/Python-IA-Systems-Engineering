"""Actúa como analista de datos y programador senior de Python 3.13. Soy profesional de oficina y quiero ver el poder de Pandas en pocos segundos. Crea un script que: 1) genere un archivo ficticio ventas_demo.csv con 40 ventas (fecha, producto, región, cantidad, precio) con errores a propósito: 2 filas duplicadas, 2 cantidades vacías y regiones mal escritas; 2) lo cargue con Pandas; 3) lo limpie (duplicados, vacíos y texto de la región); 4) cree la columna total y calcule las ventas por región; 5) dibuje un gráfico de barras por región y una línea por mes; 6) exporte la tabla limpia a Excel. Nivel básico-intermedio, comentado línea por línea."""
# analizador_rapido.py
# Gancho de la Clase 4: de una tabla desordenada a un informe en segundos
import matplotlib.pyplot as plt   # librería para hacer gráficos
import pandas as pd               # librería para analizar datos
 
# ---------- 1) Crear datos ficticios (con errores a propósito) ----------
productos = {"Laptop": 5200, "Monitor": 1400, "Teclado": 150, "Mouse": 90}   # producto: precio
nombres = list(productos)                      # lista con los nombres de productos
regiones = ["La Paz", "Cochabamba", "Santa Cruz"]   # regiones de venta
filas = []                                     # aquí guardaremos cada venta
for i in range(40):                            # 40 ventas
    producto = nombres[i % 4]                  # el producto va rotando
    filas.append({
        "fecha": f"2026-{i % 6 + 1:02d}-{i % 27 + 1:02d}",   # fecha en texto
        "producto": producto,
        "region": regiones[i % 3],             # la región va rotando
        "cantidad": None if i in (8, 29) else 1 + (i * 3) % 7,   # 2 cantidades vacías
        "precio": productos[producto],
    })
df = pd.DataFrame(filas)                       # convierte la lista en una tabla
df.loc[4, "region"] = " la paz "               # ERROR: espacios y minúsculas
df.loc[10, "region"] = "SANTA CRUZ"            # ERROR: todo en mayúsculas
df = pd.concat([df, df.iloc[[0, 1]]], ignore_index=True)   # ERROR: 2 filas duplicadas
df.to_csv("ventas_demo.csv", index=False)      # guarda la tabla en un archivo CSV
print(f"Archivo creado: ventas_demo.csv ({len(df)} filas)")
 
# ---------- 2) Cargar el archivo ----------
datos = pd.read_csv("ventas_demo.csv", parse_dates=["fecha"])   # lee el CSV y convierte fechas
print(f"Archivo cargado: {datos.shape[0]} filas y {datos.shape[1]} columnas")
 
# ---------- 3) Limpiar ----------
antes = len(datos)                             # filas antes de limpiar
datos = datos.drop_duplicates()                # elimina filas duplicadas
datos = datos.dropna(subset=["cantidad"])      # elimina ventas sin cantidad
datos["region"] = datos["region"].str.strip().str.title()   # arregla espacios y mayúsculas
datos["total"] = datos["cantidad"] * datos["precio"]        # nueva columna: total de cada venta
print(f"Limpieza: {antes} filas -> {len(datos)} filas")
 
# ---------- 4) Resumen ----------
por_region = datos.groupby("region")["total"].sum().sort_values(ascending=False)   # por región
print(f"Ventas totales: Bs {datos['total'].sum():,.0f}")
print("Ventas por región:")
for region, valor in por_region.items():   # recorre cada región
    print(f"  {region:<12} Bs {valor:>9,.0f}")   # muestra región y total
 
# ---------- 5) Gráfico e informe ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))   # una figura con 2 gráficos
por_region.plot(kind="bar", ax=ax1, title="Ventas por región (Bs)")   # barras por región
por_mes = datos.groupby(datos["fecha"].dt.month)["total"].sum()      # ventas por mes
por_mes.plot(kind="line", marker="o", ax=ax2, title="Ventas por mes (Bs)")   # línea por mes
ax1.set_xlabel("")                             # quita el título del eje X
ax2.set_xlabel("Mes")                          # título del eje X
fig.tight_layout()                             # acomoda los gráficos
fig.savefig("resumen_ventas.png")              # guarda el gráfico como imagen
datos.to_excel("informe_ventas.xlsx", index=False)   # exporta la tabla limpia a Excel
print("Archivos creados: resumen_ventas.png e informe_ventas.xlsx")
plt.show()                                     # abre el gráfico en una ventana
