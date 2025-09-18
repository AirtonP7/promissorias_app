from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from textwrap import wrap
from num2words import num2words

def export_contrato_pdf(contrato_data, filename="contrato.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 15 * mm
    max_width = width - 2 * margin
    y_pos = height - margin

    # ---------------------------
    # Logo centralizado
    # ---------------------------
    try:
        logo = ImageReader("app/assets/images/logo.png")
        logo_width = 50 * mm
        logo_height = 20 * mm
        c.drawImage(
            logo,
            (width - logo_width)/2,
            y_pos - logo_height,
            width=logo_width,
            height=logo_height,
            mask='auto',  # mantém fundo transparente
            preserveAspectRatio=True
        )
        y_pos -= logo_height + 5
    except:
        pass

    # Linha divisória
    c.setStrokeColor(HexColor("#0E5A31"))
    c.setLineWidth(1)
    c.line(margin, y_pos, width - margin, y_pos)
    y_pos -= 15

    # ---------------------------
    # Título do contrato
    # ---------------------------
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor("#333333"))
    c.drawCentredString(width / 2, y_pos, "CONTRATO PARTICULAR DE VENDA")
    y_pos -= 20

    # ---------------------------
    # Converter valores e número de parcelas por extenso
    # ---------------------------
    valor_extenso = num2words(contrato_data['valor_total'], lang='pt_BR').title()
    num_parcelas_extenso = num2words(contrato_data['num_parcelas'], lang='pt_BR').title()

    # ---------------------------
    # Função para escrever texto com quebra e multipágina
    # ---------------------------
    def draw_wrapped_text(c, text, x, y, max_width, line_height=12, font="Helvetica", size=11, bold_lines=None):
        c.setFont(font, size)
        c.setFillColor(HexColor("#000000"))
        if bold_lines is None:
            bold_lines = []
        for idx, paragraph in enumerate(text.split("\n")):
            lines = wrap(paragraph.strip(), width=95)
            for line in lines:
                if y < margin + 50:  # nova página
                    c.showPage()
                    y = height - margin
                if idx in bold_lines:
                    c.setFont("Helvetica-Bold", size)
                else:
                    c.setFont(font, size)
                c.drawString(x, y, line)
                y -= line_height
            y -= 6
        return y

    # ---------------------------
    # Texto principal
    # ---------------------------
    contrato_texto = f"""
Pelo presente contrato particular de empréstimo de dinheiro, de um lado,
{contrato_data['nome_empresa']}, CNPJ nº {contrato_data['cnpj_empresa']}, doravante denominado CREDOR,
e, de outro lado, {contrato_data['nome_devedor']} inscrito no CPF/CNPJ nº {contrato_data['cpf_devedor']}, doravante denominado DEVEDOR,
têm justo e contratado o seguinte:

CLÁUSULA 1ª
O CREDOR dá como empréstimo ao DEVEDOR, a quantia de R$: {contrato_data['valor_total']:,.2f} ({valor_extenso}) mediante as condições seguintes.

CLÁUSULA 2ª
Que a quantia acima emprestada foi paga em espécie ao DEVEDOR, e que o mesmo pagará o valor do empréstimo conforme condições estabelecidas em contrato
junto à empresa em {contrato_data['num_parcelas']} ({num_parcelas_extenso}) Notas Promissórias nos seguintes vencimentos:
"""

    # Lista das parcelas
    parcelas_lista = "\n".join([f" - Parcela {i+1}: Vencimento {p['vencimento']} — Valor: R$ {p['valor']:,.2f}"
                                for i, p in enumerate(contrato_data['parcelas'])])
    contrato_texto += f"{parcelas_lista}\n\ncomo forma de garantia.\n"

    contrato_texto += """
CLÁUSULA 3ª
Na falta do pagamento do empréstimo dentro do prazo e data, o CREDOR poderá executar a dívida através do protesto da Nota Promissória e cobrança judicial.

CLÁUSULA 4ª
Todos os encargos que venham a recair durante o período de pagamento do empréstimo, serão de responsabilidade do DEVEDOR.

CLÁUSULA 5ª
Fica eleito o foro desta cidade de Fortaleza/CE, para dirimir qualquer dúvida referente a este contrato. 
E assim, por estarem plenamente contratados na forma acima, assinam o presente contrato em duas vias de igual teor.

"""

    # Definir quais linhas serão em negrito (Cláusulas)
    bold_lines = []
    for idx, line in enumerate(contrato_texto.split("\n")):
        if "CLÁUSULA" in line:
            bold_lines.append(idx)

    y_pos = draw_wrapped_text(c, contrato_texto, margin, y_pos, max_width, font="Helvetica", size=11, bold_lines=bold_lines)

    # ---------------------------
    # Assinaturas
    # ---------------------------
    y_pos -= 30
    if y_pos < margin + 100:
        c.showPage()
        y_pos = height - margin

    c.drawString(margin, y_pos, f"FORTALEZA _____/_____/_____")
    y_pos -= 60
    c.drawString(margin, y_pos, f"CREDOR: ______________________________")
    y_pos -= 30
    c.drawString(margin, y_pos, f"DEVEDOR: ______________________________")
    y_pos -= 30
    c.drawString(margin, y_pos, "TESTEMUNHA: ______________________________")
    y_pos -= 30
    c.drawString(margin, y_pos, "TESTEMUNHA: ______________________________")

    c.save()
    return filename
