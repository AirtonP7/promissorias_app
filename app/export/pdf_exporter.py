from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from textwrap import wrap
from datetime import datetime
import re
import os

def export_promissorias_pdf(promissorias, filename="promissoria.pdf", logo_path=None, logo_position="left"):
    if not promissorias:
        return filename

    # Pega o nome do devedor da primeira promissória
    devedor = promissorias[0].get("devedor", "Devedor")
    # Substitui espaços e caracteres inválidos por "_"
    devedor_safe = re.sub(r'[^A-Za-z0-9_-]+', '_', devedor.strip())

    # Data e hora atuais
    agora = datetime.now().strftime("%d-%m-%Y_%H-%M")

    # Monta o nome final
    filename = f"Promissoria_{devedor_safe}_{agora}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin = 15 * mm
    padding = 6 * mm
    espaco_entre = 8 * mm   # espaço maior entre promissórias
    caixa_altura = ((height - 2*margin) - 2*espaco_entre) / 2
    caixa_largura = width - 2*margin

    for idx, prom in enumerate(promissorias):
        pos = idx % 2
        if idx > 0 and pos == 0:
            c.showPage()

        y_top = height - margin - pos*(caixa_altura + espaco_entre)

        # Moldura da promissória
        c.setLineWidth(1.2)
        c.setStrokeColor(HexColor("#000000"))
        c.rect(margin, y_top - caixa_altura, caixa_largura, caixa_altura)

        # Título
        titulo_y = y_top - padding - 5*mm
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(HexColor("#0E5A31"))
        c.drawCentredString(width/2, titulo_y, "NOTA DE PROMISSÓRIA")

        # Logo opcional
        if logo_path:
            try:
                logo = ImageReader(logo_path)
                if logo_position == "left":  # esquerda do título
                    logo_width = 20*mm
                    logo_height = 20*mm
                    logo_y = titulo_y - (logo_height/2) + 5
                    c.drawImage(
                        logo,
                        margin + padding,
                        logo_y,
                        width=logo_width,
                        height=logo_height,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                elif logo_position == "center":  # central acima do título
                    logo_width = 30*mm
                    logo_height = 30*mm
                    c.drawImage(
                        logo,
                        (width - logo_width)/2,
                        titulo_y + 10*mm,
                        width=logo_width,
                        height=logo_height,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
            except:
                pass

        # Linha divisória abaixo do título
        linha_y = titulo_y - 6*mm
        c.setStrokeColor(HexColor("#6D6D6D"))
        c.setLineWidth(0.5)
        c.line(margin + padding, linha_y, width - margin - padding, linha_y)

        # Cabeçalho
        y_text = titulo_y - 12*mm
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(HexColor("#000000"))
        c.drawString(margin + padding, y_text, f"Devedor: {prom.get('devedor','')}")
        c.drawString(width/2 + padding, y_text, f"Valor Total: {prom.get('valor_total','')}")
        y_text -= 5*mm
        c.drawString(margin + padding, y_text, f"Data Emissão: {prom.get('data_emissao','')}")    
        c.drawString(width/2 + padding, y_text, f"Valor da Parcela: {prom.get('valor_parcela','')}")
        y_text -= 5*mm
        c.drawString(margin + padding, y_text, f"Vencimento: {prom.get('vencimento','')}")
        y_text -= 8*mm

        # Corpo (texto principal da promissória)
        corpo_lines = wrap(prom.get("corpo", ""), width=85)

        min_corpo_y = y_top - caixa_altura + padding + 20*mm  
        text_object = c.beginText()
        text_object.setFont("Helvetica", 10)
        text_object.setFillColor(HexColor("#000000"))

        y_text = y_top - padding - 45*mm
        text_object.setTextOrigin(margin + padding, y_text)

        for line in corpo_lines:
            if text_object.getY() < min_corpo_y:
                break
            text_object.textLine(line)

        c.drawText(text_object)

        # Rodapé
        rodape_y = y_top - caixa_altura + padding + 30*mm  
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#000000"))
        c.drawString(margin + padding, rodape_y, "Pagável em Fortaleza - Ceará")
        rodape_y -= 5*mm
        c.drawString(margin + padding, rodape_y,
                     f"Emitente: {prom.get('emitente','')}   CPF: {prom.get('cpf_emitente','')}")
        rodape_y -= 5*mm
        c.drawString(margin + padding, rodape_y, "FORTALEZA _____/_____/_____")

        # Assinatura
        c.setFont("Helvetica", 9)
        c.drawCentredString(width/2, rodape_y - 8*mm, "Assinatura do Devedor:")
        c.setLineWidth(1.5)
        c.line(width/2 - 40*mm, rodape_y - 16*mm, width/2 + 40*mm, rodape_y - 16*mm)

        # Numeração
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(HexColor("#000000"))
        c.drawRightString(width - margin - padding, y_top - caixa_altura + padding,
                          f"N° Promissória {idx+1}/{len(promissorias)}")

    c.save()
    return filename
