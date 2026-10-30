# crear_documentos_prueba.py
# Paso previo: crea los documentos FICTICIOS para probar la aplicación (no contienen datos reales)
from pathlib import Path                  # herramienta para trabajar con rutas de archivos
from reportlab.lib.pagesizes import A4    # tamaño de hoja A4
from reportlab.pdfgen import canvas       # herramienta para "dibujar" texto en un PDF
 
CARPETA = Path(__file__).parent / "documentos_prueba"   # carpeta donde se guardan los documentos
 
CONTRATO = [   # (título, párrafos) de cada página del contrato de 12 páginas
    ("Cláusula 1: Objeto", ["El Prestador brindará asesoría contable mensual a Cliente Ejemplo S.A.",
                            "Incluye revisión de libros, preparación de informes y atención de consultas."]),
    ("Cláusula 2: Vigencia", ["El contrato dura 12 meses, desde el 1 de noviembre de 2026.",
                              "Puede renovarse por escrito con 30 días de anticipación."]),
    ("Cláusula 3: Honorarios", ["Los honorarios son de Bs 8.500 mensuales, facturados el primer día hábil.",
                                "Los honorarios no incluyen viáticos ni gastos de terceros."]),
    ("Cláusula 4: Plazo de pago", ["El Cliente pagará cada factura dentro de 30 días calendario desde su recepción.",
                                   "Los pagos se realizan por transferencia bancaria."]),
    ("Cláusula 5: Penalidades por retraso", ["El retraso en el pago genera un interés del 2% mensual sobre el saldo.",
                                             "Si el retraso supera 60 días, el Prestador puede suspender el servicio."]),
    ("Cláusula 6: Entrega de informes", ["El Prestador entregará un informe mensual hasta el día 5 de cada mes.",
                                         "Los informes se envían por correo electrónico al responsable del Cliente."]),
    ("Cláusula 7: Confidencialidad", ["Ambas partes guardarán reserva de la información durante 5 años.",
                                      "La obligación continúa después de terminado el contrato."]),
    ("Cláusula 8: Propiedad de los documentos", ["Los documentos del Cliente siguen siendo de su propiedad.",
                                                 "El Prestador conservará copias solo mientras dure el servicio."]),
    ("Cláusula 9: Responsabilidad", ["La responsabilidad del Prestador se limita a los honorarios de 3 meses.",
                                     "No responde por decisiones tomadas sin su asesoría."]),
    ("Cláusula 10: Terminación", ["Cualquiera de las partes puede terminar el contrato con 45 días de aviso previo.",
                                  "La terminación no elimina los pagos pendientes."]),
    ("Cláusula 11: Controversias", ["Las partes buscarán resolver las diferencias por negociación directa.",
                                    "Si no hay acuerdo, se someterán a los tribunales de La Paz, Bolivia."]),
    ("Cláusula 12: Firmas", ["Se firma en dos ejemplares del mismo tenor, en la ciudad de La Paz.",
                             "Este documento es ficticio y se usa solo con fines educativos."]),
]
POLITICA = [   # (título, párrafos) de la política de reembolsos de 4 páginas
    ("Reembolsos: alcance", ["Esta política aplica a las compras de productos de la empresa ficticia Andina Demo."]),
    ("Reembolsos: plazos", ["Se aceptan solicitudes dentro de 10 días hábiles desde la recepción del producto.",
                            "El reembolso se realiza en 7 días hábiles después de aprobada la solicitud."]),
    ("Reembolsos: condiciones", ["El producto debe estar sin uso y con su factura original."]),
    ("Reembolsos: excepciones", ["Los productos personalizados no admiten reembolso, salvo defecto de fabricación."]),
]
 
 
def crear_pdf(ruta, titulo, paginas):   # crea un PDF con una página por cada elemento de la lista
    pdf = canvas.Canvas(str(ruta), pagesize=A4)   # crea el PDF vacío
    alto = A4[1]   # altura de la hoja
    for numero, (subtitulo, parrafos) in enumerate(paginas, start=1):   # una página por elemento
        pdf.setFont("Helvetica-Bold", 18)   # letra grande y en negrita
        pdf.drawString(50, alto - 70, titulo)   # título del documento
        pdf.setFont("Helvetica-Bold", 14)   # letra mediana en negrita
        pdf.drawString(50, alto - 110, f"Página {numero} - {subtitulo}")   # subtítulo de la página
        pdf.setFont("Helvetica", 11)   # letra normal
        y = alto - 145   # posición vertical del primer párrafo
        for parrafo in parrafos:   # escribe cada párrafo
            pdf.drawString(50, y, parrafo)
            y -= 22   # baja una línea
        pdf.showPage()   # termina la página
    pdf.save()   # guarda el PDF
 
 
def main():   # función principal
    CARPETA.mkdir(exist_ok=True)   # crea la carpeta si no existe
    crear_pdf(CARPETA / "contrato_servicios_demo.pdf", "Contrato de Servicios (documento ficticio)", CONTRATO)
    crear_pdf(CARPETA / "politica_reembolsos_demo.pdf", "Política de Reembolsos (documento ficticio)", POLITICA)
    pdf = canvas.Canvas(str(CARPETA / "pdf_sin_texto_demo.pdf"), pagesize=A4)   # PDF que solo tiene un dibujo
    pdf.rect(100, 400, 300, 200, fill=1)   # dibuja un rectángulo (sin texto)
    pdf.save()   # lo guarda
    (CARPETA / "archivo_danado_demo.pdf").write_text("Esto no es un PDF real.", encoding="utf-8")   # archivo roto
    print("Documentos de prueba creados en la carpeta documentos_prueba:")
    print("  contrato_servicios_demo.pdf    (12 páginas)")
    print("  politica_reembolsos_demo.pdf   (4 páginas)")
    print("  pdf_sin_texto_demo.pdf         (solo un dibujo: sirve para probar el aviso de 'sin texto')")
    print("  archivo_danado_demo.pdf        (no es un PDF real: sirve para probar el aviso de error)")
 
 
main()   # ejecuta el programa
