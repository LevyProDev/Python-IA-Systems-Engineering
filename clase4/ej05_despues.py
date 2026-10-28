"""Tengo datos/ventas_limpias.csv con las columnas: fecha, producto, region, vendedor, cantidad, precio_unitario y total. Mejora este código: calcula indicadores (total vendido, venta promedio, número de ventas, mejor producto y mejor región) en una tabla; pide el nombre del informe (Enter = informe_ventas) y exporta un Excel con las hojas Indicadores, Por región, Por producto y Por mes. Muestra al final los nombres de las hojas creadas. Comenta el código línea por línea."""
# Indicadores e informe en Excel - versión mejorada con IA
from pathlib import Path   # herramienta para trabajar con rutas de archivos
import pandas as pd        # librería para analizar datos
 
BASE = Path(__file__).parent   # carpeta donde está este script
RUTA = BASE / "datos" / "ventas_limpias.csv"   # CSV limpio (ejercicio 3)
 
 
def calcular_indicadores(df):   # devuelve una tabla con los indicadores principales
    por_producto = df.groupby("producto")["total"].sum()   # total por producto
    por_region = df.groupby("region")["total"].sum()   # total por región
    indicadores = {   # indicador -> valor
        "Total vendido (Bs)": round(df["total"].sum()),
        "Venta promedio (Bs)": round(df["total"].mean()),
        "Número de ventas": len(df),
        "Mejor producto": por_producto.idxmax(),   # idxmax = nombre con el valor más alto
        "Mejor región": por_region.idxmax(),
    }
    return pd.DataFrame({"Indicador": indicadores.keys(), "Valor": indicadores.values()})
 
 
def main():   # función principal
    if not RUTA.exists():   # si no existe el CSV limpio...
        print("Falta ventas_limpias.csv. Ejecuta primero ej03_despues.py")
        return   # termina el programa
    df = pd.read_csv(RUTA, parse_dates=["fecha"])   # lee el CSV
    indicadores = calcular_indicadores(df)   # calcula los indicadores
    print(indicadores.to_string(index=False))   # los muestra sin la columna de números
    nombre = input("Nombre del informe (Enter = informe_ventas): ").strip()   # pide el nombre
    if nombre == "":   # si no escribe nada...
        nombre = "informe_ventas"   # usa el nombre por defecto
    archivo = BASE / f"{nombre}.xlsx"   # ruta completa del informe
    with pd.ExcelWriter(archivo) as excel:   # abre un Excel para escribir varias hojas
        indicadores.to_excel(excel, sheet_name="Indicadores", index=False)   # hoja 1
        df.groupby("region")["total"].sum().to_excel(excel, sheet_name="Por región")   # hoja 2
        df.groupby("producto")["total"].sum().to_excel(excel, sheet_name="Por producto")
        por_mes = df.groupby(df["fecha"].dt.month)["total"].sum()   # total por mes
        por_mes.to_excel(excel, sheet_name="Por mes")   # hoja 4
    hojas = pd.ExcelFile(archivo).sheet_names   # lee los nombres de las hojas creadas
    print(f"Informe guardado: {archivo.name}")   # avisa el nombre
    print(f"Hojas: {', '.join(hojas)}")   # muestra las hojas
 
 
main()   # ejecuta el programa
