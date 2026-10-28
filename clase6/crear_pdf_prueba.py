# crear_pdf_prueba.py
# Crea un PDF FICTICIO de 80 páginas: "Manual de Políticas y Contratos 2026"
from pathlib import Path   # herramienta para trabajar con rutas de archivos
from reportlab.lib.pagesizes import A4   # tamaño de hoja A4
from reportlab.lib.styles import getSampleStyleSheet   # estilos de texto listos para usar
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer   # piezas del PDF
 
ARCHIVO = Path(__file__).parent / "manual_politicas_2026.pdf"   # PDF que vamos a crear
 
AREAS = ["Compras", "Contabilidad", "Legal", "Almacén", "Recursos Humanos",
         "Sistemas", "Ventas", "Logística", "Tesorería", "Auditoría"]   # 10 áreas de la empresa
CAPITULOS = ["Disposiciones generales", "Pagos a proveedores", "Contratos y condiciones",
             "Penalizaciones", "Aprobación de solicitudes", "Devoluciones",
             "Procedimientos administrativos por área", "Anexos y formularios"]   # 8 capítulos
 
# Artículos importantes (capítulo, número): son los que usaremos para hacer preguntas
CLAVES = {
    (1, 1): "Este manual establece las políticas de pagos, contratos, aprobaciones y devoluciones "
            "de Andina Demo S.R.L. (empresa ficticia). Rige desde el 1 de enero de 2026.",
    (2, 1): "El plazo general de pago a proveedores es de 15 días calendario desde la recepción "
            "de la factura aprobada. Los pagos se hacen por transferencia los martes y jueves.",
    (2, 2): "Los proveedores del exterior tienen un plazo de pago de 45 días calendario "
            "desde la fecha del embarque de la mercadería.",
    (3, 1): "Los contratos con proveedores tienen una vigencia máxima de 12 meses y pueden "
            "renovarse por escrito. Cualquiera de las partes puede terminarlos con 30 días de aviso.",
    (3, 2): "Todo contrato superior a Bs 50.000 debe ser revisado por el área Legal antes de la firma.",
    (4, 1): "Si un proveedor se retrasa en la entrega, se aplica una penalización del 2% del valor "
            "del pedido por cada semana de retraso, con un máximo del 10%.",
    (4, 2): "Si un cliente se retrasa en el pago, se cobra un interés del 1,5% mensual "
            "sobre el saldo adeudado.",
    (5, 1): "Toda solicitud debe incluir: el formulario SOL-01 completo, una cotización vigente, "
            "la aprobación firmada del jefe de área y la documentación de respaldo.",
    (5, 2): "Las solicitudes de hasta Bs 1.000 las aprueba el jefe de área; las de más de Bs 1.000 "
            "y hasta Bs 10.000, la gerencia administrativa; las de más, la gerencia general.",
    (6, 1): "Las devoluciones se aceptan dentro de 10 días hábiles desde la recepción, con el "
            "producto sin uso y la factura original. El reembolso se realiza en 7 días hábiles.",
    (6, 2): "Los productos defectuosos se cambian sin costo dentro de 30 días calendario.",
}
 
# Plantillas para el resto de artículos (cambian según el área y el número)
PLANTILLAS = {
    1: "Alcance para el área de {area}: el personal de {area} debe conocer y aplicar este manual. "
       "Las consultas se responden en un máximo de {k_mas} días hábiles.",
    2: "Pagos del área de {area}: los pagos de {area} superiores a Bs {monto} requieren una segunda "
       "firma de Tesorería. La documentación se archiva durante {anios} años.",
    3: "Contratos del área de {area}: el contrato modelo para {area} incluye la cláusula de "
       "confidencialidad número {k} y se revisa cada año.",
    4: "Penalizaciones internas del área de {area}: los incumplimientos de plazos internos se registran "
       "en el informe mensual. Tras {k} incumplimientos en un trimestre se revisan los procesos.",
    5: "Solicitudes del área de {area}: se registran con el código {codigo}-{numero} "
       "y se responden en un máximo de {k} días hábiles.",
    6: "Devoluciones del área de {area}: el responsable de {area} registra la devolución en el "
       "formulario DEV-0{k} y la envía a Contabilidad el mismo día.",
    7: "Procedimiento del área de {area}: atención de {entrada}:00 a {salida}:00 horas; caja menor máxima "
       "de Bs {caja}; el archivo físico se conserva {anios} años.",
    8: "Anexo {k}: formulario {codigo}-{k:02d}. Se presenta en original y copia al área de {area} "
       "y se conserva {anios} años.",
}
 
 
def articulo(capitulo, k):   # devuelve el texto principal del artículo k del capítulo dado
    if (capitulo, k) in CLAVES:   # si es un artículo importante...
        return CLAVES[(capitulo, k)]   # usa su texto especial
    area = AREAS[k - 1]   # área que corresponde a este artículo
    return PLANTILLAS[capitulo].format(   # si no, usa la plantilla del capítulo
        area=area, k=k, k_mas=k + 1, monto=f"{2000 + 500 * k:,}".replace(",", "."),
        anios=4 + k % 3, codigo=area[:3].upper(), numero=100 + k,
        entrada=7 + k % 3, salida=16 + k % 3, caja=300 * k)
 
 
def observacion(capitulo, k):   # devuelve un párrafo de observaciones, distinto en cada página
    area = AREAS[(k + capitulo) % 10]   # área de apoyo
    return (f"Observaciones: el área de {area} actúa como apoyo en este procedimiento y puede pedir "
            f"una revisión adicional cuando el monto supere Bs {1000 * (k + capitulo)}. "
            "Toda excepción debe quedar registrada por escrito y firmada por el responsable.")
 
 
def main():   # función principal
    estilos = getSampleStyleSheet()   # estilos de texto
    documento = SimpleDocTemplate(str(ARCHIVO), pagesize=A4, leftMargin=50, rightMargin=50,
                                  topMargin=60, bottomMargin=50)   # configura el PDF
    elementos = []   # lista de todo lo que irá en el PDF
    for numero in range(1, 81):   # 80 páginas
        capitulo = (numero - 1) // 10 + 1   # capítulo 1 a 8
        k = (numero - 1) % 10 + 1   # artículo 1 a 10 dentro del capítulo
        titulo = f"Capítulo {capitulo}: {CAPITULOS[capitulo - 1]} (página {numero})"   # subtítulo
        elementos.append(Paragraph("Manual de Políticas y Contratos 2026", estilos["Title"]))   # título
        elementos.append(Paragraph(titulo, estilos["Heading2"]))   # subtítulo
        elementos.append(Spacer(1, 12))   # espacio en blanco
        elementos.append(Paragraph(f"<b>Artículo {capitulo}.{k}.</b> {articulo(capitulo, k)}",
                                   estilos["BodyText"]))   # texto principal
        elementos.append(Spacer(1, 10))   # espacio en blanco
        elementos.append(Paragraph(observacion(capitulo, k), estilos["BodyText"]))   # observaciones
        elementos.append(Spacer(1, 10))   # espacio en blanco
        elementos.append(Paragraph("Documento ficticio para fines educativos.", estilos["Italic"]))
        elementos.append(PageBreak())   # salto de página
    documento.build(elementos[:-1])   # crea el PDF (sin el último salto de página)
    print(f"PDF creado correctamente: {ARCHIVO.name} (80 páginas)")   # avisa que terminó
 
 
main()   # ejecuta el programa
