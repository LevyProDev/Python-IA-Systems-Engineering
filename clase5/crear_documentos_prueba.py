# crear_documentos_prueba.py
# Crea documentos FICTICIOS para practicar con la IA local (no contienen datos reales)
from pathlib import Path   # herramienta para trabajar con carpetas y archivos
 
CARPETA = Path(__file__).parent / "documentos"   # carpeta donde se guardan los documentos
 
INFORME = """# Informe financiero del 3.er trimestre 2026
**Empresa:** Andina Demo S.R.L. (empresa ficticia)
**Moneda:** bolivianos (Bs)
 
## Ingresos
| Mes | Monto |
|---|---|
| Julio | Bs 120.000 |
| Agosto | Bs 135.000 |
| Septiembre | Bs 128.000 |
 
**Total de ingresos del trimestre: Bs 395.000**
 
## Gastos
| Concepto | Monto |
|---|---|
| Sueldos | Bs 150.000 |
| Alquiler | Bs 36.000 |
| Servicios básicos | Bs 18.000 |
| Marketing | Bs 22.000 |
 
**Total de gastos del trimestre: Bs 226.000**
 
## Resultado
- Utilidad del trimestre: Bs 169.000
- Margen de utilidad: 43%
- Los ingresos crecieron 16% frente al trimestre anterior (Bs 340.000).
- Saldo bancario inicial al 1 de septiembre: Bs 50.000
- Saldo bancario final al 30 de septiembre: Bs 82.150
 
## Comentarios de gerencia
Las ventas de septiembre fueron las más altas del trimestre.
Se recomienda mantener el control de gastos y renegociar el alquiler.
"""
 
CONTRATO = """# Contrato de prestación de servicios (documento ficticio)
Entre Estudio Demo S.R.L. (el Prestador) y Cliente Ejemplo S.A. (el Cliente).
 
## Cláusula 1. Objeto
El Prestador brindará asesoría contable mensual al Cliente.
 
## Cláusula 2. Vigencia
El contrato dura 12 meses, desde el 1 de octubre de 2026 hasta el 30 de junio de 2027.
 
## Cláusula 3. Honorarios
El Cliente pagará Bs 5.000 mensuales. El total por la vigencia del contrato es de Bs 55.000.
 
## Cláusula 4. Retraso en el pago
Si el pago se retrasa, se aplicará una penalidad del 10% sobre el monto adeudado.
 
## Cláusula 5. Confidencialidad
Ambas partes guardarán reserva de la información intercambiada.
 
## Cláusula 6. Resolución
Cualquiera de las partes puede terminar el contrato con un aviso previo de 30 días.
 
## Cláusula 7. Penalidades
Ante cualquier retraso en el pago, se aplicará una penalidad del 15% mensual.
 
## Cláusula 8. Preaviso
El aviso de terminación debe darse con 15 días de anticipación.
"""
 
ACTA = """# Acta de reunión del equipo administrativo (documento ficticio)
**Fecha de la reunión:** 14 de octubre de 2026
**Asistentes:** Rosa (Contabilidad), Pedro (Legal), Elena (Administración)
 
## Temas tratados
1. Cierre contable de septiembre.
2. Renovación del contrato de alquiler.
3. Auditoría interna de octubre.
 
## Acuerdos
- Rosa enviará el cierre contable de septiembre hasta el 10 de octubre.
- Pedro revisará el borrador del contrato de alquiler y lo devolverá el 21 de octubre.
- Elena coordinará la auditoría interna para la semana del 26 de octubre.
- Se aprobó un presupuesto de Bs 8.000 para la auditoría.
"""
 
MOVIMIENTOS = """fecha,concepto,tipo,monto
2026-09-01,Cobro cliente Alfa,ingreso,25000
2026-09-03,Pago alquiler,egreso,12000
2026-09-05,Cobro cliente Beta,ingreso,18000
2026-09-08,Pago sueldos,egreso,40000
2026-09-10,Compra materiales,egreso,6500
2026-09-12,Cobro cliente Gamma,ingreso,30000
2026-09-15,Pago servicios,egreso,4200
2026-09-18,Cobro cliente Alfa,ingreso,22000
2026-09-22,Pago impuestos,egreso,9800
2026-09-25,Pago marketing,egreso,7000
2026-09-28,Cobro cliente Delta,ingreso,15000
2026-09-30,Comisión bancaria,egreso,350
"""
 
 
def main():   # función principal
    CARPETA.mkdir(exist_ok=True)   # crea la carpeta documentos si no existe
    (CARPETA / "informe_financiero.md").write_text(INFORME, encoding="utf-8")   # informe
    (CARPETA / "contrato_servicio.md").write_text(CONTRATO, encoding="utf-8")   # contrato
    (CARPETA / "acta_reunion.md").write_text(ACTA, encoding="utf-8")   # acta
    (CARPETA / "movimientos_bancarios.csv").write_text(MOVIMIENTOS, encoding="utf-8")   # CSV
    print("Documentos ficticios creados en la carpeta documentos:")
    print("  informe_financiero.md")
    print("  acta_reunion.md")
    print("  contrato_servicio.md")
    print("  movimientos_bancarios.csv")
 
 
main()   # ejecuta el programa
